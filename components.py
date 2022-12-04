# Initial
# Jose R.

# Import Major Components

from inlet import Inlet  # Added, Noah C. Dec 3
from fan import Fan  # Added, Noah C. Dec 3
from compressor import Compressor    from burner import Burner  # Added, Noah C. Dec 3
from turbine import Turbine  # Added, Noah C. Dec 3
from mixer import Mixer  # Added, Noah C. Dec 3
from nozzle import Nozzle  # Added, Noah C. Dec 3



# Define component names
# "Freestream = 00"


def configuration(name=str):

    Int10 = Inlet(name="Int10")
    Fan20 = Fan(name="Fan20")
    Cmp30 = Compressor(name="Cmp30")
    Brn40 = Burner(name="Brn40")
    Trb50 = Turbine(name="Trb50")
    Mix60 = Mixer(name="Mix60")
    Noz70 = Nozzle(name="Noz70")

    return Int10, Fan20, Cmp30, Brn40, Trb50, Mix60, Noz70


# "Freestream = 80"


# Define Other Components
class Shaft:
    def __init__(self) -> None:
        pass


class Duct:
    def __init__(self) -> None:
        pass
