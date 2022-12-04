# fan
# Isabel H
# need to define __str__

import gas_dynamics as gd

global y
y = gd.fluids.air.gamma


class Fan:
    def __init__(self, **kwargs):
        init = {"value": 0.0, "unit": "-"}

        self.name = ""

        # Inlet
        self.Pt_in = init.copy()
        self.Tt_in = init.copy()
        # Outlet
        self.Pt_13 = init.copy()
        self.Tt_13 = init.copy()
        self.Pt_15 = init.copy()
        self.Tt_15 = init.copy()
        # Characteristics
        self.T_f = init.copy()
        self.Pi_f = init.copy()
        self.ef = init.copy()

        for property in kwargs:

            values = kwargs[property]

            if len(values) >= 2:
                value = values[0]
                unit = values[1]

            elif len(values) == 1:
                value = values[0]
                unit = ""

            else:
                raise ValueError("Not enough inputs")

            if property == "Pt_in":
                self.P0["value"] = value

                if len(values) == 2:
                    self.P0["unit"] = unit

                elif len(values) < 2:
                    self.P0["unit"] = "Pa"
                    raise Warning("Not enough inputs: assuming Pa for units for Pt_in")

            elif property == "Tt_in":
                self.T0["value"] = value

                if len(values) == 2:
                    self.T0["unit"] = unit

                elif len(values) < 2:
                    self.T0["unit"] = "K"
                    raise Warning("Not enough inputs: assuming K for units for Tt_in ")

            elif property == "T_f":
                self.T0["value"] = value

                if len(values) == 2:
                    self.T0["unit"] = unit

                elif len(values) < 2:
                    self.T0["unit"] = ""
                    raise Warning("Not enough inputs: assuming dimensionless parameter")

            elif property == "Pi_f":
                self.T0["value"] = value

                if len(values) == 2:
                    self.T0["unit"] = unit

                elif len(values) < 2:
                    self.T0["unit"] = ""
                    raise Warning("Not enough inputs: assuming dimensionless parameter")

            elif property == "ef":
                self.T0["value"] = value

                if len(values) == 2:
                    self.T0["unit"] = unit

                elif len(values) < 2:
                    self.T0["unit"] = ""
                    raise Warning("Not enough inputs: assuming dimensionless parameter")

            elif property == "name":
                self.name = values

    def calc(self):
        if self.Pt_in["value"] > 0 and self.Tt_in["value"] > 0:
            pass
        else:
            raise ValueError(
                "Incorrect inputs for inlet: nonzero values required for Pt_in and Tt_in"
            )

        # values
        self.T_f["value"] = self.Pi_f["value"] ** ((y - 1) / (y * self.ef["value"]))
        self.Pt_13["value"] = self.Pi_f["value"] * self.Pt_in["value"]
        self.Tt_13["value"] = self.T_f["value"] * self.Tt_in["value"]
        self.Pt_15["value"] = self.Pt_13["value"]
        self.Tt_15["value"] = self.Tt_13["value"]

        # units
        self.T_f["unit"] = ""
        self.Pt_13["unit"] = "Pa"
        self.Tt_13["unit"] = "K"
        self.Pt_15["unit"] = "Pa"
        self.Tt_15["unit"] = "K"

    def __str__(self):
        str = f"{self.name} Characteristics:\n"
