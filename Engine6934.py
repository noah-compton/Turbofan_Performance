import pdb
import MATLAB_calc as MATLAB

# Part List
from inlet       import Inlet
from fan         import Fan
from bypass      import Bypass
from compressor  import Compressor
from burner      import Burner
from turbine     import Turbine
from mixer       import Mixer
from nozzle      import Nozzle

# Processes
from processes import *

def my_engine():
    # -------------------------------- ENGINE DEFINITION --------------------------------------
    # --------------------------------------- 6934 --------------------------------------------
    
    # Inlet
    Int00 =      Inlet(name='Int10') # Inlet
    
    # Core
    Fan10 =        Fan(name='Fan10') # Fan (for Turbofan)
    Cmp20 = Compressor(name='Cmp20') # Single Axial High Pressure Compressor
    Brn30 =     Burner(name='Brn30') # Burner or Combustion Chamber
    Trb40 =    Turbine(name='Trb40') # Single Axial High Pressure Turbine
    
    # Bypass
    Byp13 =     Bypass(name='Byp13') # Bypass right after Fan Station
    Byp15 =     Bypass(name='Byp15') # Bypass downstream before Mixing
    
    # Mixing Plane
    Mix50 =      Mixer(name='Mix50') # Mixing Plane
    
    # Nozzle / Exhaust
    Noz70 =     Nozzle(name='Noz70') # Exhaust
    
    # ----------------------------------- TEST DATA ------------------------------------------
    # Freestream + Inlet, Station: 00
    Int00.T_in       = {'value': 223.    , 'units': 'K'    }
    Int00.P_in       = {'value': 12000   , 'units': 'Pa'   }
    Int00.XMN_in     = {'value': 2.      , 'units': '-'    }
    Int00.W_in       = {'value': 25.     , 'units': 'kg/s' }
    Int00.PR         = {'value': 0.9     , 'units': '-'    }
    
    # Fan, Station: 10
    Fan10.PR         = {'value': 1.5     , 'units': '-'    }
    Fan10.eff_poly   = {'value': 0.9     , 'units': '-'    }
    
    # Compressor, Station: 20
    Cmp20.PR       = {'value': 20.     , 'units': '-'    }
    Cmp20.eff_poly = {'value': 0.9     , 'units': '-'    }
    
    # Burner, Station: 30
    Brn30.PR       = {'value': 0.95    , 'units': '-'    }
    Brn30.eff_mech = {'value': 0.98    , 'units': '-'    }
    Brn30.Tt_out   = {'value': 1673.   , 'units': 'K'    }
    
    # Turbine, Station: 40
    Trb40.eff_poly  = {'value': 0.92    , 'units': '-'    }
    Trb40.eff_mech  = {'value': 0.95    , 'units': '-'    }
    Trb40.XMN_out   = {'value': 0.5     , 'units': '-'    }
    
    # Mixer, Station: 50
    Mix50.PR       = {'value': 0.98     , 'units': '-'    } 
    
    # Nozzle, Station: 70
    Noz70.PR       = {'value': 0.9      , 'units': '-'    }
    Noz70.P_out    = Int00.P_in
    
    # ----------------------------------- SIMULATION ------------------------------------------
    Int00.calc()
    LinkPorts(Int00, Fan10)
    
    Fan10.calc()
    SplitStream(Fan10, Cmp20, Byp13)
    Byp13.calc()
    
    Cmp20.calc()
    LinkPorts(Cmp20, Brn30)
    
    Brn30.calc(T0=Int00.T_in)
    LinkPorts(Brn30, Trb40)
    
    # Turbine Calculated Parameters
    Trb40.inlet_TR     = Int00.TR
    Trb40.inlet_W_in   = Int00.W_in
    
    Trb40.fan_TR       = Fan10.TR
    Trb40.fan_PR       = Fan10.PR
    
    Trb40.compr_TR     = Cmp20.TR
    Trb40.compr_PR     = Cmp20.PR
    
    Trb40.burner_FAR   = Brn30.FAR
    Trb40.burner_TRmax = Brn30.TRmax
    Trb40.burner_PR    = Brn30.PR
    
    Trb40.calc()
    
    # Bypass Calculation
    Fan10.BPR = Trb40.BPR
    Fan10.mass_conservation()
    
    SplitStream(Fan10, Cmp20, Byp13)
    Cmp20.mass_conservation()
    LinkPorts(Cmp20, Brn30)
    Brn30.calc(T0=Int00.T_in)
    
    Byp13.calc()
    LinkPorts(Byp13, Byp15)
    Byp15.calc()
    
    LinkStreams(Trb40, Byp15, Mix50)
    
    Mix50.calc()
    LinkPorts(Mix50, Noz70)
    
    Noz70.calc()
    
    # ----------------------------------- PERFORMANCE ------------------------------------------
    Fn = net_thrust(Int00, Noz70)
    eff_ther, eff_prop, eff_all = efficiency(Int00, Brn30, Noz70)
    TSFC = tsfc(Int00, Brn30, Noz70)
    
    
    return Int00, Fan10, Cmp20, Brn30, Trb40, Mix50, Noz70, Fn, TSFC

