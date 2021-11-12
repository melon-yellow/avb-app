
#################################################################################################################################################

# Imports
import json
import flask
import py_misc

# Modules
from ..helpers import homerico
from ..helpers import trefila
from ..helpers import util
from ..services import mysql

#################################################################################################################################################

Request = flask.Request
Response = flask.Response

#################################################################################################################################################

# Load Routes
def __load__(app: py_misc.Express):

    #################################################################################################################################################

    @app.route('/avb/trefila/producao/')
    def trefilaProducao(req: Request, res: Response):
        # read prod
        data = homerico.ProducaoLista(lista=2361)
        return res(
            json.dumps(data),
            mimetype='application/json',
            status=200
        )

    #################################################################################################################################################

    @app.route('/avb/trefila/utilizacao/csv/')
    def trefilaUtilizacaoCsv(req: Request, res: Response):
        # MySQL Connection
        csv = mysql.trefila.utilizacao()
        # Retrun Data
        return res(
            csv,
            mimetype='text/csv',
            headers={
                'Content-disposition': (
                    'attachment; filename=utilizacao.csv'
                )
            },
            status=200
        )

    #################################################################################################################################################

    @app.route('/avb/trefila/produtividade/')
    def trefilaProdutividade(req: Request, res: Response):
        # get date
        data = trefila.producaoMaquinas()
        # get util data
        utilTrefila = util.read.trefila()
        data.update({
            's': utilTrefila.get('SEC'),
            'u01': utilTrefila.get('m01', {}).get('UTIL'),
            'u02': utilTrefila.get('m02', {}).get('UTIL'),
            'u03': utilTrefila.get('m03', {}).get('UTIL'),
            'u04': utilTrefila.get('m04', {}).get('UTIL'),
            'u05': utilTrefila.get('m05', {}).get('UTIL'),
            't01': utilTrefila.get('m01', {}).get('TEMPO_PARADO'),
            't02': utilTrefila.get('m02', {}).get('TEMPO_PARADO'),
            't03': utilTrefila.get('m03', {}).get('TEMPO_PARADO'),
            't04': utilTrefila.get('m04', {}).get('TEMPO_PARADO'),
            't05': utilTrefila.get('m05', {}).get('TEMPO_PARADO')
        })
        # return json
        return res(
            json.dumps(data),
            mimetype='application/json',
            status=200
        )

    #################################################################################################################################################

    @app.route('/avb/trefila/metas/')
    def trefilaMetas(req: Request, res: Response):
        # Read Metas
        report = homerico.RelatorioGerencialTrimestre(
            idReport=16,
            registros={
                'PRODUÇÃO': 2962,
                'PRODUÇÃO HORÁRIA': 2966,
                'RENDIMENTO METÁLICO': 2963,
                'PRODUÇÃO POR MÁQUINA': 2988
            }
        )
        # Append Metas
        try: report.update(mysql.trefila.custo())
        except: pass
        try: report.update(mysql.trefila.sucata())
        except: pass
        try: report.update(mysql.trefila.vs())
        except: pass
        try: # Utilizacao
            metaUtil = mysql.trefila.utilizacao()
            # util trf dia
            utilTrefila = util.read.trefila()
            total = (
                utilTrefila.get('m01', {}).get('UTIL') +
                utilTrefila.get('m02', {}).get('UTIL') +
                utilTrefila.get('m03', {}).get('UTIL') +
                utilTrefila.get('m04', {}).get('UTIL') +
                utilTrefila.get('m05', {}).get('UTIL')
            )
            # update util
            metaUtil['utilizacao'].update({
                'dia': (total / 4) * 100
            })
            # update metas
            report.update(metaUtil)
        except: pass

        # Return Data
        return res(
            json.dumps(report),
            mimetype='application/json',
            status=200
        )

#################################################################################################################################################
