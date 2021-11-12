
#################################################################################################################################################

# Imports
import os
import requests

#################################################################################################################################################

# Get Address
remote = os.getenv('HOMERICO_NETWORK_ADDRESS')

#################################################################################################################################################

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
