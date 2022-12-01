# Initial

# Import Packages:
import gas_dynamics as gd
from methods import Property

class Compressor:
    def __init__(self, **kwargs):
        for property in kwargs:
            values = kwargs[property]
            
            append = Property()
            
            if len(values) >= 2:
                append.value = values[0]
                append.unit = values[1]
                
            elif len(values) == 1:
                append.value = values[0]
                append.unit = ''
            
            else:
                raise ValueError('Not enough inputs')
                

            if property == "Pt_in":
                self.Pt_in = append
                
                if len(values) < 2:
                    self.Pt_in.unit = "kPa"
                    raise Warning("Pt_in has not enough inputs, assuming kPa for units")   
                
            elif property == "Tt_in":
                self.Tt_in = append
                
                if len(values) < 2:
                    self.Tt_in.unit = "K"
                    raise Warning("Tt_in has not enough inputs, assuming K for units")   
                
            elif property == "W_in":
                self.W_in = append
                
                if len(values) < 2:
                    self.W_in.unit = "lbm/s"
                    raise Warning("W_in has not enough inputs, assuming lbm/s for units")   

            elif property == "pi_c":
                self.pi_c = append
                
                if len(values) < 2:
                    self.pi_c.unit = "-"
                    raise Warning("pi_c has not enough inputs, assuming value is dimensionless")        

            elif property == "t_c":
                self.t_c = append
                
                if len(values) < 2:
                    self.t_c.unit = "-"
                    raise Warning("t_c has not enough inputs, assuming value is dimensionless")        
                    
            elif property == "name":
                self.name = values
    
    def compressor_calculations(self):
        if hasattr(self, 'pi_c') and hasattr(self, "t_c"):
            # Calculate Efficiency
            pass
        elif hasattr(self, 'pi_c') and hasattr(self, "e_c"):
            # Calculate Pressure Ratio
            pass
        elif hasattr(self, 't_c') and hasattr(self, "e_c"):
            # Calculate Temperature Ratio
            pass
        else:
            raise ValueError("Not enough compressor characteristics were defined, check input")

    compressor_calculations()

    def __str__(self): 
        str = f"{self.name} Characteristics:\n" \
              f"Efficiency:\n" \
              f"Pressure Ratio:\n"
        return str


