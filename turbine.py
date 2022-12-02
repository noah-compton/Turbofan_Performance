# Date    | Description of Changes:                          | Author
# ----------------------------------------------------------------------------
# Dec 2   | Added comments                                   | Jose R.
#         | Downstream station needs:                        |
#         |  - Static P and T exiting Turbine                |
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

# .gamma .R .cp

import gas_dynamics as gd
import math

global y
y = gd.fluids.air.gamma


class Turbine:
    def _init_(self, **kwargs):

        initial = {"value": 0.0, "unit": "-"}

        self.name = ""

        # Inlet                                     Dec 2; JR Comment
        self.Pt_in = initial.copy()
        self.Tt_in = initial.copy()

        # Outlet
        self.Pt_out = initial.copy()
        self.Tt_out = initial.copy()
        self.P_out = initial.copy()                # Parameters
        # P5 = Pt5*(((Tt5/T5)**(y/(y-1)))**-1)     #
        self.T_out = initial.copy()                #
        # T5 = Tt5*((1+0.5*(y-1)*M5**2)**-1)       # Mixer needed
        self.a_out = initial.copy()                # Speed of sound at exit

        # Characteristics                            
        self.PR = initial.copy()                     # Pressure Ratio
        self.TR = initial.copy()                     # Temperature Ratio
        self.eff_poly = initial.copy()               # Polytropic efficiency
        self.eff_mech = initial.copy()               # Mechanicsal efficiency
        self.BPR = initial.copy()                    # BPR -> bypass ratio
        self.XMN_out = initial.copy()                # Mach out
        self.W_core = initial.copy()                 # 
        self.W_f = initial.copy()                    # W_f -> fuel flow


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
                    self.Pt_in["units"] = unit

                elif len(values) < 2:
                    self.Pt_in["units"] = "kPa"
                    raise Warning("Not enough inputs: assuming kPa as units for Pt_in.")

            elif property == "Tt_in":
                self.Tt_in["value"] = value

                if len(values) == 2:
                    self.Tt_in["units"] = unit

                if len(values) < 2:
                    self.Tt_in["units"] = "K"
                    raise Warning("Not enough inputs: assuming K as units for Tt_in.")

            elif property == "PR":
                self.PR["value"] = value

                if len(values) == 2:
                    self.PR["unit"] = unit

                if len(values) < 2:
                    self.PR["units"] = ""
                    raise Warning(
                        "Not enough inputs: assuming dimensionless parameter."
                    )

            elif property == "TR":
                self.TR["value"] = value

                if len(values) == 2:
                    self.TR["units"] = unit

                elif len(values) < 2:
                    self.TR["units"] = ""
                    raise Warning(
                        "Not enough inputs: assuming dimensionless parameter."
                    )

            elif property == "eff_poly":
                self.eff_poly["value"] = value

                if len(values) == 2:
                    self.eff_poly["units"] = unit

                elif len(values) < 2:
                    self.eff_poly["units"] = ""
                    raise Warning("Efficiency being used as a percentage.")

            elif property == "eff_mech":
                self.eff_mech["value"] = value

                if len(values) == 2:
                    self.eff_mech["units"] = unit

                elif len(values) < 2:
                    self.eff_mech["units"] = ""
                    raise Warning("Efficiency being used as a percentage.")

            elif property == "BPR":
                self.BPR["value"] = value

                if len(values) == 2:
                    self.BPR["units"] = unit

                elif len(values) < 2:
                    self.BPR["units"] = ""
                    raise Warning(
                        "Not enough inputs: assuming dimensionless parameter."
                    )

            elif property == "Mach at Exit":
                self.mach_at_exit["value"] = value

                if len(values) == 2:
                    self.mach_at_exit["units"] = unit

                elif len(values) < 2:
                    self.mach_at_exit["units"] = ""
                    raise Warning("Using Mach as dimensionless parameter.")

            elif property == "W_core":
                self.m0["value"] = value

                if len(values) == 2:
                    self.m0["units"] = unit

                elif len(values) < 2:
                    self.m0["units"] = "kg/s"
                    raise Warning("Not enough inputs: assuming kg/s for units")

            elif property == "W_f":
                self.mf["value"] = value

                if len(values) == 2:
                    self.mf["units"] = unit

                elif len(values) < 2:
                    self.mf["units"] = "kg/s"
                    raise Warning("Not enough inputs: assuming kg/s for units")

            elif property == "name":
                self.name = values

            else:
                raise ValueError("Incorrect inputs!")


    def poly_efficiency(self):
        y = 1.4

        if self.temperature_ratio["value"] > 0 and self.pressure_ratio["value"] > 0:
            self.polytropic_efficiency["value"] = (
                1 - self.temperature_ratio["value"]
            ) / (1 - (self.pressure_ratio["value"] ** ((y - 1) / y)))
            self.polytropic_efficiency["units"] = "-"

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
