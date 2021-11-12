
#################################################################################################################################################

# Imports
import os
import requests

#################################################################################################################################################

# Get Address
remote = os.getenv('HOMERICO_NETWORK_ADDRESS')

#################################################################################################################################################

# RelatorioLista("01/06/2020","13/07/2020","35")
def RelatorioLista(
    dataInicial: str,
    dataFinal: str,
    idProcesso: str
):
    res = requests.post(
        url=f'{remote}/relatorioLista',
        json={
            'dataInicial': dataInicial,
            'dataFinal': dataFinal,
            'idProcesso': idProcesso
        }
    )
    # Return Result
    return res.text

#################################################################################################################################################

# RelatorioGerencialReport("01/05/2020","1")
def RelatorioGerencialReport(
    data: str,
    idReport: str
):
    res = requests.post(
        url=f'{remote}/relatorioGerencialReport',
        json={
            'data': data,
            'idReport': idReport
        }
    )
    # Return Result
    return res.text

#################################################################################################################################################

# RelatorioBoletim("01/07/2020","13/07/2020","85")
def RelatorioBoletim(
    dataInicial: str,
    dataFinal: str,
    idReport: str
):
    res = requests.post(
        url=f'{remote}/relatorioBoletim',
        json={
            'dataInicial': dataInicial,
            'dataFinal': dataFinal,
            'idReport': idReport
        }
    )
    # Return Result
    return res.text

#################################################################################################################################################

# ProducaoLista("30/04/2021","2361")
def ProducaoLista(
    dataFinal: str,
    controle: str
):
    res = requests.post(
        url=f'{remote}/producaoLista',
        json={
            'dataFinal': dataFinal,
            'controle': controle
        }
    )
    # Return Result
    return res.text

#################################################################################################################################################

# RelatorioGerencialRegistro("01/05/2020","2")
def RelatorioGerencialRegistro(
    data: str,
    registro: str
):
    res = requests.post(
        url=f'{remote}/relatorioGerencialRegistro',
        json={
            'data': data,
            'registro': registro
        }
    )
    # Return Result
    return res.text

#################################################################################################################################################
