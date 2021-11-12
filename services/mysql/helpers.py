
#################################################################################################################################################

# Imports
import os
import requests
import datetime

#################################################################################################################################################

# Get Address
remoteApp = os.getenv('AVB_APP_NETWORK_ADDRESS')

#################################################################################################################################################

# Get Escala Turno
def escalaTurno(
    data: datetime.datetime = None,
    referencia: dict[str,tuple[str,str,str,str]] = None
):
    res = requests.post(
        url=f'{remoteApp}/laminador/escalaTurno',
        json={
            'data': data,
            'referencia': referencia
        }
    )
    # Return Result
    return res.json()

#################################################################################################################################################

# Get Last Day Of Month
def lastDayOfMonth(date: datetime.datetime):
    if date.month == 12: return date.replace(day=31)
    return (
        date.replace(month=(date.month + 1), day=1) -
        datetime.timedelta(days=1)
    )

#################################################################################################################################################
