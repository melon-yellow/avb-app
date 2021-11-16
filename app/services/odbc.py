
#################################################################################################################################################

# Imports
import os
import requests

#################################################################################################################################################

# Get Address
remote = os.getenv('ODBC_SERVICE_ADDRESS')

#################################################################################################################################################

# SAP
class sap:

    def preditivas(equip: list[str]):
        if not isinstance(equip, list): raise Exception('invalid argument "equip"')
        if not all(isinstance(i, str) for i in equip): raise Exception('invalid argument "equip"')
        res = requests.post(
            url=f'{remote}/sap/preditivas/',
            json={ 'equip': equip }
        )
        res.raise_for_status()
        return res.json()

#################################################################################################################################################

# Aciaria
class aciaria:

    class ld:

        def espectrometro():
            res = requests.get(
                url=f'{remote}/aciaria/ld/espectrometro/',
            )
            res.raise_for_status()
            return res.json()
    
    class fp:

        def espectrometro():
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
