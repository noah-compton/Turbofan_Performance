__author__ = "Jose M. Roque"
__version__ = "0.0.1"
__status__ = "Development"
'''
processes are functions used accross all classes that represent components, as well as to connect stations
'''
def LinkPorts(object1, object2):
    object2.Pt_in = object1.Pt_out
    object2.Tt_in = object1.Tt_out
    object2.W_in  = object1.W_out
    
    object2.inlet  = object1.name
    object1.outlet = object2.name


def LinkStreams(object1, object2, object3):
    object3.Pt_in1   = object1.Pt_out
    object3.P_in1    = object1.P_out
    object3.Tt_in1   = object1.Tt_out
    object3.T_in1    = object1.T_out
    object3.W_in1    = object1.W_out
    object3.XMN_in1  = object1.XMN_out
    
    object1.outlet  = object3.name
    object3.inlet1  = object1.name
    
    object3.Pt_in2   = object2.Pt_out
    object3.P_in2    = object2.P_out
    object3.Tt_in2   = object2.Tt_out
    object3.T_in     = object2.T_out
    object3.W_in2    = object2.W_out
    object3.XMN_in2  = object2.XMN_out
    
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
    Fg['units'] = nozzle.W_out['units'] + nozzle.u_out['units']
    
    if Fg['units'] == 'kg/sm/s':
        Fg['units'] = 'N'
    
    return Fg

def ram_drag(inlet):
    
    Dram = {"value": 0.0, "units": "-"}
    Dram['value'] = inlet.W_in['value'] * inlet.u_in['value']
    Dram['units'] = inlet.W_in['units'] + inlet.u_in['units']
    
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
    KE1 = (1/2) *  inlet.W_out['value'] *     inlet.u_in['value']
    den = Qr    *    burner.Wf['value'] * burner.eff_mech['value']
    
    eff_ther  = (KE2 - KE1) / den

    Fn = net_thrust(inlet, nozzle)

    eff_prop = Fn['value'] * inlet.u_in['value'] / (KE2 - KE1)

    eff_all = eff_prop * eff_ther  

    return eff_ther, eff_prop, eff_all
    
def tsfc(inlet, burner, nozzle):
    Qr = 42800000
    TSFC      = {"value": 0.0, "units": "-"}

    Fn = net_thrust(inlet, nozzle)
    
    TSFC['value'] = burner.Wf['value'] / Fn['value']
    
    return TSFC

def set_stations():
    P0      = Int00.P_in
    T0      = Int00.T_in
    Pt0     = Int00.Pt_in
    Tt0     = Int00.Tt_in
    XMN0    = Int00.XMN_in

    P1      = Fan10.P_in
    T1      = Fan10.T_in
    Pt1     = Fan10.Pt_in
    Tt1     = Fan10.Tt_in
    XMN1    = Fan10.XMN_in

    P2      = Cmp20.P_in
    T2      = Cmp20.T_in
    Pt2     = Cmp20.Pt_in
    Tt2     = Cmp20.Tt_in
    XMN2    = Cmp20.XMN_in

    P3      = Brn30.P_in
    T3      = Brn30.T_in
    Pt3     = Brn30.Pt_in
    Tt3     = Brn30.Tt_in
    XMN3    = Brn30.XMN_in

    P4      = Trb40.P_in
    T4      = Trb40.T_in
    Pt4     = Trb40.Pt_in
    Tt4     = Trb40.Tt_in
    XMN4    = Trb40.XMN_in

    P5      = Mix50.P_in
    T5      = Mix50.T_in
    Pt5     = Mix50.Pt_in
    Tt5     = Mix50.Tt_in
    XMN5    = Mix50.XMN_in

    P7      = Noz70.P_in
    T7      = Noz70.T_in
    Pt7     = Noz70.Pt_in
    Tt7     = Noz70.Tt_in
    XMN7    = Noz70.XMN_in