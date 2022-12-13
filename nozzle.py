__author__ = "Noah Thomas Compton"
__version__ = "0.0.1"
__email__ = "noah.compton@ufl.edu"
__status__ = "Development"

import gas_dynamics as gd
import math

global y
y = gd.fluids.air.gamma

class Nozzle:
    """A model for describing the characterisics of a nozzle"""

    def __init__(self, **kwargs):
        """Initializes a Nozzle class do define flow changes within the stage.

        Paramerters:

            Parameters are characterized by a dictionary with 2 keys and values to maintain a quantitative and qualitative description.
            The form of the parameters is such: {"value": 0.0, "units": "str"}
            Example: self.Pt_in = {"value": 1000, "units": "kPa"}

            Pt_in           (dict):     Incoming total pressure.
            Tt_in           (dict):     Incoming total temperature.
            W_in            (dict):     Incoming mass flow rate.
            Pt_out          (dict):     Total pressure out of the nozz;e.
            Tt_out          (dict):     Total temperature out of the nozzle.
            W_out           (dict):     Mass flow rate out of the nozzle.
            Pt_P            (dict):     Total pressure ratio for turbofan engine.
            XNM_out         (dict):     Mach value at the exit of the nozzle.
            T_out           (dict):     Static temperature out of the nozzle.
            P_out           (dict):     Static pressure out of the nozzle.
            u_out           (dict):     Velocity at exit of nozzle.
            u_eff           (dict):     Effective velocity out of the nozzle.
            a_out           (dict):     Speed of sound out of the nozzle.
            S1              (dict):     Arbitrary variable defined for calculation.
            S2              (dict):     Arbitrary variable defined for calculation.                                
                                    
        """

        initial = {"value": 0.0, "units": "-"}

        self.name = ""
        self.inlet = ""
        self.outlet = ""

        # Inlet
        self.Pt_in = initial.copy()
        self.Tt_in = initial.copy()
        self.W_in = initial.copy()

        # Outlet
        self.Pt_out = initial.copy()
        self.Tt_out = initial.copy()
        self.W_out = initial.copy()
        self.Pt_P = initial.copy()
        self.XMN_out = initial.copy()
        self.T_out = initial.copy()
        self.P_out = initial.copy()
        self.u_out = initial.copy()
        self.u_effective = initial.copy()
        self.W_out = initial.copy()

        # Characteristics
        self.a_out = initial.copy()
        self.S1 = initial.copy()
        self.S2 = initial.copy()

        for property in kwargs:
            values = kwargs[property]

            """This is checking the inputs for each parameter. If the number of inputs is == 1 then a default unit is assigned.
                If input == 0 then a value error is raised
                """

            if len(values) >= 2:
                value = values[0]
                unit = values[1]

                if len(values) > 2 and property != "name":
                    raise Warning(
                        f"Too many inputs for property {property}. First two inputs will be used."
                    )

            elif len(values) == 1:
                value = values[0]
                unit = ""

            else:
                raise ValueError("Not enough inputs.")

            if property == "Pt_in":
                self.Pt_in["value"] = value

                if len(values) == 2:
                    self.Pt_in["units"] = unit

                elif len(values) < 2:
                    self.Pt_in["units"] = "kPa"
                    raise Warning("Not enough inputs: assuming kPa as units for Pt_in.")

            elif property == "Tt_in":
                self.Tt_in["value"] = value

                if len(values) == 2:
                    self.Tt_in["units"] = unit

                if len(values) < 2:
                    self.Tt_in["units"] = "K"
                    raise Warning("Not enough inputs: assuming K as units for Tt_in.")

            elif property == "PR":
                self.PR["value"] = value

                if len(values) == 2:
                    self.PR["unit"] = unit

                if len(values) < 2:
                    self.PR["units"] = ""
                    raise Warning(
                        "Not enough inputs: assuming dimensionless parameter."
                    )

            elif property == "TR":
                self.TR["value"] = value

                if len(values) == 2:
                    self.TR["units"] = unit

                elif len(values) < 2:
                    self.TR["units"] = ""
                    raise Warning(
                        "Not enough inputs: assuming dimensionless parameter."
                    )

            elif property == "name":
                self.name = values

            else:
                raise ValueError("Incorrect inputs!")

    def calc(self):
        """The main calculation method for the class. Should only be run once when evaluating the nozzle.
        Requirements:
            The parameters described earlier must be defined.
            Calc methods for previous stages must be run.
                The previous stages are:
                    Inlet
                    Fan
                    Compressor
                    Burner
                    Turbine
                    Mixer
                If these stages are not analyzed before using this class method then results will be incorrect.
        """

        y = gd.fluids.air.gamma

        if self.PR["value"] > 0 and self.Pt_in["value"]:
            self.Pt_out["value"] = self.PR["value"] * self.Pt_in["value"]

        else:
            raise ValueError("Incorrecpt inputs for nozzle.")

        # self.P_out["value"] = Freestream.P["value"]
        self.Pt_P["value"] = self.Pt_out["value"] / self.P_out["value"]
        self.S1["value"] = (self.Pt_P["value"]) ** ((y - 1) / y) - 1
        self.XMN_out["value"] = math.sqrt(2 * self.S1["value"] / (y - 1))
        self.Tt_out["value"] = self.Tt_in["value"]
        self.S2["value"] = 2 + (y - 1) * self.XMN_out["value"] ** 2
        self.T_out["value"] = 2 * (self.Tt_out["value"] / self.S2["value"])
        self.a_out["value"] = math.sqrt(y * gd.fluids.air.R * self.T_out["value"])
        self.u_out["value"] = self.a_out["value"] * self.XMN_out["value"]
        self.u_effective["value"] = self.u_out["value"]
        self.W_out["value"] = self.W_in["value"]

        self.P_out["units"] = self.Pt_in["units"]
        self.Pt_out["units"] = self.Pt_in["units"]
        self.Pt_P["units"] = ""
        self.S1["units"] = ""
        self.XMN_out["units"] = ""
        self.S2["units"] = ""
        self.Tt_out["units"] = self.Tt_in["units"]
        self.T_out["units"] = self.Tt_in["units"]
        self.a_out["units"] = "m/s"
        self.u_out["units"] = "m/s"
        self.u_effective["units"] = self.u_out["units"]
        self.W_out["units"] = self.W_in["units"]

    # Defining the string method for the class.
    def __str__(self):
        str = f"{self.name} Characteristics:\n" f"Efficiency:\n" f"Pressure Ratio:\n"
        return str
