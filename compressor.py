# Date    | Description of Changes:                          | Author
# ----------------------------------------------------------------------------
# Dec 1   | First compressor class working                   | Jose R.
#         | Need to incorporate gas_dynamics package         |
#         | Update __str__ definition                        |
# ----------------------------------------------------------------------------
# Nov 30  | Initial .py file on GitHub                       | Jose R.
import math
import gas_dynamics as gd
import pdb

class Compressor:
    '''
    class Compressor(**kwargs) has attributes to store typical compressor performance parameters, or parameteres needed to make typical compressor calculations, 
    and it can be modified to input and output different parameters, depending on the simulation that is desired to run.

    Input:
    Compressor will take varios compressor typical inlet parameters, such as total and static conditions of the flow as Pt_in, Tt_in, and W_in, 
    as well as performance characterization like eff_poly, eff_mech, and eff_isen for Polytropic, Mechanical and Isentropic Efficiencies.

    Output:
    Compressor will output downstream (or discharge) conditions, such as Pt_out, Tt_out and W_out
    '''

    '''
    Examples:
    Ex1: Direct Assigment:
    Cmp20 = Compressor(name='Cmp20', Pt_in ={'value': 101.325, 'units': 'kPa}, Tt_in = {'value': 288.15, 'units': 'K'})
    
    Ex2: Initializing, then assignment of values:
    Cmp20 = Compressor()
    Cmp20.name  =  'Cmp20'
    Cmp20.Pt_in = {'value': 101.325 , 'units': 'kPa} 
    Cmp20.Tt_in = {'value': 288.15  , 'units': 'K' }
    '''

    def __init__(self, **kwargs):

        init = {"value": 0.0, "units": "-"}
        
        cmp_vars = [
                      'name'     , 'inlet'    , 'outlet'   , 
                      'Pt_in'    , 'Tt_in'    , 'W_in'     , 
                      'Pt_out'   , 'Tt_out'   , 'W_out'    , 
                      'PR'       , 'TR'       , 'N_mech'   ,
                      'eff_poly' , 'eff_mech' , 'eff_isen' ,
                      ]
        
        # Indicators
        self.name = ""
        self.inlet = ""
        self.outlet = ""

        # Inlet
        self.Pt_in    = init.copy()
        self.Tt_in    = init.copy()
        self.W_in     = init.copy()

        # Outlet
        self.Pt_out   = init.copy()
        self.Tt_out   = init.copy()
        self.W_out    = init.copy()

        # Characteristics
        self.PR       = init.copy()
        self.TR       = init.copy()
        self.N_mech   = init.copy()
        
        # Efficiencies
        self.eff_poly = init.copy()
        self.eff_mech = init.copy()
        self.eff_isen = init.copy()

        interested = [
                      'name'     , 'inlet'    , 'outlet'   , 
                      'Pt_in'    , 'Tt_in'    , 'W_in'     , 
                      'Pt_out'   , 'Tt_out'   , 'W_out'    , 
                      'PR'       , 'TR'       , 'N_mech'   ,
                      'eff_poly' , 'eff_mech' , 'eff_isen' ,
                      ]

        for cmp_in in kwargs:

            values = kwargs[cmp_in]
            
            if cmp_in == 'name':
                continue
            
            elif len(values) == 2:
                value = values['value']
                units = values['units']

            elif len(values) < 1:
                raise ValueError("Input is missing value or units")
                
            elif len(values) > 2:
                raise ValueError("Input has more than one value or units")
            

            if cmp_in == 'name':
                self.name = values

            elif cmp_in in cmp_vars:
                exp1 = f"self.{cmp_in}['value'] = value"
                exp2 = f"self.{cmp_in}['units'] = units"

                exec(exp1)                
                exec(exp2)

            else:
                raise Warning("Some inputs were not expected, ignoring extra inputs")


    def temperature_ratio(self):
        '''
        function temperature_ratio() check input of the compressor to calculate one of the following: pressure ratio, 
        temperature ratio or polytropic efficiency.
        '''
        # Working fluid:
        air = gd.fluid('air', gamma=1.4, R=287, units ='J/kg-K')
        
        y = air.gamma
        R = air.R
        
        if self.PR['value'] > 0. and self.TR['value'] > 0.:
            self.eff_poly['value'] = ((y-1)/y) * (math.log(self.PR['value'])/ math.log(self.TR['value']))
            self.eff_poly['units'] = '-'
        
        elif self.PR['value'] > 0. and self.eff_poly['value'] > 0.:
            self.TR['value'] = self.PR['value']**((y-1)/(y*self.eff_poly['value']))
            self.TR['units'] = '-'       
       
        elif self.TR['value'] > 0. and self.eff_poly['value'] > 0.:        
            self.PR['value'] = self.TR['value']**((y*self.eff_poly['value'])/(y-1))
            self.PR['units'] = '-'

        else:
            raise ValueError(
                "Not enough compressor characteristics were defined, check input"
            )

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
        # self.discharge_pressure()
        self.discharge_temperature()
        self.mass_conservation()
        
    def __str__(self):
        out = f"Compressor: {self.name}\n \
                Polytropic Efficiency: {self.eff_poly}\n \
                Isentropic Efficiency: {self.eff_isen}\n \
                Pressure Ratio: {self.PR}"

        return out
