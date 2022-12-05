# inlet/flight conditions calculations
# Isabel H
# need to define __str__

import gas_dynamics as gd
import math


# establish y = 1.4, R, as global variables using gd package
global y
y = gd.fluids.air.gamma

global R
R = gd.fluids.air.R


class Inlet:
    def __init__(self, **kwargs):

        init = {"value": 0.0, "units": "-"}

        self.name = ""
        self.inlet = ""
        self.outlet = ""

        # Inlet
        self.P_in = init.copy()
        self.T_in = init.copy()
        self.XMN_in = init.copy()
        self.W_in = init.copy()

        # Outlet
        self.Pt_in = init.copy()
        self.Tt_in = init.copy()
        self.a_in = init.copy()  # a_in
        self.u_in = init.copy()  # u_in
        self.Tt_out = init.copy()
        self.Pt_out = init.copy()
        self.W_out = init.copy()

        # Characteristics
        self.PR = init.copy()
        self.TR = init.copy()

        for property in kwargs:

            values = kwargs[property]

            if len(values) >= 2:
                value = values[0]
                units = values[1]

            elif len(values) == 1:
                value = values[0]
                units = ""

            else:
                raise ValueError("Not enough inputs")

            if property == "P_in":
                self.P_in["value"] = value

                if len(values) == 2:
                    self.P_in["units"] = units

                elif len(values) < 2:
                    self.P_in["units"] = "Pa"
                    raise Warning("Not enough inputs: assuming Pa for units for P_in")

            elif property == "T_in":
                self.T_in["value"] = value

                if len(values) == 2:
                    self.T_in["units"] = units

                elif len(values) < 2:
                    self.T_in["units"] = "K"
                    raise Warning("Not enough inputs: assuming K as units for T_in.")

            elif property == "XMN_in":
                self.XMN_in["value"] = value

                if len(values) == 2:
                    self.XMN_in["units"] = units

                elif len(values) < 2:
                    self.XMN_in["units"] = ""
                    raise Warning(
                        "Not enough inputs: assuming dimensionless parameter."
                    )

            elif property == "W_in":
                self.W_in["value"] = value

                if len(values) == 2:
                    self.W_in["units"] = units

                elif len(values) < 2:
                    self.W_in["units"] = "kg/s"
                    raise Warning("Not enough inputs: assuming kg/s as units for m2.")

            elif property == "PR":
                self.PR["value"] = value

                if len(values) == 2:
                    self.PR["units"] = units

                elif len(values) < 2:
                    self.PR["units"] = ""
                    raise Warning(
                        "Not enough inputs: assuming dimensionless parameter."
                    )

            elif property == "name":
                self.name = values

    def calc(self):
        if (
            self.T_in["value"] > 0
            and self.P_in["value"] > 0
            and self.XMN_in["value"] > 0
            and self.W_in["value"] > 0
        ):
            pass
        else:
            raise ValueError(
                "Incorrect inputs for inlet: nonzero values required for P0, T0, M0, m2"
            )

        # calculate values
        self.a_in["value"] = math.sqrt(y * R * self.T_in["value"])
        self.u_in["value"] = self.XMN_in["value"] * self.a_in["value"]
        self.Tt_in["value"] = gd.stagnation_temperature(
            temperature=self.T_in["value"], mach=self.XMN_in["value"]
        )
        self.Pt_in["value"] = gd.stagnation_pressure(
            pressure=self.P_in["value"], mach=self.XMN_in["value"]
        )
        self.Tt_out["value"] = self.Tt_in["value"]
        self.TR["value"] = self.Tt_in["value"] / self.T_in["value"]
        self.Pt_out["value"] = self.Pt_in["value"] * self.PR["value"]
        self.W_out["value"] = self.W_in["value"]

        # units
        self.a_in["units"] = "m/s"
        self.u_in["units"] = "m/s"
        self.Tt_in["units"] = "K"
        self.Pt_in["units"] = "Pa"
        self.Tt_out["units"] = "K"
        self.Pt_out["units"] = "Pa"
        self.W_out["units"] = "kg/s"

    def __str__(self):
        str = f"{self.name} Characteristics:\n"
