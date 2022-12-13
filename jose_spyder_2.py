import gas_dynamics as gd
from compressor import Compressor
from burner     import Burner


Cmp20 = Compressor(name='Cmp20',eff_poly = {'value': 0.9, 'units': '-'}, PR = {'value': 20., 'units': '-'})
Brn30 = Burner(name='Brn30',eff_poly = {'value': 0.9, 'units': '-'}, PR = {'value': 20., 'units': '-'})

