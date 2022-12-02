# Initial
# Jose R.

# class Property():
#     def __init__(self,value,unit):
#         self.value = value
#         self.unit = unit

# class LinkPorts:
#     def __init__(self) -> None:
#         pass

def Drag():
    pass
    #Calculate Drag

def Thrust():
    pass
    # Calculate Net Thrust
    
# def LinkPort(outlet):   
#     inlet = (outlet['value'] , outlet['unit'])
    
#     return inlet

def LinkPorts(object1, object2):
    object2.Pt_in = object1.Pt_out
    object2.Tt_in = object1.Tt_out
    object2.W_in = object1.W_out
    
    object2.inlet  = object1.name
    object1.outlet = object2.name
    
    