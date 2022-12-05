# Initial
# Jose R.

from part_list import *

def LinkPorts(object1, object2):
    object2.Pt_in = object1.Pt_out
    object2.Tt_in = object1.Tt_out
    object2.W_in  = object1.W_out
    
    object2.inlet  = object1.name
    object1.outlet = object2.name

def LinkStreams(object1, object2, object3):
    object3.Pt_in1 = object1.Pt_out
    object3.Tt_in1 = object1.Tt_out
    object3.W_in1  = object1.W_out
    
    object1.outlet  = object3.name
    object3.inlet1  = object1.name
    
    object3.Pt_in = object2.Pt_out
    object3.Tt_in = object2.Tt_out
    object3.W_in  = object2.W_out
    
    object3.inlet2  = object2.name
    object2.outlet  = object1.name
    
def SplitStream(object1, object2, object3):
    object2.Pt_in = object1.Pt_out1
    object2.Tt_in = object1.Tt_out1
    object2.W_in  = object1.W_out1
    
    object2.inlet  = object1.name
    object1.outlet1 = object2.name
    
    object3.Pt_in = object1.Pt_out2
    object3.Tt_in = object1.Tt_out2
    object3.W_in  = object1.W_out2
    
    object3.inlet  = object1.name
    object1.outlet2 = object3.name
    
    
# Define a function that checks units
def check_units(var1, var2):
    if type(var1) is dict and type(var2) is dict:
        if var1['units'] != var2['units']:
            raise ValueError(f"Units not consistent, var1 {var1['units']} | var2 {var2['units']}")

    elif type(var1) is dict and type(var2) is str:
        if var1['units'] != var2:
            raise ValueError(f"Units not consistent, var1 {var1['units']} | var2 {var2['units']}")

    elif type(var1) is str and type(var2) is dict:
        if var1 != var2['units']:
            raise ValueError(f"Units not consistent, var1 {var1['units']} | var2 {var2['units']}")

    elif type(var1) is str and type(var2) is str:
        if var1 != var2:
            raise ValueError(f"Units not consistent, var1 {var1['units']} | var2 {var2['units']}")

    else:
        raise ValueError("Data type not recognized")
        
        
def gross_thrust(nozzle):
    
    Fg = {"value": 0.0, "units": "-"}
    Fg['value'] = nozzle.W_out['value'] * nozzle.u_out['value']
    Fg['units'] = nozzle.W_in['value'] + nozzle.u['value']
    
    if Fg['units'] == 'kg/sm/s':
        Fg['units'] = 'N'
    
    return Fg

def ram_drag(inlet):
    
    Dram = {"value": 0.0, "units": "-"}
    Dram['value'] = inlet.W_in['value'] * inlet.u_in['value']
    Dram['units'] = inlet.W_in['value'] + inlet.u_in['value']
    
    if Dram['units'] == 'kg/sm/s':
        Dram['units'] = 'N'
    
    
    return Dram

def net_thrust(inlet, nozzle):
    
    Fn = {"value": 0.0, "units": "-"}
    
    Fg = gross_thrust(nozzle)
    Dram = ram_drag(inlet)
    
    check_units(Fg, Dram)
    
    Fn['value'] = Fg['value'] - Dram['value']
    Fn['units'] = Fg['units']
    
    return Fn

def efficiency(inlet, burner, nozzle):
    Qr = 42800000
    
    TSFC      = {"value": 0.0, "units": "-"}
    
    KE2 = (1/2) * nozzle.W_out['value'] *    nozzle.u_out['value'] 
    KE1 = (1/2) *  inlet.W_out['value'] *     inlet.u_out['value']
    den = Qr    *    burner.Wf['value'] * burner.eff_poly['value']
    
    eff_ther  = (KE2 - KE1) / den

    Fn = net_thrust(inlet, nozzle)
    
    TSFC['value'] = burner.Wf['value'] / Fn['value']
    
    eff_prop = Fn['value'] * inlet.u_in['value'] / (KE2 - KE1)

    eff_all = eff_prop * eff_ther  

    return eff_ther, eff_prop, eff_all, TSFC
    
    
    
    