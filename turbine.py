import gas_dynamics as gd
import math


def turbine_efficiency(
    Tt5: float, Tt4: float, Pt5: float, Pt4: float, gas: gd.fluid = gd.fluids.air
) -> float:
    # Calculates the isentropic turbine efficiency from conditions before and after turbine

    turbine_effficiency = (1 - (Tt5 / Tt4)) / (
        1 - (Pt5 / Pt4) ** ((gas.gamma - 1) / gas.gamma)
    )

    return turbine_efficiency


def turbine_Tt5_from_efficiency(
    efficiency: float,
    Tt4: float,
    Pt5: float,
    Pt4: float,
    gas: gd.fluid = gd.fluids.air,
) -> float:
    # Calculates the temperature after turbine using isentropic efficiency

    Tt5 = (-Tt4) * (efficiency * (1 - (Pt5 / Pt4) ** ((gas.gamma - 1) / gas.gamma)) - 1)

    return Tt5


def turbine_Pt5_from_efficiency(
    efficiency:float, 
    Tt5:float, 
    Tt4:float, 
    Pt4:float, 
    gas: gd.fluid = gd.fluids.air,
) -> float:
    # Calculates the pressure after turbine using isentropic efficiency

    Pt5 = Pt4*(1-((1-Tt5/Tt4)/efficiency))**(gas.gamma/(gas.gamma-1))

    return Pt5


def turbine_Tt5(
    Tt4: float, Pt5: float, Pt4: float, gas: gd.fluid = gd.fluids.air
) -> float:
    # Calculates the ideal total temperature after turbine

    Tt5 = Tt4 * (Pt5 / Pt4) ** ((gas.gamma - 1) / gas.gamma)

    return Tt5


def turbine_Pt5(
    Tt5: float, Tt4: float, Pt4: float, gas: gd.fluid = gd.fluids.air
) -> float:
    # Calculates the ideal total pressure after turbine

    Pt5 = Pt4 * (Tt5 / Tt4) ** (gas.gamma / (gas.gamma - 1))

    return Pt5
 