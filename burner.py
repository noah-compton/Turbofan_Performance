# Date    | Description of Changes:                          | Author
# ----------------------------------------------------------------------------

from methods import check_units

class Burner:
    def __init__(self, **kwargs):
        
        init = {'value': float, 'units': str}
        
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
        self.PR         = init.copy()
        self.TR         = init.copy()
        self.TRmax      = init.copy()
        self.eff_mech   = init.copy()
        self.eff_poly   = init.copy()
        self.eff_isen   = init.copy()
        self.FAR        = init.copy()
        
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
                    self.Pt_in['units'] = 'Pa'
                    raise Warning("Pt_in has not enough inputs, assuming kPa for units")   
                
            elif property == "Tt_in":
                self.Tt_in['value'] = value 
                
                if len(values) < 2:
                    self.Tt_in['units'] = "K"
                    raise Warning("Tt_in has not enough inputs, assuming K for units")   
            
                
            elif property == "W_in":
                self.W_in['value'] = value 
                
                if len(values) < 2:
                    self.W_in['units'] = "lbm/s"
                    raise Warning("W_in has not enough inputs, assuming lbm/s for units")   
            
            elif property == "Wf":
                self.Wf['value'] = value 
                
                if len(values) < 2:
                    self.Wf['units'] = "lbm/hr"
                    raise Warning("Wf has not enough inputs, assuming lbm/hr for units")   
            
            elif property == "Tt_out":
                self.Tt_out['value'] = value 
                
                if len(values) < 2:
                    self.Tt_out['units'] = "K"
                    raise Warning("Tt_in has not enough inputs, assuming K for units")   
                        
            elif property == "PR":
                self.PR['value'] = value 
                
                if len(values) < 2:
                    self.PR['units'] = "-"
                    raise Warning("PR has not enough inputs, assuming value is dimensionless")        

            elif property == "TR":
                self.TR['value'] = value 
                
                if len(values) < 2:
                    self.TR['units'] = "-"
                    raise Warning("TR has not enough inputs, assuming value is dimensionless")     
                    
            elif property == "eff_mech":
                self.eff_mech['value'] = value 
                
                if len(values) < 2:
                    self.eff_mech['units'] = "-"
                    raise Warning("e has not enough inputs, assuming value is dimensionless")        
                             
            elif property == "name":
                self.name = values

    # Methods
    def temperature_ratio(self):
        if self.Tt_out['units'] == self.Tt_in['units']:
            dTt = self.Tt_out['value'] - self.Tt_in['value']
            
            if self.Tt_out['value'] > 0 and self.Tt_in['value'] > 0:
                    self.TR['value'] = self.Tt_out['value'] / self.Tt_in['value']
       
    def fuel_to_air_ratio(self):
        y = 1.4        # This can go away by adding the air as inlet fluid
        cp = 1004      # This can go away by adding the air as inlet fluid
        Q = 42800000   # This can go away by adding the air as inlet fluid
        
        check_units(self.Tt_in, self.Tt_out)
        self.FAR['value'] = cp * (self.Tt_out['value'] - self.Tt_in['value']) / (Q*self.eff_mech['value'] - cp*self.Tt_out['value'])
    
    def fuel_flow(self):
        self.Wf['value'] = self.W_in['value'] * self.FAR['value']
        self.Wf['units'] = self.W_in['units']
        
    def max_temperature_ratio(self, T0):
        check_units(self.Tt_out, T0)
        self.TRmax['value'] = self.Tt_out['value'] / T0['value']
        self.TRmax['units'] = '-'
    
    def mass_conservation(self):
        check_units(self.W_in, self.Wf)
        self.W_out['value'] = self.W_in['value'] + self.Wf['value']
        self.W_out['units'] = self.W_in['units']
        
    def calc(self, T0):
        # Calculate TR
        self.temperature_ratio()

        # Calculate FAR
        self.fuel_to_air_ratio()
        
        # Calculate TRmax
        self.max_temperature_ratio(T0)

        # Calculate Fuel Flow
        self.fuel_flow()

        # Conservation
        self.mass_conservation()

        self.Pt_out['value'] = self.PR['value'] * self.Pt_in['value']
        self.Pt_out['units'] = self.Pt_in['units']

        if self.Tt_out == 0: 
            self.Tt_out['value'] = self.TR['value'] * self.Tt_in['value']
            self.Tt_out['units'] = self.Tt_in['units']     

    
    def __str__(self): 
        str = f"{self.name} Characteristics:\n" \
              f"Efficiency:\n" \
              f"Pressure Ratio:\n"
        return str