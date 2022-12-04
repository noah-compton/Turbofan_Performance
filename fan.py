#fan
# Isabel H
# need to define __str__

import gas_dynamics as gd

global y
y = gd.fluids.air.gamma

class Fan:
    def __init__(self, **kwargs):
        init = {'value': 0., 'unit': '-'}
        
        self.name   = ''
    
        #Inlet
        self.Pt_in = init.copy()
        self.Tt_in = init.copy()
        #Outlet
        self.Pt_13 = init.copy()
        self.Tt_13 = init.copy()
        #Characteristics
        self.TR = init.copy()    # TR
        self.PR = init.copy()   # PR
        self.eff_poly = init.copy()     # eff_poly

        for property in kwargs:

            values = kwargs[property]

            if len(values) >= 2:
                value = values[0]
                unit = values[1]
                
            elif len(values) == 1:
                value = values[0]
                unit = ''
            
            else:
                raise ValueError('Not enough inputs')

            
            if property == "Pt_in":
                self.Pt_in['value'] = value

                if len(values) == 2:
                    self.Pt_in["unit"] = unit

                elif len(values) < 2:
                    self.Pt_in['unit'] = 'Pa'
                    raise Warning("Not enough inputs: assuming Pa for units for Pt_in")
            
            elif property == "Tt_in":
                 self.Tt_in["value"] = value

                 if len(values) == 2:
                    self.Tt_in["unit"] = unit

                 elif len(values) < 2:
                        self.Tt_in["unit"] = "K"
                        raise Warning("Not enough inputs: assuming K for units for Tt_in ")
            
            elif property == "TR":
                 self.TR["value"] = value

                 if len(values) == 2:
                    self.TR["unit"] = unit

                 elif len(values) < 2:
                        self.TR["unit"] = ""
                        raise Warning("Not enough inputs: assuming dimensionless parameter")
            
            elif property == "PR":
                 self.PR["value"] = value

                 if len(values) == 2:
                    self.PR["unit"] = unit

                 elif len(values) < 2:
                        self.PR["unit"] = ""
                        raise Warning("Not enough inputs: assuming dimensionless parameter")
            
            elif property == "eff_poly":
                 self.eff_poly["value"] = value

                 if len(values) == 2:
                    self.eff_poly["unit"] = unit

                 elif len(values) < 2:
                        self.eff_poly["unit"] = ""
                        raise Warning("Not enough inputs: assuming dimensionless parameter")

           
            elif property == "name":
                self.name = values
    
    def calc(self):
        if self.Pt_in["value"] > 0 and self.Tt_in["value"] > 0:
             pass
        else:
             raise ValueError("Incorrect inputs for inlet: nonzero values required for Pt_in and Tt_in")
        
        #values
        self.TR["value"] = (self.PR["value"] ** ((y - 1)/(y*self.ef["value"])))
        self.Pt_13["value"] = self.PR["value"] * self.Pt_in["value"]
        self.Tt_13["value"] = self.TR["value"] * self.Tt_in["value"]

        #units
        self.TR["unit"] =''
        self.Pt_13["unit"] = 'Pa'
        self.Tt_13["unit"] = 'K'

    def __str__(self):
        str = f"{self.name} Characteristics:\n"
        
