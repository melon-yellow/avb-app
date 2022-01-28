
#################################################################################################################################################

# Imports
from asyncio import gather

# Modules
from .helpers import num
from .homerico import relatorio_gerencial_registro

#################################################################################################################################################

async def rendimento():
    try:
        (
            (ok1, rend),
            (ok2, carg)
        ) = await gather(
            relatorio_gerencial_registro(registro=15),
            relatorio_gerencial_registro(registro=1218)
        )
        # Check Response
        if not ok1: raise rend
        if not ok2: raise carg
        # Assembly Data
        data: dict[str, float] = {
            'rendimento': None, 'carga_solida': None
        }
        if (
            isinstance(rend, list) and
            (len(rend) >= 2) and
            isinstance(rend[1], list) and
            (len(rend[1]) >= 3) and
            isinstance(rend[1][2], str)
        ):
            data.update({'rendimento': num(rend[1][2])})
        if (
            isinstance(carg, list) and
            (len(carg) >= 2) and
            isinstance(carg[1], list) and
            (len(carg[1]) >= 3) and
            isinstance(carg[1][2], str)
        ):
            data.update({'carga_solida': num(carg[1][2])})
        # Return Data
        return (True, data)
    except Exception as error:
        return (False, error)

#################################################################################################################################################
