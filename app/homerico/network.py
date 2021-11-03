
#################################################################################################################################################

# Imports
import requests

#################################################################################################################################################

# Class Homerico-Conexao
class HomericoConexao:

    #################################################################################################################################################
    
    def addr(self, addr: str):
        self.__addr__ = addr
        return True

    def auth(self, user: str, password: str):
        self.__auth__ = (user, password)
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
            url=f'{self.__addr__}/relatorioLista',
            auth=self.__auth__,
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
        idReport: str
    ):
        res = requests.post(
            url=f'{self.__addr__}/relatorioGerencialReport',
            auth=self.__auth__,
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
        self,
        dataInicial: str,
        dataFinal: str,
        idReport: str
    ):
        res = requests.post(
            url=f'{self.__addr__}/relatorioBoletim',
            auth=self.__auth__,
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
        self,
        dataFinal: str,
        controle: str
    ):
        res = requests.post(
            url=f'{self.__addr__}/producaoLista',
            auth=self.__auth__,
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
            url=f'{self.__addr__}/relatorioGerencialRegistro',
            auth=self.__auth__,
            json={
                'data': data,
                'registro': registro
            }
        )
        # Return Result
        return res.text

#################################################################################################################################################
