# fan
# Isabel H
# need to define __str__

import gas_dynamics as gd

global y
y = gd.fluids.air.gamma

class Fan:
        """A model for describing the characterisics of a fan"""

    def __init__(self, **kwargs):
        """Initializes a Fan class to define flow changes within the stage.
                Parameters:
                Parameters are characterized by a dictionary with 2 keys and values to maintain a quantitative and qualitative description.
                The form of the parameters is such: {"value": 0.0, "units": "str"}
                Example: self.Pt_in = {"value": 1000, "units": "kPa"}

            Pt_in            (dict):     Inlet total pressure.
            Tt_in            (dict):     Inlet total temperature.
            W_in             (dict):     Incoming mass flow rate.
            Pt_out1          (dict):     Outgoing port 1 total pressure.
            Pt_out2          (dict):     Outgoing port 2 total pressure.
            Tt_out1          (dict):     Outgoing port 1 total temperature.
            Tt_out2          (dict):     Outgoing port 2 total temperature.
            W_out1           (dict):     Outgoing port 1 mass flow.
            W_out2           (dict):     Outgoing port 2 mass flow.
            BPR              (dict):     Bypass ratio.
            PR               (dict):     Pressure ratio across the fan.
            TR               (dict):     Temperature ratio across the fan.
            eff_poly         (dict):     Polytropic efficiency.
            
            """
        init = {'value': 0., 'units': '-'}
        
        self.name   = ''
        self.inlet = ''
        self.outlet = ''
    
        #Inlet
        self.Pt_in = init.copy()
        self.Tt_in = init.copy()
        self.W_in = init.copy()

        #Outlet
        self.Pt_out1 = init.copy()
        self.Pt_out2 = init.copy()
        self.Tt_out1 = init.copy()
        self.Tt_out2 = init.copy()
        self.W_out1 = init.copy()
        self.W_out2 = init.copy()

        #Characteristics
        self.BPR = init.copy()
        self.TR = init.copy()    # TR
        self.PR = init.copy()   # PR
        self.eff_poly = init.copy()     # eff_poly

        for property in kwargs:

            values = kwargs[property]

            if len(values) >= 2:
                value = values[0]
                units = values[1]
                
            elif len(values) == 1:
                value = values[0]
                units = ''
            
            else:
                raise ValueError('Not enough inputs')

            
            if property == "Pt_in":
                self.Pt_in['value'] = value

                if len(values) == 2:
                    self.Pt_in["units"] = units

                elif len(values) < 2:
                    self.Pt_in['units'] = 'Pa'
                    raise Warning("Not enough inputs: assuming Pa for units for Pt_in")
            
            elif property == "Tt_in":
                 self.Tt_in["value"] = value

                 if len(values) == 2:
                    self.Tt_in["units"] = units

                 elif len(values) < 2:
                        self.Tt_in["units"] = "K"
                        raise Warning("Not enough inputs: assuming K for units for Tt_in ")
            
            elif property == "TR":
                 self.TR["value"] = value

                 if len(values) == 2:
                    self.TR["units"] = units

                 elif len(values) < 2:
                        self.TR["units"] = ""
                        raise Warning("Not enough inputs: assuming dimensionless parameter")
            
            elif property == "PR":
                 self.PR["value"] = value

                 if len(values) == 2:
                    self.PR["units"] = units

                 elif len(values) < 2:
                        self.PR["units"] = ""
                        raise Warning("Not enough inputs: assuming dimensionless parameter")
            
            elif property == "eff_poly":
                 self.eff_poly["value"] = value

                 if len(values) == 2:
                    self.eff_poly["units"] = units

                 elif len(values) < 2:
                        self.eff_poly["units"] = ""
                        raise Warning("Not enough inputs: assuming dimensionless parameter")
                        
            elif property == "BPR":
                 self.BPR["value"] = value

                 if len(values) == 2:
                    self.BPR["units"] = units

                 elif len(values) < 2:
                        self.BPR["units"] = ""
                        raise Warning("Not enough inputs: assuming dimensionless parameter")
           
            elif property == "name":
                self.name = values
                
    def mass_conservation(self):
        self.W_out1['value'] =  self.W_in['value'] / (self.BPR['value'] + 1)
        self.W_out2['value'] =  self.W_in['value'] - self.W_out1['value']

        self.W_out1['units'] =  self.W_in['units']
        self.W_out2['units'] =  self.W_in['units']


    def calc(self):
        if (self.Pt_in["value"] > 0 and self.Tt_in["value"] > 0):
             pass
        else:
             raise ValueError("Incorrect inputs for inlet: nonzero values required for Pt_in and Tt_in")
        
        #values
        self.TR["value"] = (self.PR["value"] ** ((y - 1)/(y*self.eff_poly["value"])))
        self.Pt_out1["value"] = self.PR["value"] * self.Pt_in["value"]
        self.Pt_out2["value"] = self.PR["value"] * self.Pt_in["value"]
        self.Tt_out1["value"] = self.TR["value"] * self.Tt_in["value"]
        self.Tt_out2["value"] = self.TR["value"] * self.Tt_in["value"]

        #units
        self.TR["units"] =''
        self.Pt_out1["units"] = self.Pt_in["units"]
        self.Pt_out2["units"] = self.Pt_in["units"]
        self.Tt_out1["units"] = self.Tt_in["units"]
        self.Tt_out2["units"] = self.Tt_in["units"]
        self.W_out1["units"]  = self.W_in["units"] 
        self.W_out2["units"]  = self.W_in["units"] 


    def __str__(self):
        str = f"{self.name} Characteristics:\n"
        

