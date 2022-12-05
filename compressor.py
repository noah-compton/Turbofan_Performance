# Date    | Description of Changes:                          | Author
# ----------------------------------------------------------------------------
# Dec 1   | First compressor class working                   | Jose R.
#         | Need to incorporate gas_dynamics package         |
#         | Update __str__ definition                        |
# ----------------------------------------------------------------------------
# Nov 30  | Initial .py file on GitHub                       | Jose R.

class Compressor:
    def __init__(self, **kwargs):

        init = {"value": 0.0, "units": "-"}

        self.name = ""
        self.inlet = ""
        self.outlet = ""

        # Inlet
        self.Pt_in     = init.copy()
        self.Tt_in     = init.copy()
        self.W_in      = init.copy()

        # Outlet
        self.Pt_out    = init.copy()
        self.Tt_out    = init.copy()
        self.W_out     = init.copy()
         
        # Characteristics
        self.PR        = init.copy()
        self.TR        = init.copy()
        self.eff_poly  = init.copy()
        
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

            elif property == "e":
                self.eff_poly['value'] = value 
                
                if len(values) == 2:
                    self.eff_poly['units']  = units
                    
                if len(values) < 2:
                    self.eff_poly['units'] = "-"
                    raise Warning("e has not enough inputs, assuming value is dimensionless")        
                             
            elif property == "name":
                self.name = values

    # Methods
    def poly_efficiency(self):
        y = 1.4

        self.eff_poly['value'] = ((y-1)/y) * (math.log(self.PR['value'])/ math.log(self.TR['value']))
        self.eff_poly['units'] = '-'
    
    def temperature_ratio(self):
        y = 1.4

        self.TR['value'] = self.PR['value']**((y-1)/(y*self.eff_poly['value']))
        self.TR['units'] = '-'    

    def pressure_ratio(self):
        y = 1.4
        
        self.PR['value'] = self.TR['value']**((y*self.eff_poly['value'])/(y-1))
        self.PR['units'] = '-'
        
    def discharge_pressure(self):
        self.Pt_out["value"] = self.PR["value"] * self.Pt_in["value"]
        self.Pt_out["units"] = self.Pt_in["units"]
        
    def discharge_temperature(self):
        self.Tt_out["value"] = self.TR["value"] * self.Tt_in["value"]
        self.Tt_out["units"] = self.Tt_in["units"]
    
    def mass_conservation(self):
        self.W_out["value"]  = self.W_in["value"]
        self.W_out["units"]  = self.W_in["units"]
        
    # Calculations
    def calc(self):
        
        self.temperature_ratio()
        self.discharge_pressure()
        self.discharge_temperature()
        self.mass_conservation()
        
    def __str__(self):
        str = f"{self.name} Characteristics:\n" f"Efficiency:\n" f"Pressure Ratio:\n"
        return str


