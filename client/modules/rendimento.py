
#################################################################################################################################################

from . import homerico

#################################################################################################################################################

def aciaria():
    # get app data
    rend = homerico.RelatorioGerencialRegistro(registro=15)
    carg_s = homerico.RelatorioGerencialRegistro(registro=1218)
    
    rendimento = None
    carga_solida = None

    try:
        if (not isinstance(rend, list)
            or not len(rend) >= 2
            or not isinstance(rend[1], list)
            or not len(rend[1]) >= 3
            or not isinstance(rend[1][2], str)
            ): raise Exception('homerico report "15" is invalid')
        rendimento = float(rend[1][2].replace(',', '.'))
    except: pass
    try:
        if (not isinstance(carg_s, list)
            or not len(carg_s) >= 2
            or not isinstance(carg_s[1], list)
            or not len(carg_s[1]) >= 3
            or not isinstance(carg_s[1][2], str)
            ): raise Exception('homerico report "1218" is invalid')
        carga_solida = float(carg_s[1][2].replace(',', '.'))
    except: pass

    # Return Data
    return {
        'rendimento': rendimento,
        'carga_solida': carga_solida
    }

#################################################################################################################################################
