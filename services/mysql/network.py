
#################################################################################################################################################

# Imports
import os
import requests
import datetime

#################################################################################################################################################

# Get Address
remote = os.getenv('AVB_APP_NETWORK_ADDRESS')

#################################################################################################################################################

# Get Escala Turno
def escalaTurno(
    data: datetime.datetime = None,
    referencia: dict[str,tuple[str,str,str,str]] = None
):
    res = requests.post(
        url=f'{remote}/laminador/escalaTurno',
        json={
            'data': data,
            'referencia': referencia
        }
    )
    # Return Result
    return res.json()

#################################################################################################################################################
