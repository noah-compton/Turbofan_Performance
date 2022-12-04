# inlet/flight conditions calculations
# Isabel H
# need to define __str__


import gas_dynamics as gd
import math


#establish y = 1.4, R, as global variables using gd package
global y
y = gd.fluids.air.gamma

global R
R = gd.fluids.air.R

class Inlet:
    def __init__(self, **kwargs):
        
        init = {'value': 0., 'unit': '-'}
        
        self.name   = ''
        
        #Inlet
        self.P0 = init.copy() # P_in
        self.T0 = init.copy() # T_in
        self.M0 = init.copy() # XMN_in
        self.m2 = init.copy() # W_in

        #Outlet
        self.Pt_in = init.copy()
        self.Tt_in = init.copy()
        self.a0 = init.copy()    # a_in
        self.u0 = init.copy()    # u_in
        self.Tt_out = init.copy()
        self.Pt_out = init.copy()
        self.Dram = init.copy()     # Will be calculated outside of the class

        #Characteristics
        self.Pi_d = init.copy()    # Pi_d = PR
        self.T_r = init.copy()     # TR

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

            
            if property == "P0":
                self.P0['value'] = value

                if len(values) == 2:
                    self.P0["unit"] = unit

                elif len(values) < 2:
                    self.P0['unit'] = 'Pa'
                    raise Warning("Not enough inputs: assuming Pa for units for P_in")

            
            elif property == "T0":
                 self.T0["value"] = value

                 if len(values) == 2:
                    self.T0["unit"] = unit

                 elif len(values) < 2:
                        self.T0["unit"] = "K"
                        raise Warning("Not enough inputs: assuming K as units for T_in.")

            
            elif property == "M0":
                 self.T0["value"] = value

                 if len(values) == 2:
                    self.M0["unit"] = unit

                 elif len(values) < 2:
                        self.M0["unit"] = ""
                        raise Warning("Not enough inputs: assuming dimensionless parameter.")

            
            elif property == "m2":
                 self.m2["value"] = value

                 if len(values) == 2:
                    self.m2["unit"] = unit

                 elif len(values) < 2:
                        self.m2["unit"] = "kg/s"
                        raise Warning("Not enough inputs: assuming kg/s as units for m2.")
            
            elif property == "Pi_d":
                 self.Pi_d["value"] = value

                 if len(values) == 2:
                    self.Pi_d["unit"] = unit

                 elif len(values) < 2:
                        self.Pi_d["unit"] = ""
                        raise Warning("Not enough inputs: assuming dimensionless parameter.")

            elif property == "name":
                self.name = values
            

    def calc(self):
        if self.T0["value"] > 0 and self.P0["value"] > 0 and self.M0["value"] > 0 and self.m2["value"] > 0:
             pass
        else:
             raise ValueError("Incorrect inputs for inlet: nonzero values required for P0, T0, M0, m2")

       #calculate values
        self.a0["value"] = math.sqrt(y * R * self.T0["value"])
        self.u0["value"] = self.M0["value"] * self.a_in["value"]
        self.Tt_in["value"] = gd.stagnation_temperature_ratio(mach = self.M0["value"])
        self.Pt_in["value"] = gd.stagnation_pressure_ratio(mach = self.M0["value"])
        self.Tt_out["value"] = self.Tt_in["value"]
        self.T_r = self.Tt_in["value"] / self.T0["value"]
        self.Pt_out["value"] = self.Pt_in["value"] * self.Pi_d["value"]
        self.Dram["value"] = self.m2["value"] * self.u_in["value"]
       
       #units
        self.a0["unit"] = "m/s"
        self.u0["unit"] = "m/s"
        self.Tt_in["unit"] = "K"
        self.Pt_in["unit"] = "Pa"
        self.Tt_out["unit"] = "K"
        self.Pt_out["unit"] = "Pa"
        self.Dram["unit"] = "kN"

    def __str__(self):
        str = f"{self.name} Characteristics:\n"
