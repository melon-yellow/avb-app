
#################################################################################################################################################

# Imports
import os
import requests

#################################################################################################################################################

# Get Address
remote = os.getenv('MYSQL_SERVICE_ADDRESS')

#################################################################################################################################################

# Trefila
class trefila:

    def utilizacaoTurno():
        res = requests.get(
            url=f'{remote}/trefila/utilizacao/turno/',
        )
        res.raise_for_status()
        return res.json()
    
    def utilizacao():
        res = requests.get(
            url=f'{remote}/trefila/utilizacao/',
        )
        res.raise_for_status()
        return res.json()
    
    def custo():
        res = requests.get(
            url=f'{remote}/trefila/custo/',
        )
        res.raise_for_status()
        return res.json()

    def sucata():
        res = requests.get(
            url=f'{remote}/trefila/sucata/',
        )
        res.raise_for_status()
        return res.json()
    
    def cincos():
        res = requests.get(
            url=f'{remote}/trefila/cincos/',
        )
        res.raise_for_status()
        return res.json()

#################################################################################################################################################
