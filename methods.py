# Initial
# Jose R.

class Property():
    def __init__(self,value,unit):
        self.value = value
        self.unit = unit

# class LinkPorts:
#     def __init__(self) -> None:
#         pass

def Drag():
    pass
    #Calculate Drag

def Thrust():
    pass
    # Calculate Net Thrust
    
def LinkPort(outlet):
    
    inlet = (outlet['value'] , outlet['unit'])
    
    return inlet