
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

Request = flask.request
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
    def parse_util(mq):
        r = dict()
        util = gets.get('trf', default)[mq]
        c = time != None and util != None
        r['UTIL'] = util / (time if time > 0 else 1) if c else None
        r['TEMPO_PARADO'] = ((time - util) / 60) if c else None
        return r
    # Return Util Dictionary
    data = dict(
        m01 = parse_util(1),
        m02 = parse_util(2),
        m03 = parse_util(3),
        m04 = parse_util(4),
        m05 = parse_util(5),
        SEC = time
    )

#################################################################################################################################################

# Load Routes
def __load__(app: py_misc.Express):

    #################################################################################################################################################

    @app.route('/api/trf/')
    def api_trf(req: Request, res: Response):
        date = datetime.datetime.today().strftime('%d/%m/%Y')
        csv_str = homerico.net.RelatorioLista(
            dataInicial=date,
            dataFinal=date,
            idProcesso='50'
        )
        csv_file = io.StringIO(csv_str)
        df = pandas.read_csv(csv_file, sep=';')
        try:
            df = df.filter(['Produto','Maquina','Peso do Produto'])
            df = df.stack().str.replace(',','.').unstack()
            df['Peso do Produto'] = df['Peso do Produto'].astype(float)
            df = df.groupby('Maquina').sum()
            df = df['Peso do Produto']
            df = json.loads(df.to_json())
        except: df = dict()
        dt = dict()
        # get prod data
        dt['p01'] = df.get('Trefila 01')
        dt['p02'] = df.get('Trefila 02')
        dt['p03'] = df.get('Trefila 03')
        dt['p04'] = df.get('Trefila 04')
        dt['p05'] = df.get('Trefila 05')
        # get util data
        ut = readUtil()
        dt['u01'] = ut['m01']['UTIL']
        dt['u02'] = ut['m02']['UTIL']
        dt['u03'] = ut['m03']['UTIL']
        dt['u04'] = ut['m04']['UTIL']
        dt['u05'] = ut['m05']['UTIL']
        dt['t01'] = ut['m01']['TEMPO_PARADO']
        dt['t02'] = ut['m02']['TEMPO_PARADO']
        dt['t03'] = ut['m03']['TEMPO_PARADO']
        dt['t04'] = ut['m04']['TEMPO_PARADO']
        dt['t05'] = ut['m05']['TEMPO_PARADO']
        dt['s'] = ut['SEC']
        # return json
        return res(
            json.dumps(dt),
            mimetype='application/json',
            status=200
        )

    #################################################################################################################################################

    @app.route('/api/metas_lam_frio/')
    def metas_lam_frio(req: Request, res: Response):
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
    def prod_lam_frio(req: Request, res: Response):
        data = homerico.get.ProducaoLista(lista=2361)
        return res(
            json.dumps(data),
            mimetype='application/json',
            status=200
        )

    #################################################################################################################################################

    @app.route('/api/util_csv/')
    def trf_util_csv(req: Request, res: Response):
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
    def trf_util_csv_dia(req: Request, res: Response):
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
