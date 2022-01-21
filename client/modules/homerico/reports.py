
#################################################################################################################################################

# Imports
from os import getenv
from requests import post

#################################################################################################################################################

# Get Address
remote = getenv('HOMERICO_SERVICE_ADDRESS')

#################################################################################################################################################

# Homerico Reports Class
class reports:

    #################################################################################################################################################

    def relatorio_lista(
        data_inicial: str,
        data_final: str,
        id_processo: str
    ):
        res = post(
            url=f'{remote}/reports/relatorio_lista',
            json={
                'data_inicial': data_inicial,
                'data_final': data_final,
                'id_processo': id_processo
            }
        ).json()
        # Return Result
        return res['data']

    #################################################################################################################################################

    def relatorio_gerencial_report(
        data: str,
        id_report: str
    ):
        res = post(
            url=f'{remote}/reports/relatorio_gerencial_report',
            json={
                'data': data,
                'id_report': id_report
            }
        ).json()
        # Return Result
        return res['data']

    #################################################################################################################################################

    def relatorio_boletim(
        data_inicial: str,
        data_final: str,
        id_report: str
    ):
        res = post(
            url=f'{remote}/reports/relatorio_boletim',
            json={
                'data_inicial': data_inicial,
                'data_final': data_final,
                'id_report': id_report
            }
        ).json()
        # Return Result
        return res['data']

    #################################################################################################################################################

    def producao_lista(
        data_final: str,
        controle: str
    ):
        res = post(
            url=f'{remote}/reports/producao_lista',
            json={
                'data_final': data_final,
                'controle': controle
            }
        ).json()
        # Return Result
        return res['data']

    #################################################################################################################################################

    def relatorio_gerencial_registro(
        data: str,
        registro: str
    ):
        res = post(
            url=f'{remote}/reports/relatorio_gerencial_registro',
            json={
                'data': data,
                'registro': registro
            }
        ).json()
        # Return Result
        return res['data']

#################################################################################################################################################
