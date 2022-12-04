# Date    | Description of Changes:                          | Author
# -----------------------------------------------------------------------------
# Dec 4   | Fist upload to GitHub                            | Noah C.
# -----------------------------------------------------------------------------

import components
from methods import LinkPorts

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
P0 = 12000  # [Pa] free stream static pressure
T0 = 223  # [K] free stream static temp

components.configuration("configuration one")

Inlet
