# Date    | Description of Changes:                          | Author
# -----------------------------------------------------------------------------
# Dec 4   | Changed W_core to W_in and added W_out.          | Noah C.
#         | Changed W_f to Wf. Edited for loop:              |
#         |     "for value in kwargs"                        |
#         |        - changed to                              |
#         |     "for property in kwargs"                     |
# ----------------------------------------------------------------------------
# Dec 3   | Added units & _str_ def                          | Noah C.
# ----------------------------------------------------------------------------
# Dec 3   | Added remaining calc.                            | Noah C.
#         | Need to check characteristics.                   |
#         | To do:                                           |
#         |  - add _str_ def                                 |
#         |  - check remaining stuff                         |
# ----------------------------------------------------------------------------
# Dec 3   | Static T def set. Variable names changed.        | Noah C.
#         | To do:                                           |
#         |  - Create cacl(self) method                      |
#         |  - Define remaining outputs/characteristics      |
#         |    - (whew)                                      |
# ----------------------------------------------------------------------------
# Dec 2   | Added comments                                   | Jose R.
#         | Downstream station needs:                        |
#         |  - Static P and T exiting Turbine                |
# ----------------------------------------------------------------------------
# Dec 2   | Turbine changed to a Class with appropriate      | Noah C.
#         | alterations for workability                      |
#         | To do:                                           |
#         |   - Add _str_ method                             |
#         |   - Add a5, byp ratio, m0, mfan, and mf processes  |
# ----------------------------------------------------------------------------
# Nov 25  | First Upload to Github                           |
# ----------------------------------------------------------------------------
# Nov 20  | Initial file creation as a collection of         | Noah C.
#         | functions.                                       |
# ----------------------------------------------------------------------------

# .gamma .R .cp

import gas_dynamics as gd
import math

global y, R
R = gd.fluids.air.R
y = gd.fluids.air.gamma


