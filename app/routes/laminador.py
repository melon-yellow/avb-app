
#################################################################################################################################################

# Imports
import os
import json
import flask
import py_misc
import datetime

# modules
from ..helpers import homerico
from ..helpers import turno
from ..helpers import util
from ..services import oracle
from ..services import odbc

#################################################################################################################################################

Request = flask.Request
Response = flask.Response

#################################################################################################################################################

# Load Routes
def __load__(app: py_misc.Express):

    #################################################################################################################################################

    @app.route('/avb/laminador/metas/')
    def laminadorMetas(req: Request, res: Response):
        # read metas
        data = homerico.RelatorioGerencialTrimestre(
            idReport=10,
            registros={
                'ACIDENTE CPT': 1333,
                'PROD LAMINADO': 1336,
                'REND. METALICO': 1338,
                'BLBP': 1444,
                'SUCATEAMENTO': 1350
            }
        )
        return res(
            json.dumps(data),
            mimetype='application/json',
            status=200
        )

    #################################################################################################################################################

    @app.route('/avb/laminador/producao/')
    def laminadorProducao(req: Request, res: Response):
        data = homerico.ProducaoLista(lista=1269)
        return res(
            json.dumps(data),
            mimetype='application/json',
            status=200
        )

    #################################################################################################################################################

    @app.route('/avb/laminador/produto/')
    def laminadorProduto(req: Request, res: Response):
        data = odbc.laminador.produto()
        return res(
            json.dumps(data),
            mimetype='application/json',
            status=200
        )

    #################################################################################################################################################

    @app.route('/avb/laminador/blbp/')
    def laminadorBLBP(req: Request, res: Response):
        data = odbc.laminador.blbp()
        return res(
            json.dumps(data),
            mimetype='application/json',
            status=200
        )

    #################################################################################################################################################

    @app.route('/avb/laminador/rfa/')
    def laminadorRFA(req: Request, res: Response):
        data = odbc.laminador.rfa()
        return res(
            json.dumps(data),
            mimetype='application/json',
            status=200
        )

    #################################################################################################################################################

    @app.route('/avb/laminador/rfal2/')
    def laminadorRFAL2(req: Request, res: Response):
        data = odbc.laminador.rfal2()
        return res(
            json.dumps(data),
            mimetype='application/json',
            status=200
        )

    #################################################################################################################################################

    @app.route('/avb/laminador/forno/')
    def laminadorForno(req: Request, res: Response):
        now = datetime.datetime.now()
        data = oracle.furnace.gusaapp()
        utilLaminador = util.read.laminador()
        data.update({
            'UTIL': utilLaminador.get('UTIL'),
            'TEMPO_PARADO': utilLaminador.get('TEMPO_PARADO'),
            'timestamp': now.strftime('%d/%m/%y %H:%M:%S')
        })
        return res(
            json.dumps(data),
            mimetype='application/json',
            status=200
        )

    #################################################################################################################################################

    @app.route('/avb/laminador/escalaTurno/')
    def laminadorEscalaTurno(req: Request, res: Response):
        data = turno.escala()
        return res(
            json.dumps(data),
            mimetype='application/json',
            status=200
        )

    #################################################################################################################################################

    @app.route('/avb/laminador/reports/util/')
    def laminadorReportsUtil(req: Request, res: Response):
        # save json file
        util.write(req.json)
        return res(
            json.dumps({ 'done': True }),
            mimetype='application/json',
            status=200
        )

    # Set Authentication
    laminadorReportsUtil.users.update({
        os.getenv('AVB_IBA_UTIL_REPORT_USER'):
        os.getenv('AVB_IBA_UTIL_REPORT_PASSWORD')
    })

#################################################################################################################################################
