
#################################################################################################################################################

# Imports
import io
import os
import json
import flask
import pandas
import py_misc
import datetime

# modules
from .. import turno
from .. import homerico
from .. import metas
from .. import iba

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

    @app.route('/api/trf/')
    def apiTrf(req: Request, res: Response):
        date = datetime.datetime.today().strftime('%d/%m/%Y')
        csv_str = homerico.net.RelatorioLista(
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
        data = dict()
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

    @app.route('/api/metas_lam_frio/')
    def metasLamFrio(req: Request, res: Response):
        registros = {
            'PRODUÇÃO':2962,
            'PRODUÇÃO HORÁRIA':2966,
            'RENDIMENTO METÁLICO':2963,
            'PRODUÇÃO POR MÁQUINA':2988
        }
        # get metas
        report = homerico.get.RelatorioGerencialTrimestre(
            idReport=16,
            registros=registros
        )
        # custo trf
        try: report.update(metas.trefila.Custo())
        except: pass
        # sucateamento trf
        try: report.update(metas.trefila.Sucata())
        except: pass
        # 5S
        try: report.update(metas.trefila.S5())
        except: pass
        try: # util trf dia
            ut = readUtil()
            ut = [
                ut['m01']['UTIL'],
                ut['m02']['UTIL'],
                ut['m03']['UTIL'],
                ut['m04']['UTIL'],
                ut['m05']['UTIL']
            ]
            # util trf
            util = metas.trefila.Utilizacao()
            gen_util = dict(dia=((sum(ut) * 100) / 4))
            util['utilizacao'].update(gen_util)
            report.update(util)
        except: pass
        # return data
        return res(
            json.dumps(report),
            mimetype='application/json',
            status=200
        )

    #################################################################################################################################################

    @app.route('/api/prod_lam_frio/')
    def prodLamFrio(req: Request, res: Response):
        data = homerico.get.ProducaoLista(lista=2361)
        return res(
            json.dumps(data),
            mimetype='application/json',
            status=200
        )

    #################################################################################################################################################

    @app.route('/api/util_csv/')
    def trfUtilCsv(req: Request, res: Response):
        # MySQL Connection
        csv = iba.mysql.UtilizacaoTrefila()
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

    @app.route('/api/util_csv_dia')
    def trfUtilCsvDia(req: Request, res: Response):
        # MySQL Connection
        csv = iba.mysql.UtilizacaoDiaTrefila()
        # Return Data
        return res(
            csv,
            mimetype = "text/csv",
            headers = {
                "Content-disposition": "attachment; filename=utilizacao-dia.csv"
            },
            status=200
        )

#################################################################################################################################################
