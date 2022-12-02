# Date    | Description of Changes:                          | Author
# ----------------------------------------------------------------------------
# Dec 1   | First compressor class working                   | Jose R.
#         | Need to incorporate gas_dynamics package         |
#         | Update __str__ definition                        |
# ----------------------------------------------------------------------------
# Nov 30  | Initial .py file on GitHub                       | Jose R. 

import math
import pdb

class Compressor:
    def __init__(self, **kwargs):
        
        init = {'value': 0., 'unit': '-'}
        
        self.name   = ''
        
        # Inlet
        self.Pt_in  = init.copy()
        self.Tt_in  = init.copy()
        self.W_in   = init.copy()

        # Outlet
        self.Pt_out = init.copy()
        self.Tt_out = init.copy()
        self.W_out  = init.copy()
         
        # Characteristics
        self.PR     = init.copy()
        self.TR     = init.copy()
        self.e      = init.copy()
        
        for property in kwargs:
            
            values = kwargs[property]
            
            
            if len(values) >= 2:
                value = values[0]
                unit = values[1]
                
                if len(values) > 2 and property != 'name':
                    raise Warning(f"Property {property} had too many inputs, using first 2 provided")
                
            elif len(values) == 1:
                value = values[0]
                unit = ''
            
            else:
                raise ValueError('Not enough inputs')
                

            if property == "Pt_in":
                self.Pt_in['value'] = value
                
                
                if len(values) == 2:
                    self.Pt_in['unit']  = unit
                    
                elif len(values) < 2:
                    self.Pt_in['unit'] = 'Pa'
                    raise Warning("Pt_in has not enough inputs, assuming kPa for units")   
                
            elif property == "Tt_in":
                self.Tt_in['value'] = value
                
                if len(values) == 2:
                    self.Tt_in['unit']  = unit
                    
                if len(values) < 2:
                    self.Tt_in['unit'] = "K"
                    raise Warning("Tt_in has not enough inputs, assuming K for units")   
                
            elif property == "W_in":
                self.W_in['value'] = value 
                
                if len(values) == 2:
                    self.W_in['unit']  = unit
                    
                if len(values) < 2:
                    self.W_in['unit'] = "lbm/s"
                    raise Warning("W_in has not enough inputs, assuming lbm/s for units")   

            elif property == "PR":
                self.PR['value'] = value 
                
                if len(values) == 2:
                    self.PR['unit']  = unit
                    
                if len(values) < 2:
                    self.PR['unit'] = "-"
                    raise Warning("PR has not enough inputs, assuming value is dimensionless")        

            elif property == "TR":
                self.TR['value'] = value 
                
                if len(values) == 2:
                    self.TR['unit']  = unit
                    
                if len(values) < 2:
                    self.TR['unit'] = "-"
                    raise Warning("TR has not enough inputs, assuming value is dimensionless")     
                    
            elif property == "e":
                self.e['value'] = value 
                
                if len(values) == 2:
                    self.e['unit']  = unit
                    
                if len(values) < 2:
                    self.e['unit'] = "-"
                    raise Warning("e has not enough inputs, assuming value is dimensionless")        
                             
            elif property == "name":
                self.name = values
    
    def calc(self):
        y = 1.4
        
        if self.PR['value'] > 0. and self.TR['value'] > 0.:
            self.e['value'] = ((y-1)/y) * (math.log(self.PR['value'])/ math.log(self.TR['value']))
            self.e['unit'] = '-'
        
        elif self.PR['value'] > 0. and self.e['value'] > 0.:
            self.TR['value'] = self.PR['value']**((y-1)/(y*self.e['value']))
            self.TR['unit'] = '-'       
       
        elif self.TR['value'] > 0. and self.e['value'] > 0.:        
        # elif hasattr(self, 'TR['value']') and hasattr(self, "e['value']"):
            self.PR['value'] = self.TR['value']**((y*self.e['value'])/(y-1))
            self.PR['unit'] = '-'

        else:
            raise ValueError("Not enough compressor characteristics were defined, check input")
        
    
        self.Pt_out['value'] = self.PR['value'] * self.Pt_in['value']
        self.Tt_out['value'] = self.TR['value'] * self.Tt_in['value']
        self.W_out['value']  = self.W_in['value']
        
        self.Pt_out['unit'] = self.Pt_in['unit']
        self.Tt_out['unit'] = self.Tt_in['unit']     
        self.W_out['unit']  = self.W_in['unit']

        
    def __str__(self): 
        str = f"{self.name} Characteristics:\n" \
              f"Efficiency:\n" \
              f"Pressure Ratio:\n"
        return str


