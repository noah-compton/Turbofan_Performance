# Date    | Description of Changes:                          | Author
# ----------------------------------------------------------------------------
# Dec 2   | Turbine changed to a Class with appropriate      | Noah C.
#         | alterations for workability                      |
#         | To do:                                           |   
#         |   - Add _str_ method                             |
#         |   - Add a5, byp ratio, m0, mfan, and mf methods  |
# ----------------------------------------------------------------------------
# Nov 25  | First Upload to Github                           |
# ----------------------------------------------------------------------------
# Nov 20  | Initial file creation as a collection of         | Noah C.
#         | functions.                                       |
# ----------------------------------------------------------------------------

import gas_dynamics as gd
import math


class Turbine:
    def _init_(self, **kwargs):

        initial = {"value": 0.0, "unit": "-"}

        self.name = ""

        # Inlet
        self.Pt_in = initial.copy()
        self.Tt_in = initial.copy()

        # Outlet
        self.Pt_out = initial.copy()
        self.Tt_out = initial.copy()
        self.speed_o_sound_out = initial.copy()

        # Characteristics
        self.pressure_ratio = initial.copy()
        self.temperature_ratio = initial.copy()
        self.polytropic_efficiency = initial.copy()
        self.mechanical_efficiency = initial.copy()
        self.bypass_ratio = initial.copy()
        self.mach_at_exit = initial.copy()
        self.m0 = initial.copy()
        self.mf = initial.copy()

        for value in kwargs:
            values = kwargs[property]

            if len(values) >= 2:
                value = values[0]
                unit = values[1]

                if len(values) > 2 and property != "name":
                    raise Warning(
                        f"Too many inputs for property {property}. First two inputs will be used."
                    )

            elif len(values) == 1:
                value = values[0]
                unit = ""

            else:
                raise ValueError("Not enough inputs.")

            if property == "Pt_in":
                self.Pt_in["value"] = value

                if len(values) == 2:
                    self.Pt_in["unit"] = unit

                elif len(values) < 2:
                    self.Pt_in["unit"] = "kPa"
                    raise Warning("Not enough inputs: assuming kPa as units for Pt_in.")

            elif property == "Tt_in":
                self.Tt_in["value"] = value

                if len(values) == 2:
                    self.Tt_in["unit"] = unit

                if len(values) < 2:
                    self.Tt_in["unit"] = "K"
                    raise Warning("Not enough inputs: assuming K as units for Tt_in.")

            elif property == "Pressure Ratio":
                self.pressure_ratio["value"] = value

                if len(values) == 2:
                    self.pressure_ratio["unit"] = unit

                if len(values) < 2:
                    self.pressure_ratio["unit"] = ""
                    raise Warning(
                        "Not enough inputs: assuming dimensionless parameter."
                    )

            elif property == "Temperature Ratio":
                self.temperature_ratio["value"] = value

                if len(values) == 2:
                    self.temperature_ratio["unit"] = unit

                elif len(values) < 2:
                    self.temperature_ratio["unit"] = ""
                    raise Warning(
                        "Not enough inputs: assuming dimensionless parameter."
                    )

            elif property == "Polytropic Efficiency":
                self.polytropic_efficiency["value"] = value

                if len(values) == 2:
                    self.polytropic_efficiency["unit"] = unit

                elif len(values) < 2:
                    self.polytropic_efficiency["unit"] = ""
                    raise Warning("Efficiency being used as a percentage.")

            elif property == "Mechanical Efficiency":
                self.mechanical_efficiency["value"] = value

                if len(values) == 2:
                    self.mechanical_efficiency["unit"] = unit

                elif len(values) < 2:
                    self.mechanical_efficiency["unit"] = ""
                    raise Warning("Efficiency being used as a percentage.")

            elif property == "Bypass Ratio":
                self.bypass_ratio["value"] = value

                if len(values) == 2:
                    self.bypass_ratio["unit"] = unit

                elif len(values) < 2:
                    self.bypass_ratio["unit"] = ""
                    raise Warning(
                        "Not enough inputs: assuming dimensionless parameter."
                    )

            elif property == "Mach at Exit":
                self.mach_at_exit["value"] = value

                if len(values) == 2:
                    self.mach_at_exit["unit"] = unit

                elif len(values) < 2:
                    self.mach_at_exit["unit"] = ""
                    raise Warning("Using Mach as dimensionless parameter.")

            elif property == "m0":
                self.m0["value"] = value

                if len(values) == 2:
                    self.m0["unit"] = unit

                elif len(values) < 2:
                    self.m0["unit"] = "kg/s"
                    raise Warning("Not enough inputs: assuming kg/s for units")

            elif property == "mf":
                self.mf["value"] = value

                if len(values) == 2:
                    self.mf["unit"] = unit

                elif len(values) < 2:
                    self.mf["unit"] = "kg/s"
                    raise Warning("Not enough inputs: assuming kg/s for units")

            elif property == "name":
                self.name = values

    def poly_efficiency(self):
        y = 1.4

        if self.temperature_ratio["value"] > 0 and self.pressure_ratio["value"] > 0:
            self.polytropic_efficiency["value"] = (
                1 - self.temperature_ratio["value"]
            ) / (1 - (self.pressure_ratio["value"] ** ((y - 1) / y)))
            self.polytropic_efficiency["unit"] = "-"

        else:
            raise ValueError(
                "Incorrect inputs. Temperature ratio and pressure ratio required only."
            )

    def Tt_out_from_poly_efficiency(self):
        y = 1.4

        if (
            self.Tt_in["value"] > 0
            and self.pressure_ratio["value"] > 0
            and self.polytropic_efficiency["value"] > 0
        ):
            self.Tt_out["value"] = (-self.Tt_in["value"]) * self.polytropic_efficiency[
                "value"
            ] * (1 - (self.pressure_ratio["value"]) ** ((y - 1) / y)) - 1

        else:
            raise ValueError(
                "Incorrect inputs. Total temperature in (Tt_in), pressure ratio, and polytropic efficiency required only"
            )

    def Pt_out_from_poly_efficiency(self):
        y = 1.4

        if (
            self.Pt_in["value"] > 0
            and self.temperature_ratio["self"] > 0
            and self.polytropic_efficiency["self"] > 0
        ):
            self.Pt_out["value"] = self.Pt_in["value"] * (
                1
                - (
                    (1 - self.temperature_ratio["value"])
                    / self.polytropic_efficiency["value"]
                )
            ) ** (y / (y - 1))

        else:
            raise ValueError(
                "Incorrect inputs. Total pressure in (Pt_in), temperature ratio, and polytropic efficiency required only"
            )

    def ideal_Tt_out(self):
        y = 1.4

        if self.Tt_in["value"] > 0 and self.pressure_ratio["value"] > 0:
            self.Tt_out["value"] = self.Tt_in["value"] * self.pressure_ratio[
                "value"
            ] ** ((y - 1) / y)

        else:
            raise ValueError(
                "Incorrect inputs. Total temperature in (Tt_in) and pressure ratio required only."
            )

    def ideal_Pt_out(self):
        y = 1.4

        if self.Pt_in["value"] > 0 and self.temperature_ratio["value"] > 0:
            self.Pt_out["value"] = self.Pt_in["value"] * self.temperature_ratio[
                "value"
            ] ** (y / (y - 1))

        else:
            raise ValueError(
                "Incorrect inputs. Total pressure in (Pt_in) and temperature ratio required only"
            )

    # def pressure_ratio_from_poly_efficiency(self):

    def temperature_ratio_from_poly_efficiency(self):
        y = 1.4

        if self.pressure_ratio["value"] > 0 and self.poly_efficiency["value"] > 0:
            self.temperature_ratio["value"] = self.pressure_ratio["value"] ** (
                (y - 1) * self.poly_efficiency["value"] / y
            )

        else:
            raise ValueError(
                "Incorrect inputs. Pressure ratio and polytropic efficiency required only."
            )

    def static_temperature(self):
        y = 1.4

        if self.Tt_in["value"] > 0 and 

