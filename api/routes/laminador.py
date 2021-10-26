
#################################################################################################################################################

# Imports
import json
import flask
import py_misc
import datetime

# modules
from .. import iba
from .. import furl2
from .. import homerico

#################################################################################################################################################

Request = flask.request
Response = flask.Response

#################################################################################################################################################

def readUtil():
    r = dict()
    default = [None, None]
    gets = json.load(open('./api/util.json', 'r'))
    time = gets.get('mill', default)[0]
    util = gets.get('mill', default)[1]
    c = time != None and util != None
    r['UTIL'] = util / (time if time > 0 else 1) if c else None
    r['TEMPO_PARADO'] = ((time - util) / 60) if c else None
    return r

#################################################################################################################################################

# Load Routes
def __load__(api: py_misc.API):

    #################################################################################################################################################

    @api.route('/api/metas_lam_quente/')
    def metas_lam_quente(req: Request, res: Response):
        registros = {
            'ACIDENTE CPT':1333,
            'PROD LAMINADO':1336,
            'REND. METALICO':1338,
            'BLBP':1444,
            'SUCATEAMENTO':1350
            }
        data = homerico.get.RelatorioGerencialTrim(10, registros)
        return res(
            json.dumps(data),
            mimetype='application/json',
            status=200
        )

    #################################################################################################################################################

    @api.route('/api/prod_lam_quente/')
    def prod_lam_quente(req: Request, res: Response):
        data = homerico.get.ProducaoLista(1269)
        return res(
            json.dumps(data),
            mimetype='application/json',
            status=200
        )

    #################################################################################################################################################

    @api.route('/api/l2/')
    def mill_rfa(req: Request, res: Response):
        data = iba.mssql.rfaLim()
        return res(
            json.dumps(data),
            mimetype='application/json',
            status=200
        )

    #################################################################################################################################################

    @api.route('/api/mill/')
    def api_mill(req: Request, res: Response):
        data = iba.mssql.rfa()
        return res(
            json.dumps(data),
            mimetype='application/json',
            status=200
        )

    #################################################################################################################################################

    @api.route('/api/furnace/')
    def fur_gusaapp(req: Request, res: Response):
        data = furl2.oracle.gusaapp()
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

    @api.route('/set_util/')
    def set_util(req: Request, res: Response):
        json.dump(req.json, open('./api/util.json', 'w'))
        return res(
            json.dumps({ 'done': True }),
            mimetype='application/json',
            status=200
        )

    set_util.user('iba.avb').password('sqwenjwe34#')

#################################################################################################################################################
