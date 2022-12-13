class Bypass:
    def __init__(self, **kwargs):

        init = {"value": 0., "units": '-'}

        self.name = ""
        self.inlet = ""
        self.outlet = ""

        # Inlet
        self.Pt_in   = init.copy()
        self.P_in    = init.copy()
        self.Tt_in   = init.copy()
        self.T_in    = init.copy()
        self.W_in    = init.copy()
        self.XMN_in  = init.copy()

        # Outlet
        self.Pt_out   = init.copy()
        self.P_out    = init.copy()
        self.Tt_out   = init.copy()
        self.T_out    = init.copy()
        self.W_out    = init.copy()
        self.XMN_out  = init.copy()

        # Characteristics
        self.PR = init.copy()
        self.TR = init.copy()

        for property in kwargs:
            values = kwargs[property]

            if len(values) >= 2:
                value = values[0]
                units = values[1]

                if len(values) > 2 and property != "name":
                    raise Warning(
                        f"Property {property} had too many inputs, using first 2 provided"
                    )

            elif len(values) == 1:
                value = values[0]
                units = ""

            else:
                raise ValueError("Not enough inputs")

            if property == "Pt_in":
                self.Pt_in["value"] = value

                if len(values) == 2:
                    self.Pt_in["units"] = units

                elif len(values) < 2:
                    self.Pt_in["units"] = "kPa"
                    raise Warning("Pt_in has not enough inputs, assuming kPa for units")

            elif property == "Tt_in":
                self.Tt_in["value"] = value

                if len(values) == 2:
                    self.Tt_in["units"] = units

                if len(values) < 2:
                    self.Tt_in["units"] = "K"
                    raise Warning("Tt_in has not enough inputs, assuming K for units")

            elif property == "W_in":
                self.W_in["value"] = value

                if len(values) == 2:
                    self.W_in["units"] = units

                if len(values) < 2:
                    self.W_in["units"] = "lbm/s"
                    raise Warning(
                        "W_in has not enough inputs, assuming lbm/s for units"
                    )

            elif property == "PR":
                self.PR["value"] = value

                if len(values) == 2:
                    self.PR["units"] = units

                if len(values) < 2:
                    self.PR["units"] = "-"
                    raise Warning(
                        "PR has not enough inputs, assuming value is dimensionless"
                    )

            elif property == "TR":
                self.TR["value"] = value

                if len(values) == 2:
                    self.TR["units"] = units

                if len(values) < 2:
                    self.TR["units"] = "-"
                    raise Warning(
                        "TR has not enough inputs, assuming value is dimensionless"
                    )

            elif property == "eff_poy":
                self.eff_poly["value"] = value

                if len(values) == 2:
                    self.eff_poly["units"] = units

                if len(values) < 2:
                    self.eff_poly["units"] = "-"
                    raise Warning(
                        "e has not enough inputs, assuming value is dimensionless"
                    )

            elif property == "name":
                self.name = values

    # Methods
    def mass_conservation(self):
        self.W_out["value"]  = self.W_in["value"]
        self.W_out["units"]  = self.W_in["units"]
    
    def energy_conservation(self):
        self.Tt_out["value"]  = self.Tt_in["value"]
        self.Tt_out["units"]  = self.Tt_in["units"]
    
    # Calculations
    def calc(self):
        
        self.mass_conservation()
        self.energy_conservation()
        
    def __str__(self):
        str = f"{self.name} Characteristics:\n" f"Efficiency:\n" f"Pressure Ratio:\n"
        return str