class Turbine:
    def __init__(self, **kwargs):

        initial = {"value": 0.0, "units": "-"}

        self.name = ""
        self.inlet = ""
        self.outlet = ""

        # Inlet                                     Dec 2; JR Comment
        self.Pt_in = initial.copy()
        self.Tt_in = initial.copy()
        self.W_in = initial.copy()

        self.inlet_TR = initial.copy()
        self.inlet_W_in = initial.copy()
        self.fan_TR = initial.copy()
        self.compr_TR = initial.copy()
        self.burner_f = initial.copy()
        self.burner_TRmax = initial.copy()

        # Outlet
        self.Pt_out = initial.copy()
        self.Tt_out = initial.copy()
        self.P_out = initial.copy()
        self.T_out = initial.copy()
        self.a_out = initial.copy()  # Speed of sound at exit
        self.W_out = initial.copy()

        # Characteristics
        self.PR = initial.copy()  # Pressure Ratio
        self.TR = initial.copy()  # Temperature Ratio
        self.eff_poly = initial.copy()  # Polytropic efficiency
        self.eff_mech = initial.copy()  # Mechanicsal efficiency
        self.BPR = initial.copy()  # BPR -> bypass ratio
        self.XMN_out = initial.copy()  # Mach out
        self.Wf = initial.copy()  # W_f -> fuel flow
        self.W_fan = initial.copy()  # W_fan -> fan mass flow rate

        for property in kwargs:
            values = kwargs[property]

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
                    self.PR["units"] = unit

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

            elif property == "eff_poly":
                self.eff_poly["value"] = value

                if len(values) == 2:
                    self.eff_poly["units"] = unit

                elif len(values) < 2:
                    self.eff_poly["units"] = ""
                    raise Warning("Efficiency being used as a percentage.")

            elif property == "eff_mech":
                self.eff_mech["value"] = value

                if len(values) == 2:
                    self.eff_mech["units"] = unit

                elif len(values) < 2:
                    self.eff_mech["units"] = ""
                    raise Warning("Efficiency being used as a percentage.")

            elif property == "BPR":
                self.BPR["value"] = value

                if len(values) == 2:
                    self.BPR["units"] = unit

                elif len(values) < 2:
                    self.BPR["units"] = ""
                    raise Warning(
                        "Not enough inputs: assuming dimensionless parameter."
                    )

            elif property == "XMN_out":
                self.mach_at_exit["value"] = value

                if len(values) == 2:
                    self.mach_at_exit["units"] = unit

                elif len(values) < 2:
                    self.mach_at_exit["units"] = ""
                    raise Warning("Using Mach as dimensionless parameter.")

            elif property == "W_in":
                self.W_in["value"] = value

                if len(values) == 2:
                    self.W_in["units"] = unit

                elif len(values) < 2:
                    self.W_in["units"] = "kg/s"
                    raise Warning("Not enough inputs: assuming kg/s for units")

            elif property == "Wf":
                self.Wf["value"] = value

                if len(values) == 2:
                    self.Wf["units"] = unit

                elif len(values) < 2:
                    self.Wf["units"] = "kg/s"
                    raise Warning("Not enough inputs: assuming kg/s for units")

            elif property == "inlet_TR":
                self.inlet_TR["value"] = value

                if len(values) == 2:
                    self.inlet_TR["units"] = unit

                elif len(values) < 2:
                    self.inlet_TR["units"] = ""
                    raise Warning("Not enough inputs: assuming dimensionless parameter")

            elif property == "fan_TR":
                self.fan_TR["value"] = value

                if len(values) == 2:
                    self.fan_TR["units"] = unit

                elif len(values) < 2:
                    self.fan_TR["units"] = ""
                    raise Warning("Not enough inputs: assuming dimensionless parameter")

            elif property == "compr_TR":
                self.compr_TR["value"] = value

                if len(values) == 2:
                    self.compr_TR["units"] = unit

                elif len(values) < 2:
                    self.compr_TR["units"] = ""
                    raise Warning("Not enough inputs: assuming dimensionless parameter")

            elif property == "burner_f":
                self.burner_f["value"] = value

                if len(values) == 2:
                    self.burner_f["units"] = unit

                elif len(values) < 2:
                    self.burner_f["units"] = ""
                    raise Warning("Not enough inputs: assuming dimensionless parameter")

            elif property == "burner_TRmax":
                self.burner_TRmax["value"] = value

                if len(values) == 2:
                    self.burner_TRmax["units"] = unit

                elif len(values) < 2:
                    self.burner_TRmax["units"] = ""
                    raise Warning("Not enough inputs: assuming dimensionless parameter")

            elif property == "inlet_W_in":
                self.inlet_W_in["value"] = value

                if len(values) == 2:
                    self.inlet_W_in["units"] = unit

                elif len(values) < 2:
                    self.inlet_W_in["units"] = "kg/s"
                    raise Warning("Not enough inputs: assuming kg/s as units")

            elif property == "name":
                self.name = values

            else:
                raise ValueError("Incorrect inputs!")

    def polytropic_efficiency(TR: float, PR: float, gas=gd.fluids.air) -> float:
        y = gas.gamma

        if TR > 0 and PR > 0:
            eff_poly = (1 - TR) / (1 - (PR ** ((y - 1) / y)))

        else:
            raise ValueError(
                "Incorrect inputs. Temperature ratio and pressure ratio required only."
            )
        return eff_poly

    def Tt_out_from_poly_efficiency(
        Tt_in: float, PR: float, eff_poly: float, gas=gd.fluids.air
    ) -> float:
        y = gas.gamma

        if Tt_in > 0 and PR > 0 and eff_poly > 0:
            if eff_poly > 1:
                raise ValueError(
                    "Please enter an efficiency less than or equal to one."
                )

            Tt_out = (-Tt_in) * eff_poly * (1 - (PR) ** ((y - 1) / y)) - 1

        else:
            raise ValueError(
                "Incorrect inputs. Total temperature in (Tt_in), pressure ratio, and polytropic efficiency required only"
            )
        return Tt_out

    def Pt_out_from_poly_efficiency(
        Pt_in: float, TR: float, eff_poly: float, gas=gd.fluids.air
    ) -> float:
        y = gas.gamma

        if Pt_in > 0 and TR > 0 and eff_poly > 0:
            if eff_poly > 1:
                raise ValueError(
                    "Please enter an efficiency less than or equal to one."
                )

            Pt_out = Pt_in * (1 - ((1 - TR) / eff_poly)) ** (y / (y - 1))

        else:
            raise ValueError(
                "Incorrect inputs. Total pressure in (Pt_in), temperature ratio, and polytropic efficiency required only"
            )

        return Pt_out

    def ideal_Tt_out(self):
        y = 1.4

        if self.Tt_in["value"] > 0 and self.PR["value"] > 0:
            self.Tt_out["value"] = self.Tt_in["value"] * self.PR["value"] ** (
                (y - 1) / y
            )

        else:
            raise ValueError(
                "Incorrect inputs. Total temperature in (Tt_in) and pressure ratio required only."
            )

    def ideal_Pt_out(self):
        y = 1.4

        if self.Pt_in["value"] > 0 and self.TR["value"] > 0:
            self.Pt_out["value"] = self.Pt_in["value"] * self.TR["value"] ** (
                y / (y - 1)
            )

        else:
            raise ValueError(
                "Incorrect inputs. Total pressure in (Pt_in) and temperature ratio required only"
            )

    def pressure_ratio_from_poly_efficiency(
        TR: float, eff_poly: float, gas=gd.fluids.air
    ) -> float:
        y = gas.gamma

        # (1 - ((1 - self.TR["value"]) / self.eff_poly["value"])) ** (y / (y - 1))

        if TR > 0 and eff_poly > 0:
            PR = (1 - ((1 - TR) / eff_poly)) ** (y / (y - 1))

        else:
            raise ValueError(
                "Incorrect inputs. Temperature ratio (TR) and polytropic efficiency required only."
            )

        return PR

    def temp_ratio_from_poly_efficiency(
        PR: float, eff_poly: float, gas=gd.fluids.air
    ) -> float:
        y = gas.gamma

        if PR > 0 and eff_poly > 0:
            TR = PR ** ((y - 1) * eff_poly / y)

        else:
            raise ValueError(
                "Incorrect inputs. Pressure ratio and polytropic efficiency required only."
            )

        return TR

    def temperature_ratio_from_poly_efficiency(self):
        y = 1.4

        if self.PR["value"] > 0 and self.eff_poly["value"] > 0:
            self.TR["value"] = self.PR["value"] ** (
                (y - 1) * self.eff_poly["value"] / y
            )

        else:
            raise ValueError(
                "Incorrect inputs. Pressure ratio and polytropic efficiency required only."
            )

    def static_temperature(self):
        y = 1.4

        if self.Tt_in["value"] > 0 and self.XMN_out["value"] > 0:
            self.T_out["value"] = self.Tt_in["value"] * (
                (1 + 0.5 * (y - 1) * self.XMN_out["value"] ** 2) ** -1
            )

        else:
            raise ValueError(
                "Incorrect inputs. Total tempurature out (Tt5) and Mach out (XMN_out) required only."
            )

    def speed_of_sound_out(Tt_out: float, mach_out: float, gas=gd.fluids.air) -> float:
        y = gas.gamma
        R = gas.R

        if Tt_out > 0 and mach_out > 0:
            T_out = Tt_out * ((1 + 0.5 * (y - 1) * mach_out**2) ** -1)

            a_out = math.sqrt(R * y * T_out)

        else:
            raise ValueError(
                "Incorrect inputs. Total tempurature out (Tt5) and Mach out (mach_out) required only."
            )

        return a_out

    def sonic_velocity_out(self):
        y = 1.4

        if self.Tt_out["value"] > 0 and self.XMN_out["value"] > 0:
            self.T_out["value"] = self.Tt_out["value"] * (
                (1 + 0.5 * (y - 1) * self.XMN_out["value"] ** 2) ** -1
            )

            self.a_out["value"] = math.sqrt(gd.fluids.air.R * y * self.T_out["value"])

        else:
            raise ValueError(
                "Incorrect inputs. Total tempurature out (Tt5) and Mach out (XMN_out) required only."
            )

    def static_pressure_out(
        Pt_out: float, Tt_out: float, mach_out: float, gas=gd.fluids.air
    ) -> float:
        y = gas.gamma

        if Pt_out > 0 and Tt_out > 0 and mach_out > 0:
            T_out = Tt_out * ((1 + 0.5 * (y - 1) * mach_out**2) ** -1)

            P_out = Pt_out * (((Tt_out / T_out) ** (y / (y - 1))) ** -1)

        else:
            raise ValueError(
                "Incorrect inputs. Total temperature out (Tt_out), total pressure out (Pt_out), and Mach number out (XMN_out) required."
            )

        return P_out

    def static_pressure(self):
        y = 1.4

        if (
            self.Pt_out["value"] > 0
            and self.Tt_out["value"] > 0
            and self.XMN_out["value"] > 0
        ):
            self.T_out["value"] = self.Tt_out["value"] * (
                (1 + 0.5 * (y - 1) * self.XMN_out["value"] ** 2) ** -1
            )

            self.P_out["value"] = self.Pt_out["value"] * (
                ((self.Tt_out["value"] / self.T_out["value"]) ** (y / (y - 1))) ** -1
            )

        else:
            raise ValueError(
                "Incorrect inputs. Total temperature out (Tt_out), total pressure out (Pt_out), and Mach number out (XMN_out) required."
            )

    def calc(self):
        y = 1.4

        if self.PR["value"] > 0 and self.eff_poly["value"] > 0:
            self.TR["value"] = self.PR["value"] ** (
                (y - 1) * self.eff_poly["value"] / y
            )
            self.TR["units"] = "-"

        elif self.TR["value"] > 0 and self.eff_poly["value"] > 0:
            self.PR["value"] = (
                1 - ((1 - self.TR["value"]) / self.eff_poly["value"])
            ) ** (y / (y - 1))
            self.PR["units"] = "-"

        elif self.TR["value"] > 0 and self.PR["value"] > 0:
            self.eff_poly["value"] = (1 - self.TR["value"]) / (
                1 - (self.PR["value"] ** ((y - 1) / y))
            )
            self.eff_poly["units"] = "-"

        else:
            raise ValueError("Not enough turbine characteristics defined. Check input.")

        self.TR["value"] = self.PR["value"] ** ((y - 1) * self.eff_poly["value"] / y)
        self.Tt_out["value"] = self.TR["value"] * self.Tt_in["value"]
        self.T_out["value"] = self.Tt_out["value"] * (
            (1 + 0.5 * (y - 1) * self.XMN_out["value"] ** 2) ** -1
        )
        self.a_out["value"] = math.sqrt(y * gd.fluids.air.R * self.T_out["value"])
        self.BPR["value"] = (
            self.eff_mech["value"]
            * (1 + self.burner_f["value"])
            * self.burner_TRmax["value"]
            * (1 - self.TR["value"])
            - self.inlet_TR["value"] * (self.compr_TR["value"] - 1)
        ) / (self.inlet_TR["value"] * (self.fan_TR["value"] - 1))
        self.Pt_out["value"] = self.Pt_in["value"] * self.PR["value"]
        self.P_out["value"] = self.Pt_out["value"] * (
            ((self.Tt_out["value"] / self.T_out["value"]) ** (y / (y - 1))) ** -1
        )
        self.W_in["value"] = self.inlet_W_in["value"] / (1 + self.BPR["value"])
        self.W_fan["value"] = self.inlet_W_in["value"] - self.W_in["value"]
        self.Wf["value"] = self.burner_f["value"] * self.W_in["value"]
        self.W_out["value"] = self.W_in["value"] + self.Wf["value"]

        self.Pt_out["units"] = self.Pt_in["units"]
        self.Tt_out["units"] = self.Tt_in["units"]
        self.T_out["units"] = self.Tt_out["units"]
        self.P_out["units"] = self.Pt_out["units"]
        self.a_out["units"] = "m/s"
        self.W_in["units"] = "kg/s"
        self.W_fan["units"] = self.W_in["units"]
        self.Wf["units"] = self.W_in["units"]
        self.W_out["units"] = self.W_in["units"]

    def __str__(self):
        output = (
            f"{self.name} Characteristics:\n Temperature Ratio: {self.TR}\n Bypass Ratio: {self.BPR}\n Mach at exit: {self.XMN_out}\n Core mass flow rate: {self.W_core}\n Fuel mass flow rate: {self.W_f}\n Fan mass flow rate: {self.W_fan}"
            f"Efficiency:\n Polytropic Efficiency: {self.eff_poly}\n Mechanical Efficiency: {self.eff_mech}\n"
            f" Pressure Ratio: {self.PR}"
        )
        return output
