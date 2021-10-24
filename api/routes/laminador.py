
#################################################################################################################################################

# Imports
import py_misc

# modules
from .. import iba
from .. import furl2
from .. import homerico

#################################################################################################################################################

# Gets Actual File Directory
filedir = py_misc.__schema__()

#################################################################################################################################################

def readUtil():
    r = dict()
    default = [None, None]
    gets = py_misc.json.load(open(filedir + '\\util.json', 'r'))
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
    def metas_lam_quente(req, res):
        registros = {
            'ACIDENTE CPT':1333,
            'PROD LAMINADO':1336,
            'REND. METALICO':1338,
            'BLBP':1444,
            'SUCATEAMENTO':1350
            }
        registros = homerico.get.RelatorioGerencialTrim(10, registros)
        return registros

    #################################################################################################################################################

    @api.route('/api/prod_lam_quente/')
    def prod_lam_quente(req, res):
        dados = homerico.get.ProducaoLista(1269)
        return dados

    #################################################################################################################################################

    @api.route('/api/l2/')
    def mill_rfa(req, res):
        return iba.mssql.rfaLim()

    #################################################################################################################################################

    @api.route('/api/mill/')
    def api_mill(req, res):
        return iba.mssql.rfa()

    #################################################################################################################################################

    @api.route('/api/furnace/')
    def fur_gusaapp(req, res):
        r = furl2.oracle.gusaapp()
        x = readUtil()
        r.update({
            'UTIL': x.get('UTIL'),
            'TEMPO_PARADO': x.get('TEMPO_PARADO'),
            'timestamp': py_misc.datetime.datetime().strftime('%d/%m/%y %H:%M:%S')
        })
        return r

    #################################################################################################################################################

    @api.route('/set_util/')
    def set_util(req):
        py_misc.json.dump(req, open(filedir + '\\util.json', 'w'))
        return dict(done=True)

    set_util.user('iba').password('sqwenjwe34#')
    
#################################################################################################################################################
