
#################################################################################################################################################

# Imports
import requests

#################################################################################################################################################

# Class Homerico-Conexao
class HomericoConexao:

    #################################################################################################################################################
    
    def addr(self, addr: str):
        self.addr = addr
        return True

    def auth(self, user: str, password: str):
        self.auth = (user, password)
        return True

    #################################################################################################################################################

    # RelatorioLista("01/06/2020","13/07/2020","35")
    def RelatorioLista(
        self,
        dataInicial: str,
        dataFinal: str,
        idProcesso: str
    ):
        res = requests.post(
            url=f'${self.addr}/relatorioLista',
            auth=self.auth,
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
        self,
        data: str,
        registro: str
    ):
        res = requests.post(
            url=f'${self.addr}/relatorioGerencialReport',
            auth=self.auth,
            json={
                'data': data,
                'registro': registro
            }
        )
        # Return Result
        return res.text

    #################################################################################################################################################

    # RelatorioBoletim("01/07/2020","13/07/2020","85")
    def RelatorioBoletim(
        self,
        dataInicial: str,
        dataFinal: str,
        idReport: str
    ):
        res = requests.post(
            url=f'${self.addr}/relatorioBoletim',
            auth=self.auth,
            json={
                'dataInicial': dataInicial,
                'dataFinal': dataFinal,
                'idaReport': idReport
            }
        )
        # Return Result
        return res.text

    #################################################################################################################################################

    # ProducaoLista("30/04/2021","2361")
    def ProducaoLista(
        self,
        dataFinal: str,
        controle: str
    ):
        res = requests.post(
            url=f'${self.addr}/producaoLista',
            auth=self.auth,
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
        self,
        data: str,
        registro: str
    ):
        res = requests.post(
            url=f'${self.addr}/relatorioGerencialRegistro',
            auth=self.auth,
            json={
                'data': data,
                'registro': registro
            }
        )
        # Return Result
        return res.text

#################################################################################################################################################
