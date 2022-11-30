# Initial

# Import Packages:
import gas_dynamics as gd

class Compressor:
    def __init__(self, **kwargs):
        for property, value, unit in kwargs:
            if property == "Pt_in":
                Pt_in.value = value
                Pt_in.unit = unit

            elif property == "Tt_in":
                Tt_in.value = value
                Tt_in.unit = unit

            elif property == "W_in":
                W_in.value = value
                W_in.unit = unit

            
        self._Pt_in.value = Pt_in.value
        self._Tt_in.value = Tt_in.value
        self._W_in.value  = W_in.value

        self._Pt_in.unit = Pt_in.unit
        self._Tt_in.unit = Tt_in.unit
        self._W_in.unit  = W_in.unit


    def __str__(self) -> str:
        print('Compressor class')
        
    @property
    def Pt_in(self):
        return self._Pt_in

    def Tt_in(self):
        return self._Tt_in

    def W_in(self):
        return self._W_in

    @Pt_in.setter
    def Pt_in(self, Pt_in):
        if Pt_in < 0:
            raise ValueError(f"{self.name} error; Pt_in < 0")

    @Tt_in.setter
    def Pt_in(self, Pt_in):
        if self.units == "SI" and self.Tt_in < -273.15:
            raise ValueError(f"{self.name} error; Tt_in < 0 K")
        elif self.units == "FPS" and self.Tt_in < -273.15:
            raise ValueError(f"{self.name} error; Tt_in < 0 K")

