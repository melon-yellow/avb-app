
#################################################################################################################################################

# Imports
from os import getenv
from requests import post
from datetime import datetime, timedelta

#################################################################################################################################################

# Get Address
remote = getenv('CLIENT_ADDRESS')

#################################################################################################################################################

# Get Escala Turno
def escalaTurno(
    data: datetime = None,
    referencia: dict[str,tuple[str,str,str,str]] = None
):
    res = post(
        url=f'{remote}/laminador/escalaTurno',
        json={
            'data': data,
            'referencia': referencia
        }
    )
    # Return Result
    return res.json()

#################################################################################################################################################

# Get Last Day Of Month
def lastDayOfMonth(date: datetime):
    if date.month == 12: return date.replace(day=31)
    return (
        date.replace(month=(date.month + 1), day=1) -
        timedelta(days=1)
    )

#################################################################################################################################################
