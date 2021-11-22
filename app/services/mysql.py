
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

    def utilizacao():
        res = requests.get(
            url=f'{remote}/trefila/utilizacao/',
        )
        res.raise_for_status()
        return res.text

    class metas:

        def utilizacao():
            res = requests.get(
                url=f'{remote}/trefila/metas/utilizacao/',
            )
            res.raise_for_status()
            return res.json()

        def custo():
            res = requests.get(
                url=f'{remote}/trefila/metas/custo/',
            )
            res.raise_for_status()
            return res.json()

        def sucata():
            res = requests.get(
                url=f'{remote}/trefila/metas/sucata/',
            )
            res.raise_for_status()
            return res.json()

        def cincos():
            res = requests.get(
                url=f'{remote}/trefila/metas/cincos/',
            )
            res.raise_for_status()
            return res.json()

#################################################################################################################################################
