# Date    | Description of Changes:                          | Author
# ----------------------------------------------------------------------------

from processes import check_units
import gas_dynamics as gd
import pdb

class Burner:    
    '''
    class Burner(**kwargs) has attributes to store typical burner performance parameters, or parameteres needed to make typical burner calculations, 
    and it can be modified to input and output different parameters, depending on the simulation that is desired to run.

    Input:
    Burner will take varios compressor typical inlet parameters, such as total and static conditions of the flow as Pt_in, Tt_in, and W_in, 
    as well as performance characterization like eff_poly, eff_mech, and eff_isen for Polytropic, Mechanical and Isentropic Efficiencies.

    Output:
    Burner will output downstream (or discharge) conditions, such as Pt_out, Tt_out and W_out
    and other parameters like Fuel-to-Air Ratio (FAR)
    '''

    '''
    Examples:
    Ex1: Direct Assigment:
    Brn30 = Burner(name='Brn30', Pt_in ={'value': 101.325, 'units': 'kPa}, Tt_in = {'value': 288.15, 'units': 'K'})
    
    Ex2: Initializing, then assignment of values:
    Brn30 = Burner()
    Brn30.name  =  'Brn30'
    Brn30.Pt_in = {'value': 101.325 , 'units': 'kPa} 
    Brn30.Tt_in = {'value': 288.15  , 'units': 'K' }
    '''
    
    def __init__(self, **kwargs):
        
        init = {'value': 0., 'units': '-'}
        
        brn_vars = [
                      'name'     , 'inlet'    , 'outlet'   , 
                      'Pt_in'    , 'Tt_in'    , 'W_in'     , 
                      'Pt_out'   , 'Tt_out'   , 'W_out'    , 
                      'PR'       , 'TR'       , 'TRmax'    ,
                      'eff_poly' , 'eff_mech' , 'eff_isen' ,
                      'FAR'      ,
                      ]
        
        # Indicators
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
        self.FAR        = init.copy()
        
        # Efficiencies
        self.eff_mech   = init.copy()
        self.eff_poly   = init.copy()
        self.eff_isen   = init.copy()
        
        for brn_in in kwargs:
           
            values = kwargs[brn_in]
            
            if brn_in == 'name':
                continue
            
            elif len(values) == 2:
                value = values['value']
                units = values['units']

            elif len(values) < 1:
                raise ValueError("Input is missing value or units")
                
            elif len(values) > 2:
                raise ValueError("Input has more than one value or units")
            

            if brn_in == 'name':
                self.name = values

            elif brn_in in brn_vars:
                exp1 = f"self.{brn_in}['value'] = value"
                exp2 = f"self.{brn_in}['units'] = units"

                exec(exp1)                
                exec(exp2)

            else:
                raise Warning("Some inputs were not expected, ignoring extra inputs")

            # values = kwargs[brn_in]
            
            # if len(values) >= 2:
            #     value = values[0]
            #     unit = values[1]
                
            # elif len(values) == 1:
            #     value = values[0]
            #     unit = ''
            
            # else:
            #     raise ValueError('Not enough inputs')
                

            # if brn_in == "Pt_in":
            #     self.Pt_in['value'] = value 
                
            #     if len(values) < 2:
            #         self.Pt_in['units'] = 'Pa'
            #         raise Warning("Pt_in has not enough inputs, assuming kPa for units")   
                
            # elif brn_in == "Tt_in":
            #     self.Tt_in['value'] = value 
                
            #     if len(values) < 2:
            #         self.Tt_in['units'] = "K"
            #         raise Warning("Tt_in has not enough inputs, assuming K for units")   
            
                
            # elif brn_in == "W_in":
            #     self.W_in['value'] = value 
                
            #     if len(values) < 2:
            #         self.W_in['units'] = "lbm/s"
            #         raise Warning("W_in has not enough inputs, assuming lbm/s for units")   
            
            # elif brn_in == "Wf":
            #     self.Wf['value'] = value 
                
            #     if len(values) < 2:
            #         self.Wf['units'] = "lbm/hr"
            #         raise Warning("Wf has not enough inputs, assuming lbm/hr for units")   
            
            # elif brn_in == "Tt_out":
            #     self.Tt_out['value'] = value 
                
            #     if len(values) < 2:
            #         self.Tt_out['units'] = "K"
            #         raise Warning("Tt_in has not enough inputs, assuming K for units")   
                        
            # elif brn_in == "PR":
            #     self.PR['value'] = value 
                
            #     if len(values) < 2:
            #         self.PR['units'] = "-"
            #         raise Warning("PR has not enough inputs, assuming value is dimensionless")        

            # elif brn_in == "TR":
            #     self.TR['value'] = value 
                
            #     if len(values) < 2:
            #         self.TR['units'] = "-"
            #         raise Warning("TR has not enough inputs, assuming value is dimensionless")     
                    
            # elif brn_in == "eff_mech":
            #     self.eff_mech['value'] = value 
                
            #     if len(values) < 2:
            #         self.eff_mech['units'] = "-"
            #         raise Warning("e has not enough inputs, assuming value is dimensionless")        
                             
            # elif brn_in == "name":
            #     self.name = values

    # processes
    def temperature_ratio(self):
        if self.Tt_out['units'] == self.Tt_in['units']:
            dTt = self.Tt_out['value'] - self.Tt_in['value']
            
            if self.Tt_out['value'] > 0 and self.Tt_in['value'] > 0:
                    self.TR['value'] = self.Tt_out['value'] / self.Tt_in['value']
       
    def fuel_to_air_ratio(self):
        # Working fluids:
        air  = gd.fluid('air' , gamma=1.4, R=287, units ='J/kg-K')
        
        cp = 1004
        y = air.gamma
        R = air.R
        
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
        out = f"Burner: {self.name}\n \
                Mechanical Efficiency: {self.eff_mech}\n \
                Fuel-to-Air Ratio: {self.FAR}\n \
                Pressure Ratio: {self.PR}"

        return out