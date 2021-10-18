import ctypes
import os

#################################################################################################################################################

#Informa o caminho da dll
file_dir = os.path.dirname(__file__)
dll_path = ''.join([file_dir, '\homerico_python64bits'])
MyDllObject = ctypes.cdll.LoadLibrary(dll_path)

#################################################################################################################################################

# Metodo Validar
Validar = MyDllObject.Validar
Validar.restype = ctypes.c_wchar_p
Validar.argtypes = [ctypes.c_wchar_p]
# Validar("homerico.avb" | "avb")

# Metodo Login
Login = MyDllObject.Login
Login.restype = ctypes.c_wchar_p
Login.argtypes = [ctypes.c_wchar_p,ctypes.c_wchar_p]
# Login(<USUARIO>, <SENHA>)

#################################################################################################################################################

RelatorioLista = MyDllObject.RelatorioLista
RelatorioLista.restype = ctypes.c_wchar_p
RelatorioLista.argtypes = [ctypes.c_wchar_p,ctypes.c_wchar_p,ctypes.c_wchar_p]
# RelatorioLista("01/06/2020","13/07/2020","35")

RelatorioGerencialReport = MyDllObject.RelatorioGerencialReport
RelatorioGerencialReport.restype = ctypes.c_wchar_p
RelatorioGerencialReport.argtypes = [ctypes.c_wchar_p,ctypes.c_wchar_p]
# RelatorioGerencialReport("01/05/2020","1")

RelatorioBoletim = MyDllObject.RelatorioBoletim
RelatorioBoletim.restype = ctypes.c_wchar_p
RelatorioBoletim.argtypes = [ctypes.c_wchar_p,ctypes.c_wchar_p]
# RelatorioBoletim("01/07/2020","13/07/2020","85")

ProducaoLista = MyDllObject.ProducaoLista
ProducaoLista.restype = ctypes.c_wchar_p
ProducaoLista.argtypes = [ctypes.c_wchar_p,ctypes.c_wchar_p]
# ProducaoLista("30/04/2021","2361"))

RelatorioGerencialRegistro = MyDllObject.RelatorioGerencialRegistro
RelatorioGerencialRegistro.restype = ctypes.c_wchar_p
RelatorioGerencialRegistro.argtypes = [ctypes.c_wchar_p,ctypes.c_wchar_p]
# RelatorioGerencialRegistro("01/05/2020","2")

#################################################################################################################################################

