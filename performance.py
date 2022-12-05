import MATLAB_calc as MATLAB

def gross_thrust(W, u):
    
    Fg = = {"value": 0.0, "units": "-"}
    Fg['value'] = W['value'] * u['value']
    Fg['units'] = W['value'] + ' ' + u['value']
    
    return Fg

def ram_drag(W, u):
    
    Dram = = {"value": 0.0, "units": "-"}
    Dram['value'] = W['value'] * u['value']
    Dram['units'] = W['value'] + ' ' + u['value']
    
    return Dram