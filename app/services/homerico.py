
#################################################################################################################################################

# Imports
import os
import requests

#################################################################################################################################################

# Get Address
remote = os.getenv('HOMERICO_SERVICE_ADDRESS')

#################################################################################################################################################

def relatorio_lista(
    data_inicial: str,
    data_final: str,
    id_processo: str
):
    res = requests.post(
        url=f'{remote}/relatorio_lista',
        json={
            'data_inicial': data_inicial,
            'data_final': data_final,
            'id_processo': id_processo
        }
    )
    # Return Result
    return res.json()['data']

#################################################################################################################################################

def relatorio_gerencial_report(
    data: str,
    id_report: str
):
    res = requests.post(
        url=f'{remote}/relatorio_gerencial_report',
        json={
            'data': data,
            'id_report': id_report
        }
    )
    # Return Result
    return res.json()['data']

#################################################################################################################################################

def relatorio_boletim(
    data_inicial: str,
    data_final: str,
    id_report: str
):
    res = requests.post(
        url=f'{remote}/relatorio_boletim',
        json={
            'data_inicial': data_inicial,
            'data_final': data_final,
            'id_report': id_report
        }
    )
    # Return Result
    return res.json()['data']

#################################################################################################################################################

def producao_lista(
    data_final: str,
    controle: str
):
    res = requests.post(
        url=f'{remote}/producao_lista',
        json={
            'data_final': data_final,
            'controle': controle
        }
    )
    # Return Result
    return res.json()['data']

#################################################################################################################################################

def relatorio_gerencial_registro(
    data: str,
    registro: str
):
    res = requests.post(
        url=f'{remote}/relatorio_gerencial_registro',
        json={
            'data': data,
            'registro': registro
        }
    )
    # Return Result
    return res.json()['data']

#################################################################################################################################################
