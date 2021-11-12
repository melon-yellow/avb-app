
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
from ..services import oracle
from ..services import mssql

#################################################################################################################################################

Request = flask.Request
Response = flask.Response

#################################################################################################################################################

# Get File-Paths
fileDir = os.path.dirname(os.path.abspath(__file__))
utilPath = os.path.abspath(os.path.join(fileDir, '../util.json'))

#################################################################################################################################################

def readUtil():
    r = dict()
    default = [None, None]
    gets = json.load(open(utilPath, 'r'))
    time = gets.get('mill', default)[0]
    util = gets.get('mill', default)[1]
    c = time != None and util != None
    r['UTIL'] = util / (time if time > 0 else 1) if c else None
    r['TEMPO_PARADO'] = ((time - util) / 60) if c else None
    return r

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

    @app.route('/avb/laminador/nivel2/')
    def laminadorNivel2(req: Request, res: Response):
        data = mssql.mill.rfaLim()
        return res(
            json.dumps(data),
            mimetype='application/json',
            status=200
        )

    #################################################################################################################################################

    @app.route('/avb/laminador/rfa/')
    def laminadorRFA(req: Request, res: Response):
        data = mssql.mill.rfa()
        return res(
            json.dumps(data),
            mimetype='application/json',
            status=200
        )

    #################################################################################################################################################

    @app.route('/avb/laminador/forno/')
    def laminadorForno(req: Request, res: Response):
        data = oracle.furnace.gusaapp()
        util = readUtil()
        data.update({
            'UTIL': util.get('UTIL'),
            'TEMPO_PARADO': util.get('TEMPO_PARADO'),
            'timestamp': datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')
        })
        return res(
            json.dumps(data),
            mimetype='application/json',
            status=200
        )

    #################################################################################################################################################

    @app.route('/avb/laminador/escalaTurno/')
    def laminadorEscalaTurno(req: Request, res: Response):
        data = turno.escala.get()
        return res(
            json.dumps(data),
            mimetype='application/json',
            status=200
        )

    #################################################################################################################################################

    @app.route('/avb/laminador/reports/util/')
    def laminadorReportsUtil(req: Request, res: Response):
        # save json file
        json.dump(req.json, open(utilPath, 'w'))
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
