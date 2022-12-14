__author__ = "Jose M. Roque"
__version__ = "0.0.1"
__status__ = "Development"

'''
processes are functions used accross all classes that represent components, as well as to connect stations
'''

def LinkPorts(object1, object2):
    '''
    function LinkPorts(object1, object2) links the two streams of the engine components, by setting the inlet
    conditions of object2 equal to the outlet conditions of object1
    '''
    object2.Pt_in = object1.Pt_out
    object2.Tt_in = object1.Tt_out
    object2.W_in  = object1.W_out
    
    object2.inlet  = object1.name
    object1.outlet = object2.name


def LinkStreams(object1, object2, object3):
    '''
    function LinkStreams(object1, object2, object3) links the two outlets of object1 and object2 in the inlet of object3
    which should be a component that joins streams such as mixer
    '''
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
    '''
    function SplitStreams(object1, object2, object3) links the two outlets of object1 and object2 in the inlet of object3
    which should be a component that joins streams such as mixer
    '''
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
    '''
    function check_units(var1, var2) checks the dictionaries have the same entry for units, which is the datatype input for the
    Turbofan_performance
    '''

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
    '''
    function gross_thrust(nozzle) calculates the gross thrust of the engine built and simulated using the 
    Turbofan_performance package
    '''
    Fg = {"value": 0.0, "units": "-"}
    Fg['value'] = nozzle.W_out['value'] * nozzle.u_out['value']
    Fg['units'] = nozzle.W_out['units'] + nozzle.u_out['units']
    
    if Fg['units'] == 'kg/sm/s':
        Fg['units'] = 'N'
    
    return Fg

def ram_drag(inlet):
    '''
    function ram_drag(inlet) calculates the ram drag of the engine built and simulated using the 
    Turbofan_performance package
    '''

    Dram = {"value": 0.0, "units": "-"}
    Dram['value'] = inlet.W_in['value'] * inlet.u_in['value']
    Dram['units'] = inlet.W_in['units'] + inlet.u_in['units']
    
    if Dram['units'] == 'kg/sm/s':
        Dram['units'] = 'N'
    
    
    return Dram

def net_thrust(inlet, nozzle):
    '''
    function net_thrust(inlet, nozzle) calculates the net thrust of the engine built and simulated using the 
    Turbofan_performance package
    '''

    Fn = {"value": 0.0, "units": "-"}
    
    Fg = gross_thrust(nozzle)
    Dram = ram_drag(inlet)
    
    check_units(Fg, Dram)
    
    Fn['value'] = Fg['value'] - Dram['value']
    Fn['units'] = Fg['units']
    
    return Fn

def efficiency(inlet, burner, nozzle):
    '''
    function efficiency(inlet, burner, nozzle) calculates the efficiencies of the engine built and simulated using the 
    Turbofan_performance package
    '''
    Qr = 42800000
    
    KE2 = (1/2) * nozzle.W_out['value'] *    nozzle.u_out['value'] 
    KE1 = (1/2) *  inlet.W_out['value'] *     inlet.u_in['value']
    den = Qr    *    burner.Wf['value'] * burner.eff_mech['value']
    
    eff_ther  = (KE2 - KE1) / den

    Fn = net_thrust(inlet, nozzle)

    eff_prop = Fn['value'] * inlet.u_in['value'] / (KE2 - KE1)

    eff_all = eff_prop * eff_ther  

    return eff_ther, eff_prop, eff_all
    
def tsfc(inlet, burner, nozzle):
    '''
    function tsfc(inlet, burner, nozzle) calculates the thrust specific fuel consumption of the engine built and simulated using the 
    Turbofan_performance package
    '''

    Qr = 42800000
    TSFC      = {"value": 0.0, "units": "-"}

    Fn = net_thrust(inlet, nozzle)
    
    TSFC['value'] = burner.Wf['value'] / Fn['value']
    
    return TSFC

def set_stations(inlet, fan, compressor, burner, turbine, mixer, nozzle, bypass):
    '''
    function set_stations(inlet, fan, compressor, burner, turbine, mixer, nozzle, bypass) sets typical jet engine designations to the engine
    built and simulated using the Turbofan_performance package
    '''

    P0      = inlet.P_in
    T0      = inlet.T_in
    Pt0     = inlet.Pt_in
    Tt0     = inlet.Tt_in
    XMN0    = inlet.XMN_in

    P1      = fan.P_in
    T1      = fan.T_in
    Pt1     = fan.Pt_in
    Tt1     = fan.Tt_in
    XMN1    = fan.XMN_in

    P2      = compressor.P_in
    T2      = compressor.T_in
    Pt2     = compressor.Pt_in
    Tt2     = compressor.Tt_in
    XMN2    = compressor.XMN_in

    P3      = burner.P_in
    T3      = burner.T_in
    Pt3     = burner.Pt_in
    Tt3     = burner.Tt_in
    XMN3    = burner.XMN_in

    P4      = turbine.P_in
    T4      = turbine.T_in
    Pt4     = turbine.Pt_in
    Tt4     = turbine.Tt_in
    XMN4    = turbine.XMN_in

    P5      = mixer.P_in
    T5      = mixer.T_in
    Pt5     = mixer.Pt_in
    Tt5     = mixer.Tt_in
    XMN5    = mixer.XMN_in

    P7      = nozzle.P_in
    T7      = nozzle.T_in
    Pt7     = nozzle.Pt_in
    Tt7     = nozzle.Tt_in
    XMN7    = nozzle.XMN_in

    P13      = bypass.P_in
    T13      = bypass.T_in
    Pt13     = bypass.Pt_in
    Tt13     = bypass.Tt_in
    XMN13    = bypass.XMN_in
    
    return( P0   , T0   , Pt0  , Tt0  , XMN0  ,
            P1   , T1   , Pt1  , Tt1  , XMN1  , 
            P2   , T2   , Pt2  , Tt2  , XMN2  , 
            P3   , T3   , Pt3  , Tt3  , XMN3  , 
            P4   , T4   , Pt4  , Tt4  , XMN4  , 
            P5   , T5   , Pt5  , Tt5  , XMN5  , 
            P7   , T7   , Pt7  , Tt7  , XMN7  , 
            P13  , T13  , Pt13 , Tt13 , XMN13  )