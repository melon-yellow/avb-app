
#################################################################################################################################################

# Imports
import os
import ctypes

#################################################################################################################################################

# Informa o caminho da dll
fileDir = os.path.dirname(os.path.abspath(__file__))
dllPath = os.path.abspath(os.path.join(fileDir, './HomericoPython64.dll'))
HomericoPython64 = ctypes.cdll.LoadLibrary(dllPath)

#################################################################################################################################################

# Metodo Validar
Validar = HomericoPython64.Validar
Validar.restype = ctypes.c_wchar_p
Validar.argtypes = [ctypes.c_wchar_p]
# Validar("homerico.avb" | "avb")

# Metodo Login
Login = HomericoPython64.Login
Login.restype = ctypes.c_wchar_p
Login.argtypes = [ctypes.c_wchar_p,ctypes.c_wchar_p]
# Login(<USUARIO>, <SENHA>)

#################################################################################################################################################

RelatorioLista = HomericoPython64.RelatorioLista
RelatorioLista.restype = ctypes.c_wchar_p
RelatorioLista.argtypes = [ctypes.c_wchar_p,ctypes.c_wchar_p,ctypes.c_wchar_p]
# RelatorioLista("01/06/2020","13/07/2020","35")

RelatorioGerencialReport = HomericoPython64.RelatorioGerencialReport
RelatorioGerencialReport.restype = ctypes.c_wchar_p
RelatorioGerencialReport.argtypes = [ctypes.c_wchar_p,ctypes.c_wchar_p]
# RelatorioGerencialReport("01/05/2020","1")

RelatorioBoletim = HomericoPython64.RelatorioBoletim
RelatorioBoletim.restype = ctypes.c_wchar_p
RelatorioBoletim.argtypes = [ctypes.c_wchar_p,ctypes.c_wchar_p]
# RelatorioBoletim("01/07/2020","13/07/2020","85")

ProducaoLista = HomericoPython64.ProducaoLista
ProducaoLista.restype = ctypes.c_wchar_p
ProducaoLista.argtypes = [ctypes.c_wchar_p,ctypes.c_wchar_p]
# ProducaoLista("30/04/2021","2361"))

RelatorioGerencialRegistro = HomericoPython64.RelatorioGerencialRegistro
RelatorioGerencialRegistro.restype = ctypes.c_wchar_p
RelatorioGerencialRegistro.argtypes = [ctypes.c_wchar_p,ctypes.c_wchar_p]
# RelatorioGerencialRegistro("01/05/2020","2")

#################################################################################################################################################
