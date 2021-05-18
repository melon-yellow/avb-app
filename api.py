# -*- coding: utf-8 -*-
import re
import sys
import json
import time
import copy
import train
import pyodbc
import ctypes
import datetime
import cx_Oracle
import numpy as np
import pandas as pd
import mysql.connector
from io import StringIO
import classification as clas
from EscalaTurno import getEscala

#################################################################################################################################################

# Import Miscellaneous
sys.path.append('E:/python/misc')
from miscellaneous import Miscellaneous

# Instance Misc
misc = Miscellaneous()

#################################################################################################################################################

# Import Homerico
sys.path.append('E:/python/homerico')
import homerico

# Setup Connection
homerico.Validar('homerico.avb')
homerico.Login('CH1200', 'bhn860')

#################################################################################################################################################

# Declare Api
api = misc.api().host('127.0.0.1').port(3000)

#################################################################################################################################################

meses = {'1':[1,2,3],'2':[4,5,6],'3':[7,8,9],'4':[10,11,12]}
mes_nome = {
    1:'Jan', 2:'Fev', 3:'Mar', 4:'Abr',
    5:'Mai', 6:'Jun', 7:'Jul', 8:'Ago',
    9:'Set',10:'Out',11:'Nov',12:'Dez'
}

def last_day_of_month(date):
    if date.month == 12:
        return date.replace(day=31)
    return date.replace(month=date.month+1, day=1) - datetime.timedelta(days=1)


def extrai_data(date):

    datas = []
    date = date.replace('-','/')
    date = date.split()
    for dat in date:
        try:
            if re.search('^([0-9]|0[0-9]|1[0-9]|2[0-9]|3[0-1])(.|-)([0-9]|0[0-9]|1[0-2])(.|-|)20[0-9][0-9]$',dat):
                date_time_obj = datetime.datetime.strptime(dat, '%d/%m/%Y')
                datas.append(date_time_obj)
                datas.sort()

            elif re.search('^([0-9]|0[0-9]|1[0-9]|2[0-9]|3[0-1])(.|-)([0-9]|0[0-9]|1[0-2])(.|-|)[0-9][0-9]$',dat):
                date_time_obj = datetime.datetime.strptime(dat, '%d/%m/%y')
                datas.append(date_time_obj)
                datas.sort()


            elif re.search('^([0-9]|0[0-9]|1[0-9]|2[0-9]|3[0-1])(.|-)([0-9]|0[0-9]|1[0-2])$',dat):
                dat = dat + '/' +datetime.datetime.strftime(datetime.datetime.today(),'%y')
                date_time_obj = datetime.datetime.strptime(dat, '%d/%m/%y')
                datas.append(date_time_obj)

        except:
            pass
    if(len(datas)<2):
        datas.append(datas[0])
    return(datas)

