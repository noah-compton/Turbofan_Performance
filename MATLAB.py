# Problem 2:
# all pi_a are TOTAL ratios
# unless pi_(greek letter), check definition.

# Define global variables
global R, y, cp, M0, P0, T0

# Import Packages
import math
from compressor import Compressor
from burner import Burner
from turbine import Turbine
from methods import LinkPort
import pdb

# Air constants
R = 287 # [J / kg K]
y = 1.4 # Constant through the engine
cp = 1004 # [J/ kg K]

# Given:
# Stream (0)
M0 = 2 # Freestream Mach number [-]
P0 = 12000 # [Pa]
T0 = 223 # [K]

# Inlet (2)
m2 = 25 # [kg/s] (1+bypass_ratio)*m0 = 25 kg/s (total mass incoming)
pi_d = 0.9 # total pressure ratio across the inlet (diffuser)

# Compressor (2-3)
pi_c = 20 # compressor pressure ratio
ec = 0.9 # Polytropic efficiency

# Fan 
pi_f = 1.5 # fan pressure ratio
ef = 0.9 # Polytropic efficiency

# Burner (3-4)
pi_b = 0.95 # burner pressure ratio
nb = 0.98 # burner efficiency
Qr = 42800000 # heat of reaction [J/kg]
Tt4 = 1673 # [K]

# Turbine (4-5)
et = 0.92 # Polytropic efficiency
nm = 0.95 # Mechanical efficiency
M5 = 0.5 # Mach number at the turbine exit
pi_fd = 1 #

# Mixer
pi_mf = 0.98

# NO Afterburner

# Nozzle (Perfectly expanded)
pi_n = 0.9 # nozzle pressure ratio
P9 = P0 # exit pressure [Pa]

# CALCULATIONS
# (a) Flight conditions
a0 = math.sqrt(y*R*T0) # Speed of sound [m/s]
u0 = M0*a0 # Flow velocity [m/s]
Dram = m2*u0 # [kN]
Tt0 = T0 + (u0**2)/(2*cp) # [K]
Tt2 = Tt0 # [K]
T_r = Tt0/T0 # [-]
Pt0 = P0*(T_r)**(y/(y-1)) # [Pa] 
Pt2 = pi_d*Pt0 # [Pa]

# (b) Fan
T_f = (pi_f)**((y-1)/(y*ef)) # Tt13/Tt2 temperature ratio [-]
Pt13 = pi_f*Pt2 # [Pa]
Tt13 = T_f*Tt2 # [K]
Tt15 = Tt13 # [K]
Pt15 = Pt13 # [Pa]

# (c) Compressor
Cmp020 = Compressor(name="Cmp020", Pt_in=(Pt2, 'Pa'), Tt_in=(Tt2, 'K'), e=(ec, "-"), PR = (pi_c, "-"))
Cmp020.calc()

T_c = (pi_c)**((y-1)/(y*ec)) # Tt3/Tt2 temperature ratio [-]
Pt3 = pi_c*Pt2 # [Pa]
Tt3 = T_c*Tt2 # [K]

Brn030 = Burner(name='Brn030', Pt_in=LinkPort(Cmp020.Pt_out), Tt_in=LinkPort(Cmp020.Tt_out), Tt_out=(Tt4,'K'), e=(nb,'-'), PR=(pi_b, '-'))
Brn030.calc()

# (d) Burner
Pt4 = pi_b*Pt3 # [kPa]
f = cp*((Tt4-Tt3)/(Qr*nb-cp*Tt4)) # mf/m0 [-]
T_x = Tt4/T0 # [-] Tau_Lambda

# (e) Turbine

Trb040 = Turbine(name='Trb040')
Trb040.LinkPort(Brn030)
Trb040.calc()

pi_t = (pi_fd*pi_f)/(pi_b*pi_c) # Pt5/Pt4 [-]
T_t = (pi_t)**((y-1)*et/y) # Tt5/Tt4 [-]
Tt5 = T_t*Tt4 # [K]
T5 = Tt5*((1+0.5*(y-1)*M5**2)**-1) # [K]
a5 = math.sqrt(y*R*T5) # [m/s]
bypass_ratio = (nm*(1+f)*T_x*(1-T_t) - T_r*(T_c - 1))/(T_r*(T_f - 1)) # [-]
m0 = m2/(1+bypass_ratio) # [kg/s]
mfan = m2 - m0 # [kg/s]
mf = f*m0 # [kg/s]

