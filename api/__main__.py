
#################################################################################################################################################

# -*- coding: utf-8 -*-
import os
import json
import pyodbc
import datetime
import requests
import pandas as pd
import mysql.connector
from io import StringIO

#################################################################################################################################################

# Import Miscellaneous
import py_misc

# Import Homerico
import homerico

# SQL Connections
import connectors as conn

# Escalas Turno
from turno.escala import getEscala

#################################################################################################################################################

# Gets Actual File Directory
file_dir = os.path.dirname(__file__)

#################################################################################################################################################

# Setup Connection
homerico.Validar('homerico.avb')
homerico.Login('CH1200', 'bhn860')

#################################################################################################################################################

# Declare Api
api = py_misc.API().host('0.0.0.0').port(3000)

#################################################################################################################################################

# Main Script Locals
class Main:
    api = api
    homerico = homerico
    sqldir = file_dir + '\\sql'

# Instance Object
__main__ = Main()

#################################################################################################################################################

# Import Routes
for entry in py_misc.os.scandir('routes'):
    if not entry.is_file(): continue
    fname = entry.name
    if '.py' != fname[-3:]: continue
    if '__init__' in fname: continue
    name = fname[:-3]
    if len(name) == 0: continue
    try:
        exec (f'import routes.{name} as m')
        if '__add__' not in m.__all__: continue
        if not callable(m.__add__): continue
        m.__add__(__main__)
    except: pass

#################################################################################################################################################

def query(conn, string):
    try:
        cursor = conn.cursor()
        cursor.execute(string)
        res = [dict((cursor.description[i][0], value) \
                   for i, value in enumerate(row)) for row in cursor.fetchall()]
        return res
    except: return []

def util_query(conn, query, tag):
    if (not isinstance(tag, str) or
        not isinstance(query, str)): return []
    res = query(conn, query.format(tag))
    return res[0]

def _old_util_trf_():
    conn = pyodbc.connect('DSN=iba;UID=sa;PWD=avb2020')
    query = open('sql/new_util.sql').read()
    r = dict(
        m02 = util_query(conn, query, 'TREFILA - 02 - OCUPADA'),
        m03 = util_query(conn, query, 'TREFILA - 03 - OCUPADA'),
        m04 = util_query(conn, query, 'TREFILA - 04 - OCUPADA'),
        m05 = util_query(conn, query, 'TREFILA - 05 - OCUPADA')
    )
    cur = conn.cursor()
    cur.connection.close()
    return r

