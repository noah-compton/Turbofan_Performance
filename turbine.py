import gas_dynamics as gd
import math


class turbine:
    def turbine_efficiency(
        Tt_out: float,
        Tt_in: float,
        Pt_out: float,
        Pt_in: float,
        gas: gd.fluid = gd.fluids.air,
    ) -> float:
        # Calculates the isentropic turbine efficiency from conditions before and after turbine

        turbine_effficiency = (1 - (Tt_out / Tt_in)) / (
            1 - (Pt_out / Pt_in) ** ((gas.gamma - 1) / gas.gamma)
        )

        return turbine_efficiency

    def turbine_Tt_out_from_efficiency(
        efficiency: float,
        Tt_in: float,
        Pt_out: float,
        Pt_in: float,
        gas: gd.fluid = gd.fluids.air,
    ) -> float:
        # Calculates the temperature after turbine using isentropic efficiency

        Tt_out = (-Tt_in) * (
            efficiency * (1 - (Pt_out / Pt_in) ** ((gas.gamma - 1) / gas.gamma)) - 1
        )

        return Tt_out

    def turbine_Pt_out_from_efficiency(
        efficiency: float,
        Tt_out: float,
        Tt_in: float,
        Pt_in: float,
        gas: gd.fluid = gd.fluids.air,
    ) -> float:
        # Calculates the pressure after turbine using isentropic efficiency

        Pt_out = Pt_in * (1 - ((1 - Tt_out / Tt_in) / efficiency)) ** (
            gas.gamma / (gas.gamma - 1)
        )

        return Pt_out

    def turbine_Tt_out(
        Tt_in: float, Pt_out: float, Pt_in: float, gas: gd.fluid = gd.fluids.air
    ) -> float:
        # Calculates the ideal total temperature after turbine

        Tt_out = Tt_in * (Pt_out / Pt_in) ** ((gas.gamma - 1) / gas.gamma)

        return Tt_out

    def turbine_Pt_out(
        Tt_out: float, Tt_in: float, Pt_in: float, gas: gd.fluid = gd.fluids.air
    ) -> float:
        # Calculates the ideal total pressure after turbine

        Pt_out = Pt_in * (Tt_out / Tt_in) ** (gas.gamma / (gas.gamma - 1))

        return Pt_out
