
#################################################################################################################################################

# Imports
import os
import requests

#################################################################################################################################################

# Get Address
remote = os.getenv('ODBC_SERVICE_ADDRESS')

#################################################################################################################################################


# Aciaria
class aciaria:

    def espectrometroLD():
        res = requests.get(
            url=f'{remote}/aciaria/ld/espectrometro/',
        )
        res.raise_for_status()
        return res.json()

    def espectrometroFP():
        res = requests.get(
            url=f'{remote}/aciaria/fp/espectrometro/',
        )
        res.raise_for_status()
        return res.json()

#################################################################################################################################################

# Laminador
class laminador:

    def produto():
        res = requests.get(
            url=f'{remote}/laminador/produto/',
        )
        res.raise_for_status()
        return res.json()

    def blbp():
        res = requests.get(
            url=f'{remote}/laminador/blbp/',
        )
        res.raise_for_status()
        return res.json()

    def rfa():
        res = requests.get(
            url=f'{remote}/laminador/rfa/',
        )
        res.raise_for_status()
        return res.json()

    def rfal2():
        res = requests.get(
            url=f'{remote}/laminador/rfal2/',
        )
        res.raise_for_status()
        return res.json()

#################################################################################################################################################