# (f) Mixing
Pt5 = pi_t*Pt4 # [Pa]
P5 = Pt5*(((Tt5/T5)**(y/(y-1)))**-1) # [Pa]

ht6m = ((cp*T0)/(1+bypass_ratio+f))*((1+f)*T_t*T_x + bypass_ratio*T_r*T_f) # [J/kg]
Tt6m = ht6m/cp # [K]
M15 = M5 # [-]
T15 = Tt15*((1+((y-1)/2)*M15**2)**-1) # [K]
a15 = math.sqrt(y*R*T15) # [m/s]
P15 = P5 # [Pa]
A_ratio = (a15/a5)*(bypass_ratio/(1+f)) # [-]

K1 = (1 + y*M5**2 + A_ratio*(1 + y*M15**2))*((1+A_ratio)**-1) # Non-dimensional parameters [-]
K2 = (((M5/a5) + ((M15*A_ratio)/a15))*math.sqrt((y-1)*cp*Tt6m))*((1 + A_ratio)**-1) #[-]
K = (K1/K2)**2 # [-]

S1 =2*y**2 - K*(y - 1) # Support variables [-]
S2 = (K - 2*y)**2 - 2*S1 # [-]
M6m = math.sqrt((K - 2*y - math.sqrt(S2))/S1) # [-]

P6m = P5*(K1/(1 + y*M6m**2)) # [Pa]

S1 = 1 + (1/2)*(y - 1)*M6m**2 # Support variables # [-]
S2 = 1 + (1/2)*(y - 1)*M5**2 # [-]
pi_mi = (P6m/P5)*((S1/S2)**(y/(y - 1))) # [-]

Pt6mi = pi_mi*Pt5 # [Pa]
pi_m = pi_mi*pi_mf # [-]
Pt6m = Pt6mi*pi_m # [Pa]

# (g) Nozzle
Pt9 = pi_n*Pt6m # [Pa]
Pt9_9 = Pt9/P9 # Total pressure to pressure ratio [-]

S1 = (Pt9_9)**((y-1)/y)-1 # Support variable [-]
M9 = math.sqrt(2*S1/(y-1)) # [-]

Tt9 = Tt6m # [K]

S1 = 2 + (y-1)*M9**2 # Support variable
T9 = 2*(Tt9/S1) # [K]

a9 = math.sqrt(y*R*T9) # [m/s]
u9 = M9*a9 # [m/s]
u9_eff = u9 # [m/s]

# (h) Gross Thrust
Fg = (m2 + mf)*u9 # [N]

# (i) TSFC
F = Fg - Dram # [N]
TSFC = (mf/F)*10**6 # [mg/s/N]

# (j) Thermal Efficiency
dKE = (1/2)*((m2+mf)*(u9**2) - m2*(u0**2)) # [J]
nth = dKE/(mf*Qr*nb) # [-]

# (k) Propulsive Efficiency
nprop = (F*u0)/dKE # [-]

# (i) Overall Efficiency
noverall = nth*nprop # [-]

# # Changing units:
# # Pa -> kPa
# # N -> kN
# # J/kg -> kJ/kg
# Va = [a0 u0 Dram*10**-3 Tt0 Tt2 Pt0*10**-3 Pt2*10**-3 T_r]
# Vb = [T_f Pt13*10**-3 Tt13 Pt15*10**-3 Tt15]
# Vc = [T_c Pt3*10**-3 Tt3]
# Vd = [Pt4*10**-3 f T_x]
# Ve = [pi_t T_t Tt5 T5 a5 bypass_ratio m0 mfan mf]
# Vf = [ht6m*10**-3 Tt6m M15 T15 a15 P15*10**-3 A_ratio M6m P6m*10**-3 pi_mi Pt6mi*10**-3 pi_m Pt6m*10**-3]
# Vg = [Pt9*10**-3 M9 Tt9 T9 a9 u9 u9_eff]
# Vh = Fg*10**-3
# Vi = TSFC
# Vj = nth
# Vk = nprop
# Vl = noverall

# # Final units:
# #  Length [m] Temperature [K]  Velocity [m/s] Force [kN] Pressure [kPa]
# #  Energy [kJ/kg] Mass flow rate [kg/s] TSFC [mg/s/N]

# # Column 1 and 2 of the table.
# # Note: the last 3 "Inf" are to fill in the spaces to they can be displayed
# C1 = [Va Vb Vc Vd Ve]
# C2 = [Vf Vg Vh Vi Vj Vk Vl1/01/01/0]

# # Display in columns
# [C1 C2]