def analisa(frase):
    try:
        saida = dict()
        user = frase.get('question')
        msg = clas.classifique(user)

        # producao
        if ('produção' in msg.keys()):
            #tem intervalo?
            if('ontem' in msg.keys() and msg['ontem']>1):
                d = datetime.datetime.now()- datetime.timedelta(days = 1)
                d = datetime.datetime.strftime(d, '%d/%m/%Y')
                d = '{} {}'.format(d,d)
                if(re.findall(r'(\d+\.\d+|\d+\,\d+)', user) and 'produto' in msg.keys()):
                    param = re.findall(r'(\d+\.\d+|\d+\,\d+)', user)
                    return busca_dados(d,param)
                else:
                    return busca_dados(d,'32')

            elif ('hoje' in msg.keys() and msg['hoje']>1):
                d = datetime.datetime.now()
                d = datetime.datetime.strftime(d, '%d/%m/%Y')
                d = '{} {}'.format(d,d)
                if(re.findall(r'(\d+\.\d+|\d+\,\d+)', user) and 'produto' in msg.keys()):
                    param = re.findall(r'(\d+\.\d+|\d+\,\d+)', user)
                    return busca_dados(d,param)
                else:
                    return busca_dados(d,'32')

            elif (extrai_data(user)):
                if(re.findall(r'(\d+\.\d+|\d+\,\d+)', user) and 'produto' in msg.keys()):
                    param = re.findall(r'(\d+\.\d+|\d+\,\d+)', user)
                    return busca_dados(user,param)
                else:
                    return busca_dados(user,'32')

            else:
                d = datetime.datetime.now()
                d = datetime.datetime.strftime(d, '%d/%m/%Y')
                d = '{} {}'.format(d,d)
                if(re.findall(r'(\d+\.\d+|\d+\,\d+)', user) and 'produto' in msg.keys()):
                    param = re.findall(r'(\d+\.\d+|\d+\,\d+)', user)
                    return busca_dados(d,param)
                else:
                    return busca_dados(d,'32')

        # qualidade
        if ('qualidade' in msg.keys()):
            #tem intervalo?
            if('ontem' in msg.keys()):
                if('média' in msg.keys()):
                    #chama calculo
                    pass
                elif('soma' in msg.keys()):
                    #chama calculo
                    pass
                else:
                    #chama calculo padrao
                    pass
            elif ('hoje' in msg.keys()):
                if('média' in msg.keys()):
                    #chama calculo
                    pass
                elif ('soma' in msg.keys()):
                    #chama calculo
                    pass
                else:
                    #chama calculo padrao
                    pass
            elif (extrai_data(user)):

                if('média' in msg.keys()):
                    #chama calculo
                    pass
                elif ('soma' in msg.keys()):
                    #chama calculo
                    pass
                else:
                    #chama calculo padrao
                    pass
        else:
            saida['answer'] = 'Sinceramente não entendi o que você falou ðﾟﾤﾔ!'
            return saida
    except:
        saida['answer'] = 'Ocorreu um erro enquanto eu fazia a consulta!'
        return saida

def busca_dados(raw_intervalo, parametro):

    try:
        if(len(parametro)>1):
            parametro = parametro.replace(',','.')
        else:
            parametro = parametro[0].replace(',','.')

        saida = dict()
        e = []
        datas = extrai_data(raw_intervalo)

        delta = datas[1] - datas[0]

        if(delta !=0):
            delta = delta.days
        else:
            delta =1

        for d in datas:
            e.append(datetime.datetime.strftime(d, '%d/%m/%Y'))
        datas = e

    #if(1):
        homerico_csv = homerico.RelatorioLista(datas[0], datas[1], '32')
        csv_file = StringIO(homerico_csv)
        df = pd.read_csv(csv_file, sep=';',dtype='object')

        df['size'] = df['Produto'].str.findall(r'\d+(?:,\d+)?').str[-1]
        df['size'] = df['size'].str.replace(',','.')
        df['size'] = df['size'].apply(pd.to_numeric,errors='coerce')
        df['Peso do Produto'] = df['Peso do Produto'].apply(pd.to_numeric,errors='coerce')
        #df = df.drop_duplicates(subset = ['size'])
        if(parametro !='32'):
            df = df[df['size'] == float(parametro)]

        df = df.filter(['DATA','Produto','Peso do Produto'])
        df.sort_values(by='DATA', inplace=True)
        x = df['Peso do Produto'].mean()
        z = df['Peso do Produto'].sum().round()/1000
        df['Total'] = x

        df = df.groupby(['Produto']).sum()/1000
        df = df.round(1)
        #df.reset_index(inplace=True)
        #df.reset_index(drop=True,inplace=True)
        if not(df.empty):
            df = df.filter(['Produto','Peso do Produto']).to_string()
            df = df.split('\n',1)[1]
            if (delta >1 and parametro =='32' ):
                saida['answer'] = (df + '\n\nMédia dos ({})dias : *{} tons/dia*'.format(delta,(z/delta).round(1)) +
                    '\n\nTotal Geral produzido no período: *{} toneladas*\n'.format((z).round(1)) + '')
            else: saida['answer'] = df + '\n\nTotal Geral produzido: {} toneladas\n'.format(z.round(1))
        else: saida['answer'] = 'Não encontrei nada com esse critério'
    except: saida['answer'] = 'Ocorreu um erro enquanto eu fazia a consulta!'
    return saida

