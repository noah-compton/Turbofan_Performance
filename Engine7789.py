# Part List
from inlet_v0       import Inlet
from fan_v2         import Fan
from bypass_v0      import Bypass
from compressor_v2  import Compressor
from burner_v0      import Burner
from turbine_v9     import Turbine
from mixer_v1       import Mixer
from nozzle_v0      import Nozzle

# Processes
from processes import *

# -------------------------------- ENGINE DEFINITION --------------------------------------
# --------------------------------------- 7789 --------------------------------------------
# Notes:
# 1) This engine is developed from Engine 6934 with the addition of the following components:
#    - High Pressure Compressor as Cmp25 downstream the original Cmp20 Compressor
#    - Low Pressure Turbine as Trb45 downstream the original Trb40 Turbine

# Inlet
Int00 =      Inlet(name='Int10') # Inlet

# Core
Fan10 =        Fan(name='Fan10') # Fan
Cmp20 = Compressor(name='Cmp20') # Low Pressure Compressor
Cmp25 = Compressor(name='Cmp25') # High Pressure Compressor
Brn30 =     Burner(name='Brn30') # Burner or Combustion Chamber
Trb40 =    Turbine(name='Trb40') # High Pressure Turbine
Trb45 =    Turbine(name='Trb45') # Low Pressure Turbine

# Bypass
Byp13 =     Bypass(name='Byp13') # Bypass right after Fan Station
Byp15 =     Bypass(name='Byp15') # Bypass downstream before Mixing

# Mixing Plane
Mix50 =      Mixer(name='Mix50') # Mixing Plane

# Nozzle / Exhaust
Noz70 =     Nozzle(name='Noz70') # Exhaust

# ----------------------------------- SIMULATION ------------------------------------------
# Inlet, Station: 00
Int00.T_in       = {'value': 223.    , 'units': 'K'    }
Int00.P_in       = {'value': 12000   , 'units': 'Pa'   }
Int00.XMN_in     = {'value': 2.      , 'units': '-'    }

# Compressor, Station: 20
Cmp20.PR       = {'value': 20.     , 'units': '-'    }
Cmp20.eff_poly = {'value': 0.9     , 'units': '-'    }

# Burner, Station: 30
Brn30.PR       = {'value': 0.95    , 'units': '-'    }
Brn30.eff_mech = {'value': 0.98    , 'units': '-'    }
Brn30.Tt_out   = {'value': 1673.   , 'units': 'K'    }

# Nozzle, Station: 70
Noz70.u_out    = {'value': 735.    , 'units': 'm/s'  }
Noz70.W_out    = {'value': 25.1070 , 'units': 'kg/s' }

# ----------------------------------- SIMULATION ------------------------------------------
Int00.calc()
LinkPorts(Int00, Fan10)

Fan10.calc()
SplitStream(Fan10, Cmp20, Byp13)

Cmp20.calc()
LinkPorts(Cmp20, Cmp25)

Cmp25.calc()
LinkPorts(Cmp25, Brn30)

Brn30.calc()
LinkPorts(Brn30, Trb40)

Trb40.calc()
LinkPorts(Trb40, Trb45)

Trb45.calc()
LinkPorts(Byp13, Byp15)
LinkStreams(Trb45, Byp15, Mix50)

Mix50.calc()
LinkPorts(Mix50, Noz70)

Noz70.calc()

# ------------------------------------ STATIONS --------------------------------------------
set_stations()

# ----------------------------------- PERFORMANCE ------------------------------------------
Fn = net_thrust(Int00, Noz70)
eff_ther, eff_prop, eff_all = efficiency(Int00, Brn30, Noz70)
TSFC = tsfc(Int00, Brn30, Noz70)