def _old_util_():
    conn = pyodbc.connect('DSN=iba;UID=sa;PWD=avb2020')
    cur = conn.cursor()
    cur.execute(query_ultil)
    r = [dict((cur.description[i][0], value) \
               for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.connection.close()
    uti = (r[0].get('OCC_SEC')/r[0].get('ATUAL_SEC'))
    r[0]['UTIL'] = uti
    r[0]['TEMPO_PARADO'] = (r[0].get('ATUAL_SEC') - r[0].get('OCC_SEC'))/60.0
    return (r[0])

#################################################################################################################################################

# Get Data From PDA Server
def get_pda(tagname):
    # Check for input Variable
    if (not isinstance(tagname, str) and
        not isinstance(tagname, list)
        ): return dict(error='tagname missing')

    try: # Request PDA Server
        res = requests.post(
            'http://localhost:3001/api/pda/',
            json=dict(tagname=tagname),
            auth=('client', '123456')
        )
        res = json.loads(res.text)
    except: # If Server Not Responding
        res = dict(value=None, name=None, status='server down')

    # Return data
    return res

#################################################################################################################################################

def util():
    r = dict()
    default = [None, None]
    gets = json.load(open(file_dir + '\\util.json', 'r'))
    time = gets.get('mill', default)[0]
    util = gets.get('mill', default)[1]
    c = time != None and util != None
    r['UTIL'] = util / (time if time > 0 else 1) if c else None
    r['TEMPO_PARADO'] = ((time - util) / 60) if c else None
    return r

#################################################################################################################################################

def util_trf():
    # Open File
    default = [None, None, None, None, None, None]
    gets = json.load(open(file_dir + '\\util.json', 'r'))
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
    return dict(
        m01 = parse_util(1),
        m02 = parse_util(2),
        m03 = parse_util(3),
        m04 = parse_util(4),
        m05 = parse_util(5),
        SEC = time
    )

#################################################################################################################################################
#                                                                    API ENDNODES                                                               #
#################################################################################################################################################

@api.route('/api/turma/')
def boletim_test(req, res):
    hoje = datetime.date.today()
    ontem = hoje - datetime.timedelta(days=1)
    hoje = hoje.strftime('%d/%m/%Y')
    ontem = ontem.strftime('%d/%m/%Y')
    e = [homerico.RelatorioBoletim(ontem, hoje, '31'),
        homerico.RelatorioBoletim(ontem, hoje, '35')]
    return e

#################################################################################################################################################

@api.route('/api/trf/')
def db_tref(req, res):
    date = datetime.datetime.today().strftime('%d/%m/%Y')
    csv_str = homerico.src.RelatorioLista(date, date, 50)
    csv_file = StringIO(csv_str)
    df = pd.read_csv(csv_file, sep=';')
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
    ut = util_trf()
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
    return dt

#################################################################################################################################################

@api.route('/api/metas_lam_quente/')
def _metas_lam_quente(req, res):
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
def _prod_lam_quente(req, res):
    dados = homerico.get.ProducaoLista(1269)
    return dados

#################################################################################################################################################

@api.route('/api/metas_lam_frio/')
def _metas_lam_frio(req, res):
    registros = {
        'PRODUÇÃO':2962,
        'PRODUÇÃO HORÁRIA':2966,
        'RENDIMENTO METÁLICO':2963,
        'PRODUÇÃO POR MÁQUINA':2988
    }
    # get metas
    registros = homerico.get.RelatorioGerencialTrim(16, registros)

    # custo trf
    try: registros.update(get_meta_custo_trf())
    except Exception as e: print(e)
    # sucateamento trf
    try: registros.update(get_meta_suca_trf())
    except: pass
    # 5S
    try: registros.update(get_meta_5S_trf())
    except: pass

    try: # util trf dia
        ut = util_trf()
        ut = [
            ut['m01']['UTIL'],
            ut['m02']['UTIL'],
            ut['m03']['UTIL'],
            ut['m04']['UTIL'],
            ut['m05']['UTIL']
        ]
        # util trf
        util = get_meta_util_trf()
        gen_util = dict(dia=((sum(ut) * 100) / 4))
        util['utilizacao'].update(gen_util)
        registros.update(util)
    except: pass
    # return data
    return registros

#################################################################################################################################################

@api.route('/api/prod_lam_frio/')
def _prod_lam_frio(req, res):
    dados = homerico.get.ProducaoLista(2361)
    return dados

#################################################################################################################################################

@api.route('/api/l2/')
def api_l2(req):
    produto = conn.odbc.iba_mssql.__callable__(None).get('CTR_PRODUCT_NAME')
    query_mssql2 = open('sql/query_mssql2.sql').read().format(produto)
    conn = pyodbc.connect('DSN=L2_SERVER;UID=sa;PWD=avb2020')
    cur = conn.cursor()
    cur.execute(query_mssql2)
    r = [dict((cur.description[i][0], value)
        for i, value in enumerate(row)) for row in cur.fetchall()]
    r = r[0] if len(r) > 0 else dict()
    cur.connection.close()
    return r

#################################################################################################################################################

@api.route('/api/mill/')
def api_mill(req, res):
    return db_mssql()

#################################################################################################################################################

@api.route('/api/furnace/')
def api_furnace(req, res):
    r = db_orcl()
    x = util()
    r['UTIL'] = x.get('UTIL')
    r['TEMPO_PARADO'] = x.get('TEMPO_PARADO')
    r['timestamp'] = py_misc.datetime.datetime.today().strftime('%d/%m/%y %H:%M:%S')
    return r

#################################################################################################################################################

@api.route('/api/aci_rendimento/')
def aci_rendimento(req, res):
    # get api data
    rend = homerico.get.RelatorioGerencialRegistro(15)
    carg_s = homerico.get.RelatorioGerencialRegistro(1218)

    rendimento = None
    carga_solida = None

    try:
        if (not isinstance(rend, list)
            or not len(rend) >= 2
            or not isinstance(rend[1], list)
            or not len(rend[1]) >= 3
            or not isinstance(rend[1][2], str)
            ): raise Exception('?')
        rendimento = float(rend[1][2].replace(',', '.'))
    except: pass

    try:
        if (not isinstance(carg_s, list)
            or not len(carg_s) >= 2
            or not isinstance(carg_s[1], list)
            or not len(carg_s[1]) >= 3
            or not isinstance(carg_s[1][2], str)
            ): raise Exception('?')
        carga_solida = float(carg_s[1][2].replace(',', '.'))
    except: pass

    # Return data
    return dict(
        rendimento = rendimento,
        carga_solida = carga_solida
    )

#################################################################################################################################################

@api.route('/questions/', methods=['POST'])
def questions(req):
    print('data from client: {}'.format(req))
    dictToReturn = analisa(req)
    print('data to client: {}'.format(dictToReturn['answer']))
    return dictToReturn

#################################################################################################################################################

@api.route('/set_util/')
def set_util(req):
    json.dump(req, open(file_dir + '\\util.json', 'w'))
    return dict(done=True)

set_util.user('iba').password('sqwenjwe34#')

#################################################################################################################################################

@api.route('/api/util_csv/')
def trf_util_csv():
    try:
        mydb12 = mysql.connector.connect(host='192.168.61.1', user='Jayron', passwd='123456', port='3306', database='iba_i')
        query = open('sql/trf_util_shift.sql').read()

        try:
            df = pd.read_sql(query, mydb12)
            mydb12.close()

        except Exception as e:
            mydb12.close()

    except Exception as e: pass

    meses = {'1':[1,2,3],'2':[4,5,6],'3':[7,8,9],'4':[10,11,12]}
    df['_0h'] = df._date.apply(lambda row : getEscala(dia = row)[0][0])
    df['_8h'] = df._date.apply(lambda row : getEscala(dia = row)[1][0])
    df['_16h'] = df._date.apply(lambda row : getEscala(dia = row)[2][0])
    df['_date'] = df['_date'].astype('str')
    dz = df
    hoje = datetime.date.today()
    #hoje = datetime.datetime.now()
    #hoje = datetime.date(2021,2,23)
    Trimestre = str((hoje.month-1)//3+1)
    Tmeses = meses.get(Trimestre)
    mon = list()
    mes = hoje.month
    #mes = datetime.date(2021,3,23).month

    bn = df[df['_date']>=datetime.date(hoje.year,Tmeses[0],1).strftime("%Y-%m-%d")]
    bn = bn[bn['_date']<=datetime.date(hoje.year,hoje.month,hoje.day).strftime("%Y-%m-%d")]
    bn = bn.filter(['_date', 'M1','M2','M3', 'M4', 'M5', '_0h', '_8h','_16h'])
    bn = bn.drop(['M1'], axis=1)
    bn['Global'] = (bn['M2']+bn['M3']+bn['M4']+bn['M5']) / 4

    return bn.to_csv()

#################################################################################################################################################

@api.route('/api/util_csv_dia')
def trf_util_csv_dia(req):
    textcsv = ''
    try:
        mydb = mysql.connector.connect(host='192.168.61.1', user='Jayron', passwd='123456', port='3306', database='iba_i')
        try:
            query = open('sql/trf_util_day.sql').read()
            df = pd.read_sql(query, mydb)
            textcsv = df.to_csv()
        except: pass
        mydb.close()
    except: pass

    return textcsv

#################################################################################################################################################

# start server
api.start()

# keep main thread alive
py_misc.keepalive()

#################################################################################################################################################
