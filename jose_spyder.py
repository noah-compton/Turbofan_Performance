import MATLAB_calc as MATLAB
import pdb

# Global Variables

# Part List
from part_list import *

# processes
from processes import *

# Global variables
global T0 # Maybe?

# Flight Conditions (Free Stream)
T0   = {'value': 223   , 'units': 'K' }
P0   = {'value': 12000 , 'units': 'Pa'}
XMN0 = {'value': 2.000 , 'units': '-' }

# Components
# Int00 = Inlet(name='Int10')
# Fan10 = Fan(name='Fan10')
# Byp13 =     Bypass(name='Byp13')
Cmp20 = Compressor(name='Cmp20')
Brn30 =     Burner(name='Brn30')
Trb40 =    Turbine(name='Trb40')
Mix50 =      Mixer(name='Mix50')

# Test Data
# Inlet, Station: 10

# Compressor, Station: 20
Cmp20.Pt_in    = {'value': MATLAB.Pt2   , 'units': 'Pa'}
Cmp20.Tt_in    = {'value': MATLAB.Tt2   , 'units': 'K' }
Cmp20.PR       = {'value': MATLAB.pi_c  , 'units': '-' }
Cmp20.eff_poly = {'value': MATLAB.ec    , 'units': '-' }

# Burner, Station: 30
Brn30.PR       = {'value': MATLAB.pi_b  , 'units': '-' }
Brn30.eff_mech = {'value': MATLAB.nb    , 'units': '-' }
Brn30.Tt_out   = {'value': MATLAB.Tt4   , 'units': 'K' }

# Turbine, Station: 40
Trb40.XMN_out  = {'value': MATLAB.pi_b  , 'units': '-' }
Trb40.eff_mech = {'value': MATLAB.nm    , 'units': '-' }
Trb40.eff_poly = {'value': MATLAB.et    , 'units': '-' }
Trb40.W_out    = Trb40.W_in

Mix50.Tt_in2  = {'value': MATLAB.Tt15  , 'units': 'K' }
Mix50.PR      = {'value': MATLAB.pi_mf , 'units': '-' }

Cmp20.calc()
LinkPorts(Cmp20, Brn30)

Brn30.calc(T0)

Mix50.XMN_in1 = {'value': MATLAB.M5              , 'units': '-'   }
Mix50.P_in1   = {'value': MATLAB.P5              , 'units': 'Pa'  }
Mix50.T_in1   = {'value': MATLAB.T5              , 'units': 'K'   }
Mix50.Pt_in1  = {'value': MATLAB.Pt5             , 'units': 'Pa'  }
Mix50.Tt_in1  = {'value': MATLAB.Tt5             , 'units': 'K'   }
Mix50.W_in1   = {'value': MATLAB.m0 + MATLAB.mf  , 'units': 'pps' }
Mix50.W_in2   = {'value': MATLAB.mfan            , 'units': 'pps' }

Trb40.calc()

Mix50.calc()

