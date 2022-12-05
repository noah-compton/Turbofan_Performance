# Date    | Description of Changes:                          | Author
# -----------------------------------------------------------------------------
# Dec 4   | Fist upload to GitHub                            | Noah C.
# -----------------------------------------------------------------------------

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

# Calculations
# Inlet/Diffuser
Int10.PR = {"value": pi_d, "units": ""}
Int10.P_in = {"value": P0, "units": "kPa"}
Int10.T_in = {"value": T0, "units": "K"}
Int10.W_in = {"value": W_total, "units": "kg/s"}
Int10.XMN_in = {"value": XMN_0, "units": ""}
Int10.calc()

# Fan
Fan20.eff_poly = {"value": ef, "units": ""}
Fan20.PR = {"value": pi_f, "units": ""}
LinkPorts(Int10, Fan20)
Fan20.calc()

# Compressor
Cmp30.PR = {"value": pi_c, "units": ""}
Cmp30.eff_poly = {"value": ec, "units": ""}
LinkPorts(Fan20, Cmp30)
Cmp30.calc()

# Burner
Brn40.PR = {"value": pi_b, "units": ""}
Brn40.eff_mech = {"value": nb, "units": ""}
Brn40.Tt_out = {"value": Tt4, "units": "K"}
LinkPorts(Cmp30, Brn40)
Brn40.calc()

# Turbine
pi_t = pi_f / (pi_b * pi_c)
Trb50.PR = {"value": pi_t, "units": ""}
Trb50.eff_mech = {"value": nm, "units": ""}
Trb50.eff_poly = {"value": et, "units": ""}
Trb50.XMN_out = {"value": M5, "units": ""}
Trb50.burner_f = {"value": Brn40.f["value"], "units": Brn40.f["units"]}
Trb50.burner_TRmax = {"value": Brn40.TRmax["value"], "units": Brn40.TRmax["units"]}
Trb50.compr_TR = {"value": Cmp30.TR["value"], "units": Cmp30.TR["units"]}
Trb50.fan_TR = {"value": Fan20.TR["value"], "units": Fan20.TR["units"]}
Trb50.inlet_TR = {"value": Int10.TR["value"], "units": Int10.TR["units"]}
LinkPorts(Brn40, Trb50)
Trb50.calc()
