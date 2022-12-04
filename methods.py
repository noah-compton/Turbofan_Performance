# Initial
# Jose R.

# class Property():
#     def __init__(self,value,unit):
#         self.value = value
#         self.unit = unit

# class LinkPorts:
#     def __init__(self) -> None:
#         pass

import pdb
# import gas_dynamics as gd

# def Fluid(name: str, gamma: float, R: float, units: str):
#     gas = gd.fluid(name=name, gamma=gamma, R=R, units=units)
#     gas.cp = gas.gamma * gas.R / (gas.gamma - 1)
#     gas.cv = gas.cp - gas.R
#     return gas    
    
def Drag():
    pass
    #Calculate Drag

def Thrust():
    pass
    # Calculate Net Thrust
    
# def LinkPort(outlet):   
#     inlet = (outlet['value'] , outlet['unit'])
    
#     return inlet

def LinkPorts(object1, object2):
    object2.Pt_in = object1.Pt_out
    object2.Tt_in = object1.Tt_out
    object2.W_in  = object1.W_out
    object2.TRmax = object1.TRmax
    
    object2.inlet  = object1.name
    object1.outlet = object2.name
    
    