
#################################################################################################################################################

# Imports
import py_misc
import mysql.connector
import pandas
import io

# modules
from .. import turno
from .. import homerico
from .. import metas

#################################################################################################################################################

Request = py_misc.flask.request
Response = py_misc.flask.Response

#################################################################################################################################################

# Gets Actual File Directory
filedir = py_misc.__schema__()

#################################################################################################################################################

def readUtil():
    # Open File
    default = [None, None, None, None, None, None]
    gets = py_misc.json.load(open('util.json', 'r'))
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
def __load__(api: py_misc.API):

    #################################################################################################################################################

    @api.route('/api/trf/')
    def api_trf(req: Request, res: Response):
        date = py_misc.datetime.datetime.today().strftime('%d/%m/%Y')
        csv_str = homerico.__dll__.RelatorioLista(date, date, 50)
        csv_file = io.StringIO(csv_str)
        df = pandas.read_csv(csv_file, sep=';')
        try:
            df = df.filter(['Produto','Maquina','Peso do Produto'])
            df = df.stack().str.replace(',','.').unstack()
            df['Peso do Produto'] = df['Peso do Produto'].astype(float)
            df = df.groupby('Maquina').sum()
            df = df['Peso do Produto']
            df = py_misc.json.loads(df.to_json())
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
            py_misc.json.dumps(dt),
            mimetype='application/json',
            status=200
        )

    #################################################################################################################################################

    @api.route('/api/metas_lam_frio/')
    def metas_lam_frio(req: Request, res: Response):
        registros = {
            'PRODUÇÃO':2962,
            'PRODUÇÃO HORÁRIA':2966,
            'RENDIMENTO METÁLICO':2963,
            'PRODUÇÃO POR MÁQUINA':2988
        }
        # get metas
        registros = homerico.get.RelatorioGerencialTrim(16, registros)
        # custo trf
        try: registros.update(metas.trefila.Custo())
        except Exception as e: print(e)
        # sucateamento trf
        try: registros.update(metas.trefila.Sucata())
        except: pass
        # 5S
        try: registros.update(metas.trefila.S5())
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
            registros.update(util)
        except: pass
        # return data
        return res(
            py_misc.json.dumps(registros),
            mimetype='application/json',
            status=200
        )

    #################################################################################################################################################

    @api.route('/api/prod_lam_frio/')
    def prod_lam_frio(req: Request, res: Response):
        data = homerico.get.ProducaoLista(2361)
        return res(
            py_misc.json.dumps(data),
            mimetype='application/json',
            status=200
        )

    #################################################################################################################################################

    @api.route('/api/util_csv/')
    def trf_util_csv(req: Request, res: Response):
        df = None
        try:
            mydb = mysql.connector.connect(
                host='127.0.0.1',
                user='Jayron',
                passwd='123456',
                port='3306',
                database='iba_i'
            )
            try:
                sql = open('../sql/trefila.util.sql').read()
                df = pandas.read_sql(sql, mydb)
            except: pass
            mydb.close()
        except: pass
        if df == None: return
        # Processing
        meses = {'1':[1,2,3],'2':[4,5,6],'3':[7,8,9],'4':[10,11,12]}
        df['_0h'] = df._date.apply(lambda row : turno.escala.get(dia = row)[0][0])
        df['_8h'] = df._date.apply(lambda row : turno.escala.get(dia = row)[1][0])
        df['_16h'] = df._date.apply(lambda row : turno.escala.get(dia = row)[2][0])
        df['_date'] = df['_date'].astype('str')
        dz = df
        hoje = py_misc.datetime.date.today()
        #hoje = datetime.datetime.now()
        #hoje = datetime.date(2021,2,23)
        Trimestre = str((hoje.month-1)//3+1)
        Tmeses = meses.get(Trimestre)
        #mes = datetime.date(2021,3,23).month
        bn = df[df['_date'] >= py_misc.datetime.date(hoje.year, Tmeses[0], 1).strftime("%Y-%m-%d")]
        bn = bn[bn['_date'] <= hoje.strftime("%Y-%m-%d")]
        bn = bn.filter(['_date','M1','M2','M3','M4','M5','_0h','_8h','_16h'])
        bn = bn.drop(['M1'], axis=1)
        bn['Global'] = (bn['M2']+bn['M3']+bn['M4']+bn['M5']) / 4
        # Retrun Data
        return res(
            bn.to_csv(),
            mimetype = "text/csv",
            headers = {
                "Content-disposition": "attachment; filename=utilizacao.csv"
            }
        )

    #################################################################################################################################################

    @api.route('/api/util_csv_dia')
    def trf_util_csv_dia(req: Request, res: Response):
        csv = None
        try:
            mydb = mysql.connector.connect(
                host='127.0.0.1',
                user='Jayron',
                passwd='123456',
                port='3306',
                database='iba_i'
            )
            try:
                sql = open('sql/trf_util_day.sql').read()
                csv = pandas.read_sql(sql, mydb).to_csv()
            except: pass
            mydb.close()
        except: pass
        if csv == None: return
        # Return Data
        return res(
            csv,
            mimetype = "text/csv",
            headers = {
                "Content-disposition": "attachment; filename=utilizacao-dia.csv"
            }
        )


#################################################################################################################################################
