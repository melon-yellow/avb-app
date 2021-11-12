
#################################################################################################################################################

# Imports
import json
import flask
import py_misc

# modules
from ..helpers import homerico

#################################################################################################################################################

Request = flask.Request
Response = flask.Response

#################################################################################################################################################

# Load Routes
def __load__(app: py_misc.Express):

    #################################################################################################################################################

    @app.route('/avb/aciaria/rendimento/')
    def aciariaRendimento(req: Request, res: Response):
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
                ): raise Exception('?')
            rendimento = float(rend[1][2].replace(',', '.'))
        except: pass

        try:
            if (not isinstance(carg_s, list)
                or not len(carg_s) >= 2
                or not isinstance(carg_s[1], list)
                or not len(carg_s[1]) >= 3
                or not isinstance(carg_s[1][2], str)
                ): raise Exception('?')
            carga_solida = float(carg_s[1][2].replace(',', '.'))
        except: pass
        # Set Data
        data = dict(
            rendimento = rendimento,
            carga_solida = carga_solida
        )
        # Return data
        return res(
            json.dumps(data),
            mimetype='application/json',
            status=200
        )

#################################################################################################################################################
