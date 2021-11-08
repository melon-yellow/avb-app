
#################################################################################################################################################

# Imports
import py_misc

# modules
from . import avbot
from . import aciaria
from . import laminador
from . import trefila
from . import turno

#################################################################################################################################################

# Load Modules
def __load__(app: py_misc.Express):
    avbot.__load__(app)
    aciaria.__load__(app)
    laminador.__load__(app)
    trefila.__load__(app)
    turno.__load__(app)

#################################################################################################################################################
