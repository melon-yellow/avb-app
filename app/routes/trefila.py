
#################################################################################################################################################

# Imports
import io
import os
import json
import flask
import pandas
import py_misc
import datetime

# Modules
from ..helpers import homerico
from ..services import mysql

#################################################################################################################################################

Request = flask.Request
Response = flask.Response

#################################################################################################################################################

# Get File-Paths
fileDir = os.path.dirname(os.path.abspath(__file__))
utilPath = os.path.abspath(os.path.join(fileDir, '../util.json'))

#################################################################################################################################################

def readUtil():
    # Open File
    default = [None, None, None, None, None, None]
    gets: dict = json.load(open(utilPath, 'r'))
    time = gets.get('trf', default)[0]
    # Parse Util
    def parseUtil(mq):
        r = dict()
        util = gets.get('trf', default)[mq]
        c = time != None and util != None
        r['UTIL'] = util / (time if time > 0 else 1) if c else None
        r['TEMPO_PARADO'] = ((time - util) / 60) if c else None
        return r
    # Return Util Dictionary
    return {
        'SEC': time,
        'm01': parseUtil(1),
        'm02': parseUtil(2),
        'm03': parseUtil(3),
        'm04': parseUtil(4),
        'm05': parseUtil(5),
    }

#################################################################################################################################################

# Load Routes
def __load__(app: py_misc.Express):

    #################################################################################################################################################

    @app.route('/avb/trefila/produtividade/')
    def trefilaProdutividade(req: Request, res: Response):
        # get date
        date = datetime.datetime.today().strftime('%d/%m/%Y')
        # read meta
        csv_str = homerico.network.RelatorioLista(
            dataInicial=date,
            dataFinal=date,
            idProcesso='50'
        )
        csv_file = io.StringIO(csv_str)
        df = pandas.read_csv(csv_file, sep=';')
        prod = {}
        try:
            df = df.filter(['Produto','Maquina','Peso do Produto'])
            df = df.stack().str.replace(',','.').unstack()
            df['Peso do Produto'] = df['Peso do Produto'].astype(float)
            df = df.groupby('Maquina').sum()
            df = df['Peso do Produto']
            prod.update(json.loads(df.to_json()))
        except: pass
        # get prod data
        data = {
            'p01': prod.get('Trefila 01'),
            'p02': prod.get('Trefila 02'),
            'p03': prod.get('Trefila 03'),
            'p04': prod.get('Trefila 04'),
            'p05': prod.get('Trefila 05')
        }
        # get util data
        util = readUtil()
        data.update({
            's': util.get('SEC'),
            'u01': util.get('m01', {}).get('UTIL'),
            'u02': util.get('m02', {}).get('UTIL'),
            'u03': util.get('m03', {}).get('UTIL'),
            'u04': util.get('m04', {}).get('UTIL'),
            'u05': util.get('m05', {}).get('UTIL'),
            't01': util.get('m01', {}).get('TEMPO_PARADO'),
            't02': util.get('m02', {}).get('TEMPO_PARADO'),
            't03': util.get('m03', {}).get('TEMPO_PARADO'),
            't04': util.get('m04', {}).get('TEMPO_PARADO'),
            't05': util.get('m05', {}).get('TEMPO_PARADO')
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
        # read metas
        report = homerico.RelatorioGerencialTrimestre(
            idReport=16,
            registros={
                'PRODUÇÃO': 2962,
                'PRODUÇÃO HORÁRIA': 2966,
                'RENDIMENTO METÁLICO': 2963,
                'PRODUÇÃO POR MÁQUINA': 2988
            }
        )
        # custo trf
        try: report.update(mysql.trefila.custo())
        except: pass
        # sucateamento trf
        try: report.update(mysql.trefila.sucata())
        except: pass
        # 5S
        try: report.update(mysql.trefila.fives())
        except: pass
        try: 
            # util trf
            util = mysql.trefila.utilizacao()
            # util trf dia
            ru = readUtil()
            total = (
                ru.get('m01', {}).get('UTIL') +
                ru.get('m02', {}).get('UTIL') +
                ru.get('m03', {}).get('UTIL') +
                ru.get('m04', {}).get('UTIL') +
                ru.get('m05', {}).get('UTIL')
            )
            # update util
            util['utilizacao'].update({
                'dia': (total / 4) * 100
            })
            # update metas
            report.update(util)
        except: pass
        # return data
        return res(
            json.dumps(report),
            mimetype='application/json',
            status=200
        )

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
            mimetype = "text/csv",
            headers = {
                "Content-disposition": "attachment; filename=utilizacao.csv"
            },
            status=200
        )

#################################################################################################################################################
