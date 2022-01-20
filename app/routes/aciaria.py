
#################################################################################################################################################

# Imports
import json
import flask
import py_misc

# modules
from ..helpers import homerico
from ..services import odbc

#################################################################################################################################################

Request = flask.Request
Response = flask.Response

#################################################################################################################################################

# Load Routes
def __load__(app: py_misc.express.Express):

    ##########################################################################################################################

    @app.route('/avb/aciaria/ld/espectrometro/')
    def aciariaLDEspectrometro(req: Request, res: Response):
        data = odbc.aciaria.ld.espectrometro()
        return res(
            json.dumps(data),
            mimetype='application/json',
            status=200
        )

    ##########################################################################################################################

    @app.route('/avb/aciaria/fp/espectrometro/')
    def aciariaFPEspectrometro(req: Request, res: Response):
        data = odbc.aciaria.fp.espectrometro()
        return res(
            json.dumps(data),
            mimetype='application/json',
            status=200
        )

    #################################################################################################################################################

    @app.route('/avb/aciaria/rendimento/')
    def aciariaRendimento(req: Request, res: Response):
        try:
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

            # Set Data
            data = {
                'rendimento': rendimento,
                'carga_solida': carga_solida
            }

            # Return data
            return res(
                json.dumps(data),
                mimetype='application/json',
                status=200
            )
    
        except Exception as e:

            # Return data
            return res(
                json.dumps({ "error": f'{e}' }),
                mimetype='application/json',
                status=200
            )

#################################################################################################################################################
