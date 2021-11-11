
#################################################################################################################################################

# Imports
import datetime
import mysql.connector
import pandas
import io

# Modules
from .. import turno
from .. import homerico

#################################################################################################################################################

mes_nome = {
    1:'Jan', 2:'Fev', 3:'Mar', 4:'Abr',
    5:'Mai', 6:'Jun', 7:'Jul', 8:'Ago',
    9:'Set', 10:'Out', 11:'Nov', 12:'Dez'
}
meses = {'1':[1,2,3],'2':[4,5,6],'3':[7,8,9],'4':[10,11,12]}

#################################################################################################################################################

def Trim(cod):
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
                homerico_csv = homerico.get.RelatorioGerencialRegistro(data, cod)
                csv_file = io.StringIO(homerico_csv)
                df = pandas.read_csv(csv_file, sep=';')
                mon.append(df['acumulado'].values[0])
            except: mon.append(None)
        else:
            try:
                data = datetime.date(me.year,i, homerico.get.LastDayOfMonth(datetime.date(me.year,i,1)).day).strftime('%d/%m/%Y')
                homerico_csv = homerico.RelatorioGerencialRegistro(data, cod)
                csv_file = io.StringIO(homerico_csv)
                df = pandas.read_csv(csv_file, sep=';')
                mon.append(df['acumulado'].values[0])
            except: mon.append(None)
    lista = list()
    for i in m: lista.append(mes_nome[i])
    return(mon)

#################################################################################################################################################

def Utilizacao():
    try:
        mydb12 = mysql.connector.connect(
            host='gusal2',
            user='jayron',
            passwd='123456',
            port='3306',
            database='iba_i'
        )
        query = open('sql/trf_util_shift.sql').read()
        df = pandas.read_sql(query, mydb12)

        try: mydb12.close()
        except: pass

    except: return

    df['_0h'] = df._date.apply(lambda row : turno.escala.get(dia = row)[0][0])
    df['_8h'] = df._date.apply(lambda row : turno.escala.get(dia = row)[1][0])
    df['_16h'] = df._date.apply(lambda row : turno.escala.get(dia = row)[2][0])
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
                dz = df[df['_date']>=datetime.date(hoje.year, m, 1).strftime('%Y-%m-%d')]
                dz = dz[dz['_date']<=datetime.date(hoje.year, m, homerico.get.LastDayOfMonth(datetime.date(hoje.year,m,1)).day).strftime('%Y-%m-%d')]
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

#################################################################################################################################################

def Custo():
    try:
        dbCusto = mysql.connector.connect(
            host='gusal2',
            user='jayron',
            passwd='123456',
            port='1517',
            database='lam'
        )
        queryC = 'SELECT * FROM wf_sap WHERE YEAR(data_msg)=2021;'
        dfC = pandas.read_sql(queryC, dbCusto)
    except:
        try: dbCusto.close()
        except: pass
        return

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
                dz = dz[dz['DATA_MSG']<=datetime.date(hoje.year,m, homerico.get.LastDayOfMonth(datetime.date(hoje.year,m,1)).day).strftime('%Y-%m-%d')]
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

#################################################################################################################################################

def S5():
    try:
        db5S = mysql.connector.connect(
            host='gusal2',
            user='jayron',
            passwd='123456',
            port='1517',
            database='lam'
        )
        query5S = 'SELECT * FROM metas WHERE YEAR(data_msg)=2021 and nome_meta = "5S";'
        dfC = pandas.read_sql(query5S, db5S)
    except:
        try: db5S.close()
        except: pass
        return

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
                dz = dfC[dfC['DATA_MSG']>=datetime.date(hoje.year, m, 1).strftime('%Y-%m-%d')]
                dz = dz[dz['DATA_MSG']<=datetime.date(hoje.year, m, homerico.get.LastDayOfMonth(datetime.date(hoje.year,m,1)).day).strftime('%Y-%m-%d')]
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

#################################################################################################################################################

def Sucata():
    try:
        dbSuca = mysql.connector.connect(
            host='gusal2',
            user='jayron',
            passwd='123456', 
            port='1517',
            database='lam'
        )
        querysuca = 'SELECT * FROM metas WHERE YEAR(data_msg)=2021 and nome_meta = "sucateamento";'
        dfC = pandas.read_sql(querysuca, dbSuca)
    except:
        try: dbSuca.close()
        except: pass
        return

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
                dz = dfC[dfC['DATA_MSG']>=datetime.date(hoje.year, m, 1).strftime('%Y-%m-%d')]
                dz = dz[dz['DATA_MSG']<=datetime.date(hoje.year, m, homerico.get.LastDayOfMonth(datetime.date(hoje.year,m,1)).day).strftime('%Y-%m-%d')]
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

#################################################################################################################################################
