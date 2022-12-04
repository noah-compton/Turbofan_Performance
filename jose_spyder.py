import MATLAB_calc as MATLAB
import pdb

# Global Variables
global T0
T0 = MATLAB.T0

# Methods
from methods import LinkPorts

# Part List
from compressor import Compressor
from burner import Burner
from turbine import Turbine

# Components
Cmp20 = Compressor(name='Cmp20')
Brn30 = Burner(name='Brn30')
Trb40 = Turbine(name='Trb40')

# Test Data
# Compressor, Station: 20
Cmp20.Pt_in    = {'value': MATLAB.Pt2   , 'units': 'Pa' }
Cmp20.Tt_in    = {'value': MATLAB.Tt2   , 'units': 'K'  }
Cmp20.PR       = {'value': MATLAB.pi_c  , 'units': '-'  }
Cmp20.eff_poly = {'value': MATLAB.ec    , 'units': '-'  }

# Burner, Station: 30
Brn30.PR       = {'value': MATLAB.pi_b  , 'units': '-'  }
Brn30.eff_mech = {'value': MATLAB.nb    , 'units': '-'  }
Brn30.Tt_out   = {'value': MATLAB.Tt4   , 'units': 'K'  }

# Turbine, Station: 40
Trb40.XMN_out  = {'value': MATLAB.pi_b  , 'units': '-'  }
Trb40.eff_mech = {'value': MATLAB.nm    , 'units': '-'  }
Trb40.eff_poly = {'value': MATLAB.et  , 'units': '-'  }

Cmp20.calc()
LinkPorts(Cmp20, Brn30)

Brn30.calc()
LinkPorts(Brn30, Trb40)

Trb40.calc()
pdb.set_trace()