def get_trim(cod):
    now = datetime.datetime.now()
    qt = str((now.month-1)//3+1)
    m = meses.get(qt)
    me = datetime.date.today()
    mon = list()
    mes = me.month
    for i in m:
        if i > mes: mon.append(None)
        elif i == mes:
            try:
                data = datetime.date(me.year,i,me.day).strftime('%d/%m/%Y')
                homerico_csv = homerico.RelatorioGerencialRegistro(data, cod)
                csv_file = StringIO(homerico_csv)
                df = pd.read_csv(csv_file, sep=';')
                mon.append(df['acumulado'].values[0])
            except: mon.append(None)
        else:
            try:
                data = datetime.date(me.year,i,last_day_of_month(datetime.date(me.year,i,1)).day).strftime('%d/%m/%Y')
                homerico_csv = homerico.RelatorioGerencialRegistro(data, cod)
                csv_file = StringIO(homerico_csv)
                df = pd.read_csv(csv_file, sep=';')
                mon.append(df['acumulado'].values[0])
            except: mon.append(None)
    lista = list()
    for i in m: lista.append(mes_nome[i])
    meta_json['meses'] = lista
    return(mon)

def get_meta_util_trf():
    try:
        mydb12 = mysql.connector.connect(host='192.168.17.61', user='Jayron', passwd='123456', port='3306', database='iba_i')
        query = open('sql/trf_util_shift.sql').read()

        try:
            df = pd.read_sql(query, mydb12)
            mydb12.close()

        except Exception as e:
            mydb12.close()

    except Exception as e: pass

    df['_0h'] = df._date.apply(lambda row : getEscala(dia = row)[0][0])
    df['_8h'] = df._date.apply(lambda row : getEscala(dia = row)[1][0])
    df['_16h'] = df._date.apply(lambda row : getEscala(dia = row)[2][0])
    df['_date'] = df['_date'].astype('str')
    dz = df
    hoje = datetime.date.today()
    Trimestre = str((hoje.month-1)//3+1)
    Tmeses = meses.get(Trimestre)
    mon = list()
    mes = hoje.month

    bn = df[df['_date']>=datetime.date(hoje.year,Tmeses[0],1).strftime('%Y-%m-%d')]
    bn = bn[bn['_date']<=datetime.date(hoje.year,hoje.month,hoje.day).strftime('%Y-%m-%d')]
    bn = bn.filter(['_date', 'M1','M2','M3', 'M4', 'M5', '_0h', '_8h','_16h'])
    bn = bn.drop(['M1'], axis=1)
    bn = bn.mean()
    bn = bn.mean()
    for m in Tmeses:
        if m > mes: mon.append(None)
        elif m == mes:
            try:
                dz = df[df['_date']>=datetime.date(hoje.year,hoje.month,1).strftime('%Y-%m-%d')]
                dz = dz[dz['_date']<=datetime.date(hoje.year,hoje.month,hoje.day).strftime('%Y-%m-%d')]
                dz = dz.filter(['_date', 'M1','M2','M3', 'M4', 'M5', '_0h', '_8h','_16h'])
                dz = dz.drop(['M1'], axis=1)
                dz = dz.mean()
                dz = dz.mean()
                mon.append(dz)
            except: mon.append(None)
        else:
            try:
                dz = df[df['_date']>=datetime.date(hoje.year,m,1).strftime('%Y-%m-%d')]
                dz = dz[dz['_date']<=datetime.date(hoje.year,m,last_day_of_month(datetime.date(hoje.year,m,1)).day).strftime('%Y-%m-%d')]
                dz = dz.filter(['_date', 'M1','M2','M3', 'M4', 'M5', '_0h', '_8h','_16h'])
                dz = dz.drop(['M1'], axis=1)
                dz = dz.mean()
                dz = dz.mean()
                mon.append(dz)
            except: mon.append(None)
    util_json = {}

    util_json['utilizacao'] = { 'meta': 0.0, 'dia': 0.0, 'acumulado': 0, 'mes1': 0.0, 'mes2': 0, 'mes3': 0 }
    util_json['utilizacao']['meta'] = 60.0
    util_json['utilizacao']['dia'] = 0.0
    util_json['utilizacao']['mes1'] = mon[0]
    util_json['utilizacao']['mes2'] = mon[1]
    util_json['utilizacao']['mes3'] = mon[2]
    util_json['utilizacao']['acumulado'] = bn

    return(util_json)

def get_meta_custo_trf():
    try:
        dbCusto = mysql.connector.connect(host='192.168.17.61', user='jayron', passwd='123123', port='1517', database='lam')
        queryC = 'SELECT * FROM wf_sap WHERE YEAR(data_msg)=2021;'
        dfC = pd.read_sql(queryC, dbCusto)
    except:
        dbCusto.close()
        print('Erro na conexão')

    hoje = datetime.date.today()
    #hoje = datetime.datetime.now()
    #hoje = datetime.date(2021,2,23)
    Trimestre = str((hoje.month-1)//3+1)
    Tmeses = meses.get(Trimestre)
    mon = list()
    mes = hoje.month
    #mes = datetime.date(2021,3,23).month
    dz = dfC

    #trimestre
    bn = dfC[dfC['DATA_MSG']>=datetime.date(hoje.year,Tmeses[0],1).strftime('%Y-%m-%d')]
    bn = bn[bn['DATA_MSG']<=datetime.date(hoje.year,hoje.month,hoje.day).strftime('%Y-%m-%d')]
    bn = bn['VALOR'].sum()
    ###########

    #dia
    bm = dfC[dfC['DATA_MSG']>=datetime.date(hoje.year,hoje.month,hoje.day).strftime('%Y-%m-%d')]
    bm = bm['VALOR'].sum()
    ###########

    for m in Tmeses:
        if m > mes: mon.append(None)
        elif m == mes:
            try:
                dz = dfC[dfC['DATA_MSG']>=datetime.date(hoje.year,hoje.month,1).strftime('%Y-%m-%d')]
                dz = dz[dz['DATA_MSG']<=datetime.date(hoje.year,hoje.month,hoje.day).strftime('%Y-%m-%d')]
                dz = dz['VALOR'].sum()
                mon.append(dz)
            except: mon.append(None)
        else:
            try:
                dz = dfC[dfC['DATA_MSG']>=datetime.date(hoje.year,m,1).strftime('%Y-%m-%d')]
                dz = dz[dz['DATA_MSG']<=datetime.date(hoje.year,m,last_day_of_month(datetime.date(hoje.year,m,1)).day).strftime('%Y-%m-%d')]
                dz = dz['VALOR'].sum()
                mon.append(dz)
            except: mon.append(None)

    custo_json = {}
    custo_json['custo'] = { 'meta': 0.0, 'dia': 0.0, 'acumulado': 0, 'mes1': 0.0, 'mes2': 0, 'mes3': 0 }
    custo_json['custo']['meta'] = 110.0
    custo_json['custo']['dia'] = bm
    custo_json['custo']['mes1'] = mon[0]
    custo_json['custo']['mes2'] = mon[1]
    custo_json['custo']['mes3'] = mon[2]
    custo_json['custo']['acumulado'] = bn

    return(custo_json)

def get_meta_5S_trf():
    try:
        db5S = mysql.connector.connect(host='192.168.17.61', user='jayron', passwd='123123', port='1517', database='lam')
        query5S = 'SELECT * FROM metas WHERE YEAR(data_msg)=2021 and nome_meta = "5S";'
        dfC = pd.read_sql(query5S, db5S)
    except:
        db5S.close()
        print('Erro na conexão')

    hoje = datetime.date.today()
    #hoje = datetime.datetime.now()
    #hoje = datetime.date(2021,2,23)
    Trimestre = str((hoje.month-1)//3+1)
    Tmeses = meses.get(Trimestre)
    mon = list()
    mes = hoje.month
    #mes = datetime.date(2021,3,23).month
    dz = dfC
    dz['DATA_MSG'] = dz['DATA_MSG'].astype('datetime64[ns]')
    #trimestre
    bn = dfC[dfC['DATA_MSG']>=datetime.date(hoje.year,Tmeses[0],1).strftime('%Y-%m-%d')]
    bn = bn[bn['DATA_MSG']<=datetime.date(hoje.year,hoje.month,hoje.day).strftime('%Y-%m-%d')]
    bn = bn['VALOR'].sum()
    ###########
    #dia
    bm = dfC[dfC['DATA_MSG']>=datetime.date(hoje.year,hoje.month,hoje.day).strftime('%Y-%m-%d')]
    bm = bm['VALOR'].sum()
    ###########

    for m in Tmeses:
        if m > mes: mon.append(None)
        elif m == mes:
            try:
                dz = dfC[dfC['DATA_MSG']>=datetime.date(hoje.year,hoje.month,1).strftime('%Y-%m-%d')]
                dz = dz[dz['DATA_MSG']<=datetime.date(hoje.year,hoje.month,hoje.day).strftime('%Y-%m-%d')]
                dz = dz['VALOR'].sum()
                mon.append(dz)
            except: mon.append(None)
        else:
            try:
                dz = dfC[dfC['DATA_MSG']>=datetime.date(hoje.year,m,1).strftime('%Y-%m-%d')]
                dz = dz[dz['DATA_MSG']<=datetime.date(hoje.year,m,last_day_of_month(datetime.date(hoje.year,m,1)).day).strftime('%Y-%m-%d')]
                dz = dz['VALOR'].sum()
                mon.append(dz)
            except: mon.append(None)

    M5S_json = {}
    M5S_json['5S'] = { 'meta': 0.0, 'dia': 0.0, 'acumulado': 0, 'mes1': 0.0, 'mes2': 0, 'mes3': 0 }
    M5S_json['5S']['meta'] = 90.0
    M5S_json['5S']['dia'] = 90
    M5S_json['5S']['mes1'] = mon[0]
    M5S_json['5S']['mes2'] = mon[1]
    M5S_json['5S']['mes3'] = mon[2]
    M5S_json['5S']['acumulado'] = bn

    return(M5S_json)

def get_meta_suca_trf():
    try:
        dbsuca = mysql.connector.connect(host='192.168.17.61', user='jayron', passwd='123123', port='1517', database='lam')
        querysuca = 'SELECT * FROM metas WHERE YEAR(data_msg)=2021 and nome_meta = "sucateamento";'
        dfC = pd.read_sql(querysuca, dbsuca)
    except:
        dbsuca.close()
        print('Erro na conexão')

    hoje = datetime.date.today()
    #hoje = datetime.datetime.now()
    #hoje = datetime.date(2021,2,23)
    Trimestre = str((hoje.month-1)//3+1)
    Tmeses = meses.get(Trimestre)
    mon = list()
    mes = hoje.month
    #mes = datetime.date(2021,3,23).month
    dz = dfC
    dz['DATA_MSG'] = dz['DATA_MSG'].astype('datetime64[ns]')
    #trimestre
    bn = dfC[dfC['DATA_MSG']>=datetime.date(hoje.year,Tmeses[0],1).strftime('%Y-%m-%d')]
    bn = bn[bn['DATA_MSG']<=datetime.date(hoje.year,hoje.month,hoje.day).strftime('%Y-%m-%d')]
    bn = bn['VALOR'].sum()
    ###########
    #dia
    bm = dfC[dfC['DATA_MSG']>=datetime.date(hoje.year,hoje.month,hoje.day).strftime('%Y-%m-%d')]
    bm = bm['VALOR'].sum()
    ###########

    for m in Tmeses:
        if m > mes: mon.append(None)
        elif m == mes:
            try:
                dz = dfC[dfC['DATA_MSG']>=datetime.date(hoje.year,hoje.month,1).strftime('%Y-%m-%d')]
                dz = dz[dz['DATA_MSG']<=datetime.date(hoje.year,hoje.month,hoje.day).strftime('%Y-%m-%d')]
                dz = dz['VALOR'].sum()
                mon.append(dz)
            except: mon.append(None)
        else:
            try:
                dz = dfC[dfC['DATA_MSG']>=datetime.date(hoje.year,m,1).strftime('%Y-%m-%d')]
                dz = dz[dz['DATA_MSG']<=datetime.date(hoje.year,m,last_day_of_month(datetime.date(hoje.year,m,1)).day).strftime('%Y-%m-%d')]
                dz = dz['VALOR'].sum()
                mon.append(dz)
            except: mon.append(None)

    sucata_json = {}
    sucata_json['sucateamento'] = { 'meta': 0.0, 'dia': 0.0, 'acumulado': 0, 'mes1': 0.0, 'mes2': 0, 'mes3': 0 }
    sucata_json['sucateamento']['meta'] = 3.0
    sucata_json['sucateamento']['dia'] = 0
    sucata_json['sucateamento']['mes1'] = mon[0]
    sucata_json['sucateamento']['mes2'] = mon[1]
    sucata_json['sucateamento']['mes3'] = mon[2]
    sucata_json['sucateamento']['acumulado'] = bn

    return(sucata_json)


registros = {'ACIDENTE CPT':1333,'PROD LAMINADO':1336,'REND. METALICO':1338,'BLBP':1444,'SUCATEAMENTO':1350}
values = {'dia':0,'meta':'N/A'}

meta_json = {
    'ACIDENTE CPT':{'meta':'','dia':0,'acumulado':0,'mes1':0,'mes2':0,'mes3':0},
    'PROD LAMINADO':{'meta':'','dia':0,'acumulado':0,'mes1':0,'mes2':0,'mes3':0}, \
    'REND. METALICO':{'meta':'','dia':0,'acumulado':0,'mes1':0,'mes2':0,'mes3':0},
    'BLBP':{'meta':'','dia':0,'acumulado':0,'mes1':0,'mes2':0,'mes3':0},
    'SUCATEAMENTO':{'meta':'','dia':0,'acumulado':0,'mes1':0,'mes2':0,'mes3':0},
    'meses':0
}

produto = ''

query_orcl = open('sql/query_orcl.sql').read()
query_mssql = open('sql/query_mssql.sql').read()
query_ultil = open('sql/query_ultil.sql').read()

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
        res = misc.requests.post(
            'http://localhost:3001/api/pda/',
            json=dict(tagname=tagname),
            auth=('client', '123456')
        )
        res = misc.json.loads(res.text)
    except: # If Server Not Responding
        res = dict(value=None, name=None, status='server down')

    # Return data
    return res

#################################################################################################################################################

def util():
    r = dict()
    gets = get_pda([
        'Modules.2 CTR_2.Analog.TIME_PLC_CTR',
        'Modules.2 CTR_2.Analog.TIME_UTIL_MILL'
    ])
    time = gets[0].get('value')
    util = gets[1].get('value')
    c = time != None and util != None
    r['UTIL'] = util / (time if time > 0 else 1) if c else None
    r['TEMPO_PARADO'] = ((time - util) / 60) if c else None
    return r

#################################################################################################################################################

def util_trf():
    # Open File
    gets = get_pda([
        'Modules.12 MILL_2.Analog.TIME_PLC_MIL',
        'Modules.12 MILL_2.Analog.TREFILA_01_UTIL_TIME',
        'Modules.12 MILL_2.Analog.TREFILA_02_UTIL_TIME',
        'Modules.12 MILL_2.Analog.TREFILA_03_UTIL_TIME',
        'Modules.12 MILL_2.Analog.TREFILA_04_UTIL_TIME',
        'Modules.12 MILL_2.Analog.TREFILA_05_UTIL_TIME'
    ])
    time = gets[0].get('value')
    # Parse Util
    def parse_util(mq):
        r = dict()
        util = gets[mq].get('value')
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

#string to number
def num(string, ptbr=False):
    if string == '': return None
    string = string.replace(' ','')
    if ptbr:
        string = string.replace('.','')
        string = string.replace(',','.')
    return float(string)

#csv to matrix
def matrix(txt, columnbreak=';', linebreak='\n'):
    return list(map(lambda line: line.split(columnbreak), txt.split(linebreak)))

#################################################################################################################################################

# relatorio gerencial parser
def get_relatorio_gerencial(rel, registros=dict(), date=None):
    _registros = copy.deepcopy(registros)
    if date == None: date = datetime.datetime.today().strftime('%d/%m/%Y')
    # private map function
    def _replace_reg(row):
        if row[0] in list(_registros.values()):
            for reg in _registros: row[0] = reg if (row[0] == _registros[reg]) else row[0]
            _registros[row[0]] = dict(
                meta = num(row[1],True),
                dia = num(row[2],True),
                acumulado = num(row[3],True))
        else: return None
        return row
    # get function
    for i in _registros: _registros[i] = str(_registros[i])
    homerico_csv = homerico.RelatorioGerencialReport(date, rel)
    list(map(_replace_reg, matrix(homerico_csv)))
    null_reg = dict(meta=None, dia=None, acumulado=None)
    for item in list(_registros): _registros[item] = copy.deepcopy(null_reg) if (type(_registros[item]) != dict) else _registros[item]
    return copy.deepcopy(_registros)

#################################################################################################################################################

# relatorio gerencial
def relatorio_gerencial(rel, registros=dict()):
    relatorio = get_relatorio_gerencial(rel, registros)
    today = datetime.date.today()
    qt = 3*((today.month-1)//3+1)
    m = [qt-2,qt-1,qt]
    for i in m:
        last_day = last_day_of_month(datetime.date(today.year,i,1)).day
        if i == today.month: last_day = today.day
        date = datetime.date(today.year,i,last_day).strftime('%d/%m/%Y')
        e = get_relatorio_gerencial(rel, registros, date)
        for item in relatorio:
            mes = 'mes{}'.format(i-qt+3)
            relatorio[item][mes] = e[item]['acumulado']
    return relatorio

#################################################################################################################################################

# relatorio gerencial
def relatorio_gerencial_registro(registro=''):
    date = datetime.datetime.today().strftime('%d/%m/%Y')
    homerico_csv = homerico.RelatorioGerencialRegistro(date, registro)
    return matrix(homerico_csv)

#################################################################################################################################################

# producao lista
def producao_lista(lista):
    hoje = datetime.date.today()
    ultimo_dia = last_day_of_month(hoje).strftime('%d/%m/%Y')
    homerico_csv = homerico.ProducaoLista(ultimo_dia, lista)
    dados = matrix(homerico_csv)
    dados.pop(0)
    d = list()
    for item in dados:
        if len(item) != 2: dados.pop(dados.index(item))
    for item in dados:
        date = '{}{}'.format(item[0][:2].zfill(2), ultimo_dia[2:])
        d.append(
            dict(data=date, peso=num(item[1], True))
        )
    return d

#################################################################################################################################################

# old function
def py_get_pims(req):
    # Check for input Variable
    if ('tagname' not in req or
        not isinstance(req['tagname'], str)
        ): return dict(error='tagname missing')

    # Get Query String
    string = open('sql/pims_get_tag.sql').read()
    string = string.format(req['tagname'])

    # Connnect to pims SQL Plus server
    conn = pyodbc.connect('DSN=IP21;UID=Administrator;PWD=gnsa2011*')
    cursor = conn.cursor()

    # Execute query
    cursor.execute(string)
    res = [dict((cursor.description[i][0], value) \
        for i, value in enumerate(row)) for row in cursor.fetchall()]
    cursor.connection.close()

    # check length of result
    if len(res) > 0: res = res[0]
    else: res = dict(error='not found')

    # Return data
    return res

#################################################################################################################################################
#                                                                    API ENDNODES                                                               #
#################################################################################################################################################

@api.add('/api/turma/')
def boletim_test(req):
    hoje = datetime.date.today()
    ontem = hoje - datetime.timedelta(days=1)
    hoje = hoje.strftime('%d/%m/%Y')
    ontem = ontem.strftime('%d/%m/%Y')
    e = [homerico.RelatorioBoletim(ontem, hoje, '31'),
        homerico.RelatorioBoletim(ontem, hoje, '35')]
    return e

#################################################################################################################################################

@api.add('/api/trf/')
def db_tref(req):
    hoje = datetime.datetime.today().strftime('%d/%m/%Y')
    homerico_csv = homerico.RelatorioLista(hoje, hoje, '50')
    csv_file = StringIO(homerico_csv)
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
    dt['p01'] = df.get('Trefila 01', None)
    dt['p02'] = df.get('Trefila 02', None)
    dt['p03'] = df.get('Trefila 03', None)
    dt['p04'] = df.get('Trefila 04', None)
    dt['p05'] = df.get('Trefila 05', None)
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

@api.add('/api/metas_lam_quente/')
def _metas_lam_quente(req):
    registros = {
        'ACIDENTE CPT':1333,
        'PROD LAMINADO':1336,
        'REND. METALICO':1338,
        'BLBP':1444,
        'SUCATEAMENTO':1350
        }
    registros = relatorio_gerencial('10', registros)
    return registros

#################################################################################################################################################

@api.add('/api/prod_lam_quente/')
def _prod_lam_quente(req):
    dados = producao_lista('1269')
    return dados

#################################################################################################################################################

@api.add('/api/metas_lam_frio/')
def _metas_lam_frio(req):
    registros = {
        'PRODUÇÃO':2962,
        'PRODUÇÃO HORÁRIA':2966,
        'RENDIMENTO METÁLICO':2963,
        'PRODUÇÃO POR MÁQUINA':2988
    }
    # util trf dia
    ut = util_trf()
    ut = [
        ut['m01']['UTIL'],
        ut['m02']['UTIL'],
        ut['m03']['UTIL'],
        ut['m04']['UTIL'],
        ut['m05']['UTIL']
    ]
    util = get_meta_util_trf()
    gen_util = dict(dia=((sum(ut) * 100) / 4))
    util['utilizacao'].update(gen_util)
    # custo trf
    custo_trf = get_meta_custo_trf()
    # sucateamento trf
    suca_trf = get_meta_suca_trf()
    # 5S
    m5s_trf = get_meta_5S_trf()
    # get metas
    registros = relatorio_gerencial('16', registros)
    registros.update(util)
    registros.update(custo_trf)
    registros.update(suca_trf)
    registros.update(m5s_trf)
    return registros

#################################################################################################################################################

@api.add('/api/prod_lam_frio/')
def _prod_lam_frio(req):
    dados = producao_lista('2361')
    return dados

#################################################################################################################################################

@api.add('/api/furnace/')
def db_orcl(req):
    con = cx_Oracle.connect('gusaapp/gusaapp@10.20.6.66/orcl')
    cur = con.cursor()
    cur.execute(query_orcl)
    r = [dict((cur.description[i][0], value)
        for i, value in enumerate(row)) for row in cur.fetchall()]
    r = r[0] if len(r) > 0 else dict()
    cur.connection.close()
    x = util()
    r['UTIL'] = x.get('UTIL')
    r['TEMPO_PARADO'] = x.get('TEMPO_PARADO')
    r['timestamp'] = datetime.datetime.today().strftime('%d/%m/%y %H:%M:%S')
    return r

#################################################################################################################################################

def db_mssql():
    conn = pyodbc.connect('DSN=iba;UID=sa;PWD=avb2020')
    cur = conn.cursor()
    cur.execute(query_mssql)
    r = [dict((cur.description[i][0], value)
        for i, value in enumerate(row)) for row in cur.fetchall()]
    r = r[0] if len(r) > 0 else dict()
    pname = r.get('CTR_PRODUCT_NAME')
    pname = pname.strip() if isinstance(pname, str) else None
    if pname != None: r['CTR_PRODUCT_NAME'] = pname
    cur.connection.close()
    return r

#################################################################################################################################################

@api.add('/api/aci_rendimento/')
def aci_rendimento(req):
    # get api data
    rend = relatorio_gerencial_registro('15')
    carg_s = relatorio_gerencial_registro('1218')

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

@api.add('/api/mill/')
def _db_mssql(req):
    return db_mssql()

#################################################################################################################################################

@api.add('/api/l2/')
def db_mssql2(req):
    produto = db_mssql().get('CTR_PRODUCT_NAME')
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

@api.add('/questions/', methods=['POST'])
def questions(req):
    print('data from client: {}'.format(req))
    dictToReturn = analisa(req)
    print('data to client: {}'.format(dictToReturn['answer']))
    return dictToReturn

#################################################################################################################################################

# start server
api.start()

# keep main thread alive
misc.keepalive()

#################################################################################################################################################
