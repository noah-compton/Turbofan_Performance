# Date    | Description of Changes:                          | Author
# ----------------------------------------------------------------------------

import pdb

class Burner:
    def __init__(self, **kwargs):
        
        init = {'value': 0., 'unit': '-'}
        
        self.name   = ''
        self.inlet = ''
        self.outlet = ''
        
        # Inlet
        self.Pt_in  = init.copy()
        self.Tt_in  = init.copy()
        self.W_in   = init.copy()
        self.Wf     = init.copy()

        # Outlet
        self.Pt_out = init.copy()
        self.Tt_out = init.copy()
        self.W_out  = init.copy()
         
        # Characteristics
        self.PR     = init.copy()
        self.TR     = init.copy()
        self.TRmax  = init.copy()
        self.e      = init.copy()
        self.f      = init.copy()
        
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
                
                if len(values) < 2:
                    self.Pt_in['unit'] = 'Pa'
                    raise Warning("Pt_in has not enough inputs, assuming kPa for units")   
                
            elif property == "Tt_in":
                self.Tt_in['value'] = value 
                
                if len(values) < 2:
                    self.Tt_in['unit'] = "K"
                    raise Warning("Tt_in has not enough inputs, assuming K for units")   
            
                
            elif property == "W_in":
                self.W_in['value'] = value 
                
                if len(values) < 2:
                    self.W_in['unit'] = "lbm/s"
                    raise Warning("W_in has not enough inputs, assuming lbm/s for units")   
            
            elif property == "Wf":
                self.Wf['value'] = value 
                
                if len(values) < 2:
                    self.Wf['unit'] = "lbm/hr"
                    raise Warning("Wf has not enough inputs, assuming lbm/hr for units")   
            
            elif property == "Tt_out":
                self.Tt_out['value'] = value 
                
                if len(values) < 2:
                    self.Tt_out['unit'] = "K"
                    raise Warning("Tt_in has not enough inputs, assuming K for units")   
                        
            elif property == "PR":
                self.PR['value'] = value 
                
                if len(values) < 2:
                    self.PR['unit'] = "-"
                    raise Warning("PR has not enough inputs, assuming value is dimensionless")        

            elif property == "TR":
                self.TR['value'] = value 
                
                if len(values) < 2:
                    self.TR['unit'] = "-"
                    raise Warning("TR has not enough inputs, assuming value is dimensionless")     
                    
            elif property == "e":
                self.e['value'] = value 
                
                if len(values) < 2:
                    self.e['unit'] = "-"
                    raise Warning("e has not enough inputs, assuming value is dimensionless")        
                             
            elif property == "name":
                self.name = values

    def calc(self):
        y = 1.4        # This can go away by adding the air as inlet fluid
        cp = 1004      # This can go away by adding the air as inlet fluid
        Q = 42800000   # This can go away by adding the air as inlet fluid
        T0 = 223       # This should be a global variable
        
        if self.Tt_out['unit'] == self.Tt_in['unit']:
            dTt = self.Tt_out['value'] - self.Tt_in['value']
            
            if self.Tt_out['value'] > 0 and self.Tt_in['value'] > 0:
                    self.TR['value'] = self.Tt_out['value'] / self.Tt_in['value']
       
        else:
            raise ValueError(f"Units not consistent, check Tt_out and Tt_in for {self.name}")
        
        self.f['value'] = cp * ( dTt ) / (Q*self.e['value'] - cp*self.Tt_out['value'])
        
        self.TRmax['value'] = self.Tt_out['value'] / T0
        self.TRmax['unit'] = '-'
        
        self.Pt_out['value'] = self.PR['value'] * self.Pt_in['value']
        self.Pt_out['unit'] = self.Pt_in['unit']

        if self.Tt_out == 0: 
            self.Tt_out['value'] = self.TR['value'] * self.Tt_in['value']
            self.Tt_out['unit'] = self.Tt_in['unit']     


    def __str__(self): 
        str = f"{self.name} Characteristics:\n" \
              f"Efficiency:\n" \
              f"Pressure Ratio:\n"
        return str