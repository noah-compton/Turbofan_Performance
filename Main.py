# Date    | Description of Changes:                          | Author
# -----------------------------------------------------------------------------
# Dec 4   | Fist upload to GitHub                            | Noah C.
# -----------------------------------------------------------------------------

import components
from methods import LinkPorts
import gas_dynamics as gd

from inlet import Inlet  # Added, Noah C. Dec 3
from fan import Fan  # Added, Noah C. Dec 3
from compressor import Compressor
from burner import Burner  # Added, Noah C. Dec 3
from turbine import Turbine  # Added, Noah C. Dec 3
from mixer import Mixer  # Added, Noah C. Dec 3
from nozzle import Nozzle  # Added, Noah C. Dec 3

Int10 = Inlet(name="Int10")
Fan20 = Fan(name="Fan20")
Cmp30 = Compressor(name="Cmp30")
Brn40 = Burner(name="Brn40")
Trb50 = Turbine(name="Trb50")
Mix60 = Mixer(name="Mix60")
Noz70 = Nozzle(name="Noz70")

# Component Characteristics
W_total = 25  # [kg/s] total mass flow coming into engine
pi_d = 0.9  # Total pressure ratio across inlet

pi_f = 1.5  # Total pressure ratio across fan
ef = 0.9  # fan polytropic efficiency

pi_c = 20  # compressor pressure ratio
ec = 0.9  # compressor polytropic efficiency

pi_b = 0.95  # Burner pressure ratio
nb = 0.98  # Burner efficiency
Qr = 42800000  # [J/kg] heat of reaction
Tt4 = 1673  # [K] outlet total temp of burner

et = 0.92  # polytropic efficiency of turbine
nm = 0.95  # mechanical efficiency of turbine
M5 = 0.5  # Mach at turbine exit

pi_mf = 0.98  # Mixer

pi_n = 0.9  # Nozzle pressure ratio

# Initial Conditions
R = 287  # [J / kg K]  gas constant
y = 1.4  # Ratio of specific heats -> remains constant throughout
cp = 1004  # [J / kg K] specific heat
XMN_0 = 2  # Free stream Mach number
P0 = 12  # [kPa] free stream static pressure
T0 = 223  # [K] free stream static temp
Pt0 = gd.stagnation_pressure(pressure=P0, mach=XMN_0)
Tt0 = gd.stagnation_temperature(temperature=T0, mach=XMN_0)
Int10.Pt_in = {"value": Pt0, "units": "kPa"}
Int10.Tt_in = {"value": Tt0, "units": "K"}