#     def turbine_Pt_out(
#         Tt_out: float, Tt_in: float, Pt_in: float, gas: gd.fluid = gd.fluids.air
#     ) -> float:
#         # Calculates the ideal total pressure after turbine

#         Pt_out = Pt_in * (Tt_out / Tt_in) ** (gas.gamma / (gas.gamma - 1))

#     def turbine_efficiency(
#         Tt_out: float,
#         Tt_in: float,
#         Pt_out: float,
#         Pt_in: float,
#         gas: gd.fluid = gd.fluids.air,
#     ) -> float:
#         # Calculates the isentropic turbine efficiency from conditions before and after turbine

#         turbine_effficiency = (1 - (Tt_out / Tt_in)) / (
#             1 - (Pt_out / Pt_in) ** ((gas.gamma - 1) / gas.gamma)
#         )

#         return turbine_efficiency

#     def turbine_Tt_out_from_efficiency(
#         efficiency: float,
#         Tt_in: float,
#         Pt_out: float,
#         Pt_in: float,
#         gas: gd.fluid = gd.fluids.air,
#     ) -> float:
#         # Calculates the temperature after turbine using isentropic efficiency

#         Tt_out = (-Tt_in) * (
#             efficiency * (1 - (Pt_out / Pt_in) ** ((gas.gamma - 1) / gas.gamma)) - 1
#         )

#         return Tt_out

#     def turbine_Pt_out_from_efficiency(
#         efficiency: float,
#         Tt_out: float,
#         Tt_in: float,
#         Pt_in: float,
#         gas: gd.fluid = gd.fluids.air,
#     ) -> float:
#         # Calculates the pressure after turbine using isentropic efficiency

#         Pt_out = Pt_in * (1 - ((1 - Tt_out / Tt_in) / efficiency)) ** (
#             gas.gamma / (gas.gamma - 1)
#         )

#         return Pt_out

#     def turbine_Tt_out(
#         Tt_in: float, Pt_out: float, Pt_in: float, gas: gd.fluid = gd.fluids.air
#     ) -> float:
#         # Calculates the ideal total temperature after turbine

#         Tt_out = Tt_in * (Pt_out / Pt_in) ** ((gas.gamma - 1) / gas.gamma)

#         return Tt_out

#     def turbine_Pt_out(
#         Tt_out: float, Tt_in: float, Pt_in: float, gas: gd.fluid = gd.fluids.air
#     ) -> float:
#         # Calculates the ideal total pressure after turbine

#         Pt_out = Pt_in * (Tt_out / Tt_in) ** (gas.gamma / (gas.gamma - 1))

#         return Pt_out
