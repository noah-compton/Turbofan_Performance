__author__ = "Jose M. Roque"
__version__ = "0.0.1"
__status__ = "Development"

from processes import *
import gas_dynamics as gd

class Mixer:
    '''
    class Mixer(**kwargs) has attributes to store typical mixer performance parameters, or parameteres needed to make typical mixer calculations, 
    and it can be modified to input and output different parameters, depending on the simulation that is desired to run.

    Input:
    Mixer will take varios mixer typical inlet parameters for the two strems mixing, such as total and static conditions of the flow as Pt_in, Tt_in, and W_in, 
    as well as performance characterization like eff_poly, eff_mech, and eff_isen for Polytropic, Mechanical and Isentropic Efficiencies.

    Output:
    Mixer will output downstream (or discharge) conditions of the mixed flow, such as Pt_out, Tt_out and W_out.
    '''

    '''
    Examples:
    Ex1: Direct Assigment:
    Mix50 = Burner(name='Mix50', Pt_in ={'value': 101.325, 'units': 'kPa}, Tt_in = {'value': 288.15, 'units': 'K'})
    
    Ex2: Initializing, then assignment of values:
    Mix50 = Burner()
    Mix50.name  =  'Mix50'
    Mix50.Pt_in = {'value': 101.325 , 'units': 'kPa} 
    Mix50.Tt_in = {'value': 288.15  , 'units': 'K' }
    '''

    def __init__(self, **kwargs):

        init = {"value": 0.0, "units": "-"}
        
        mix_vars = [
                      'name'   , 'inlet1' , 'inlet2'  , 'outlet' , 
                      'Pt_in1' , 'Tt_in1' , 'W_in1'   ,
                      'P_in1'  , 'T_in1'  , 'XMN_in1' ,
                      'Pt_in2' , 'Tt_in2' , 'W_in2'   ,
                      'P_in2'  , 'T_in2'  , 'XMN_in2' ,         
                      'Pt_out' , 'Tt_out' , 'W_out'   , 'Ht_out' ,
                      'P_out'  , 'T_out'  , 'XMN_out' ,        
                      'PR'     , 'PRi'    , 'PRm'     , 
                      'TR'     , 'AR'     , 'FAR'     ,
                      ]
        
        self.name = ""
        self.inlet1 = ""
        self.inlet2 = ""
        self.outlet = ""

        # Inlet1
        self.Pt_in1   = init.copy()
        self.Tt_in1   = init.copy()
        self.P_in1    = init.copy()
        self.T_in1    = init.copy()
        self.W_in1    = init.copy()
        self.XMN_in1  = init.copy()

        # Inlet2
        self.Pt_in2   = init.copy()
        self.Tt_in2   = init.copy()
        self.P_in2    = init.copy()
        self.T_in2    = init.copy()
        self.W_in2    = init.copy()
        self.XMN_in2  = init.copy()

        # Outlet
        self.Pt_out   = init.copy()
        self.Tt_out   = init.copy()
        self.P_out    = init.copy()
        self.T_out    = init.copy()
        self.W_out    = init.copy()
        self.XMN_out  = init.copy()
        self.Ht_out   = init.copy()

        # Characteristics
        self.PR       = init.copy()
        self.PRi      = init.copy()
        self.PRm      = init.copy()
        self.TR       = init.copy()
        self.AR       = init.copy()
        self.FAR      = init.copy()

        for mix_in in kwargs:

            values = kwargs[mix_in]
            
            if mix_in == 'name':
                continue
            
            elif len(values) == 2:
                value = values['value']
                units = values['units']

            elif len(values) < 1:
                raise ValueError("Input is missing value or units")
                
            elif len(values) > 2:
                raise ValueError("Input has more than one value or units")
            

            if mix_in == 'name':
                self.name = values

            elif mix_in in mix_vars:
                exp1 = f"self.{mix_in}['value'] = value"
                exp2 = f"self.{mix_in}['units'] = units"

                exec(exp1)                
                exec(exp2)

            else:
                raise Warning("Some inputs were not expected, ignoring extra inputs")


    def discharge_temperature(self):
        check_units(self.Tt_in1, self.Tt_in2)
        check_units(self.W_in1, self.W_in2)
        
        self.Tt_out['value'] = (self.W_in1['value'] * self.Tt_in1['value'] + self.W_in2['value'] * self.Tt_in2['value']) / (self.W_in1['value'] + self.W_in2['value'])
        self.Tt_out['units'] = self.Tt_in1['units']
        
    def discharge_enthalpy(self):
        cp = 1004  # This can go away by adding the air as inlet fluid
        
        self.Ht_out['value'] = cp * self.Tt_out['value']
        self.Ht_out['units'] = 'J / kg'

    def assume_ideal(self):
        
        if self.XMN_in1['value'] > 0:
            self.XMN_in2['value'] = self.XMN_in1['value']
            self.XMN_in2['units'] = self.XMN_in1['units']

        elif self.XMN_in2['value'] > 0:
            self.XMN_in1['value'] = self.XMN_in2['value']
            self.XMN_in1['units'] = self.XMN_in2['units']
            
        if self.P_in1['value'] > 0:
            self.P_in2['value'] = self.P_in1['value']
            self.P_in1['units'] = self.P_in2['units']
            
        elif self.P_in2['value'] > 0:
            self.P_in1['value'] = self.P_in2['value']
            self.P_in1['units'] = self.P_in2['units']

    def area_ratio(self):
        
        if self.T_in2['value'] > 0:
            pass
        else:
            T_Tt_2 = gd.stagnation_temperature_ratio(mach=self.XMN_in2['value'])
            self.T_in2['value'] = self.Tt_in2['value'] * T_Tt_2
            self.T_in2['units'] = self.Tt_in2['units']
        
        check_units(self.T_in1, self.T_in2)
        check_units(self.W_in1, self.W_in2)

        self.AR['value'] = (self.W_in2['value']/self.W_in1['value']) * (self.T_in2['value'] / self.T_in1['value']) ** (1/2)

    def sonic_velocity(self, T):
        # Working fluids:
        air  = gd.fluid('air' , gamma=1.4, R=287, units ='J/kg-K')
        
        # a = (y*R*T) ** (1/2)
        a = gd.sonic_velocity(temperature=T, gas=air)
        return a
    
    def discharge_mach(self):
        # Working fluids:
        air  = gd.fluid('air' , gamma=1.4, R=287, units ='J/kg-K')
        
        cp = 1004
        y = air.gamma
        R = air.R
        
        a1  = self.sonic_velocity(self.T_in1['value'])
        a2  = self.sonic_velocity(self.T_in2['value'])

        temp1 = ((1 + y * self.XMN_in1['value'] ** 2) + self.AR['value'] * (1 + y * self.XMN_in2['value'] ** 2)) / (1 + self.AR['value'])
        temp2 = (( (y-1)*self.Ht_out['value']) ** (1/2) ) *( (self.XMN_in1['value'] / a1 ) + self.AR['value'] * (self.XMN_in2['value'] / a2) ) / (1 + self.AR['value'])
        temp3 = (temp1 / temp2) ** 2
        temp4 = (2 * y ** 2) - temp3 * (y-1) 
        temp5 = ((temp3 - 2*y) ** 2) - 2*temp4
        
        self.XMN_out['value'] = ((temp3 - 2*y - (temp5)**(1/2)) / temp4)**(1/2)

    def discharge_static_pressure(self):
        # Working fluids:
        air  = gd.fluid('air' , gamma=1.4, R=287, units ='J/kg-K')
        
        cp = 1004
        y = air.gamma
        R = air.R
        
        temp1 = ((1 + y * self.XMN_in1['value'] ** 2) + self.AR['value'] * (1 + y * self.XMN_in2['value'] ** 2)) / (1 + self.AR['value'])

        self.P_out['value'] = self.P_in1['value'] * (temp1/(1 + y * self.XMN_out['value']**2))
        self.P_out['units'] = self.P_in1['units']

    def pressure_ratio_ideal(self):
        # Working fluids:
        air  = gd.fluid('air' , gamma=1.4, R=287, units ='J/kg-K')
        
        cp = 1004
        y = air.gamma
        R = air.R

        num = 1 + (1/2)*(y-1) * self.XMN_out['value'] ** 2
        den = 1 + (1/2)*(y-1) * self.XMN_in1['value'] ** 2
        exp = y / (y - 1)

        check_units(self.P_in1, self.Pt_out)
        
        self.PRi['value'] = (self.P_out['value'] / self.P_in1['value']) * (num / den) ** exp 
        self.PRi['units'] = '-' 
        
    def pressure_ratio_mixed(self):
        self.PRm['value'] = self.PRi['value'] * self.PR['value']
        pass

    def discharge_pressure_mixed(self):
        self.Pt_out['value'] = self.PRm['value'] * self.PRi['value'] * self.Pt_in1['value']
        self.Pt_out['units'] = self.Pt_in1['units']
        
    def mass_convervation(self):
        check_units(self.W_in1, self.W_in2)
        self.W_out['value'] = self.W_in1['value'] + self.W_in2['value']
        self.W_out['units'] = self.W_in1['units']
        
    def calc(self):
        
        self.discharge_temperature()
        self.discharge_enthalpy()
        self.assume_ideal()
        self.area_ratio()
        self.discharge_mach()
        self.discharge_static_pressure()
        self.pressure_ratio_ideal()
        self.pressure_ratio_mixed()
        self.discharge_pressure_mixed()
        self.mass_convervation()

    def __str__(self):
        out = f"Mixer: {self.name}\n"

        return out
