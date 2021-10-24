
#################################################################################################################################################

# Imports
import py_misc

# modules
from . import avbot
from . import aciaria
from . import laminador
from . import trefila
from . import turno
from .. import homerico

#################################################################################################################################################

# Load Modules
def __load__(api: py_misc.API, h: homerico):
    avbot.__load__(api)
    aciaria.__load__(api, h)
    laminador.__load__(api, h)
    trefila.__load__(api, h)
    turno.__load__(api)

#################################################################################################################################################
