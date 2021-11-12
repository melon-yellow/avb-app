
#################################################################################################################################################

# Imports
import os
import pandas
import datetime
import mysql.connector

# Modules
from . import helpers

#################################################################################################################################################

# Get File-Paths
fileDir = os.path.dirname(os.path.abspath(__file__))
util_sql = os.path.abspath(os.path.join(fileDir, './sql/trefila.utilizacao.sql'))

#################################################################################################################################################

mes_nome = {
    1:'Jan', 2:'Fev', 3:'Mar', 4:'Abr',
    5:'Mai', 6:'Jun', 7:'Jul', 8:'Ago',
    9:'Set', 10:'Out', 11:'Nov', 12:'Dez'
}
trims = {
    1: [1,2,3],
    2: [4,5,6],
    3: [7,8,9],
    4: [10,11,12]
}

#################################################################################################################################################

def utilizacaoMaquinas():
    # MySQL Connection
    db = mysql.connector.connect(
        host='gusal2',
        user='jayron',
        passwd='123456',
        port='3306',
        database='iba_i'
    )
    df = pandas.read_sql(
        open(util_sql).read(),
        db
    )
    db.close()
    # Return Data
    return str(df.to_csv())


#################################################################################################################################################

def utilizacao():
    try:
        db = mysql.connector.connect(
            host='gusal2',
            user='jayron',
            passwd='123456',
            port='3306',
            database='iba_i'
        )
        df = pandas.read_sql(
            open('sql/trf_util_shift.sql').read(),
            db
        )
        db.close()
    except: return {}

    df['_0h'] = df['_date'].apply(lambda row : helpers.escalaTurno(data=row)[0][0])
    df['_8h'] = df['_date'].apply(lambda row : helpers.escalaTurno(data=row)[1][0])
    df['_16h'] = df['_date'].apply(lambda row : helpers.escalaTurno(data=row)[2][0])
    df['_date'] = df['_date'].astype('str')

    hoje = datetime.datetime.now()
    trim = trims.get(
        ((hoje.month - 1) // 3) + 1
    )
    mon = list()
    mes = hoje.month

    bn = df[df['_date']>=datetime.date(hoje.year,trim[0],1).strftime('%Y-%m-%d')]
    bn = bn[bn['_date']<=datetime.date(hoje.year,hoje.month,hoje.day).strftime('%Y-%m-%d')]
    bn = bn.filter(['_date', 'M1','M2','M3', 'M4', 'M5', '_0h', '_8h','_16h'])
    bn = bn.drop(['M1'], axis=1)
    bn = bn.mean().mean()

    # Iterate over Months
    for m in trim:
        try:
            # Check Month
            if m > mes: raise Exception('invalid month')
            if m < mes:
                month = m
                last = helpers.lastDayOfMonth(
                    datetime.date(hoje.year,m,1)
                ).day
            if m == mes:
                month = hoje.month
                last = hoje.day
            # Get Data
            dz = df[df['_date']>=datetime.date(hoje.year, month, 1).strftime('%Y-%m-%d')]
            dz = dz[dz['_date']<=datetime.date(hoje.year, month, last).strftime('%Y-%m-%d')]
            dz = dz.filter(['_date', 'M1','M2','M3', 'M4', 'M5', '_0h', '_8h','_16h'])
            dz = dz.drop(['M1'], axis=1)
            dz = dz.mean().mean()
            mon.append(dz)
        # On Error
        except: mon.append(None)
    # Assembly Data
    util_json = {
        'utilizacao': {
            'meta': 60.0,
            'dia': 0.0,
            'acumulado': bn,
            'mes1': mon[0],
            'mes2': mon[1],
            'mes3': mon[2]
        }
    }
    # Return Data
    return util_json

#################################################################################################################################################

def custo():
    try:
        db = mysql.connector.connect(
            host='gusal2',
            user='jayron',
            passwd='123456',
            port='1517',
            database='lam'
        )
        df = pandas.read_sql(
            'SELECT * FROM wf_sap WHERE YEAR(data_msg) = 2021',
            db
        )
        db.close()
    except: return {}

    hoje = datetime.date.today()
    Tmeses = trims.get(
        ((hoje.month - 1) // 3) + 1
    )
    mon = list()
    mes = hoje.month

    #trimestre
    bn = df[df['DATA_MSG']>=datetime.date(hoje.year,Tmeses[0],1).strftime('%Y-%m-%d')]
    bn = bn[bn['DATA_MSG']<=datetime.date(hoje.year,hoje.month,hoje.day).strftime('%Y-%m-%d')]
    bn = bn['VALOR'].sum()
    ###########

    #dia
    bm = df[df['DATA_MSG']>=datetime.date(hoje.year,hoje.month,hoje.day).strftime('%Y-%m-%d')]
    bm = bm['VALOR'].sum()
    ###########

    for m in Tmeses:
        if m > mes: mon.append(None)
        elif m == mes:
            try:
                dz = df[df['DATA_MSG']>=datetime.date(hoje.year,hoje.month,1).strftime('%Y-%m-%d')]
                dz = dz[dz['DATA_MSG']<=datetime.date(hoje.year,hoje.month,hoje.day).strftime('%Y-%m-%d')]
                dz = dz['VALOR'].sum()
                mon.append(dz)
            except: mon.append(None)
        else:
            try:
                dz = df[df['DATA_MSG']>=datetime.date(hoje.year,m,1).strftime('%Y-%m-%d')]
                dz = dz[dz['DATA_MSG']<=datetime.date(hoje.year,m, helpers.lastDayOfMonth(datetime.date(hoje.year,m,1)).day).strftime('%Y-%m-%d')]
                dz = dz['VALOR'].sum()
                mon.append(dz)
            except: mon.append(None)
    # Assembly Data
    custo_json = {
        'custo': {
            'meta': 110.0,
            'dia': bm,
            'acumulado': bn,
            'mes1': mon[0],
            'mes2': mon[1],
            'mes3': mon[2]
        }
    }
    # Retrun Data
    return custo_json

#################################################################################################################################################

def vs():
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
        return {}

    hoje = datetime.date.today()
    Tmeses = trims.get(
        ((hoje.month - 1) // 3) + 1
    )
    mon = list()
    mes = hoje.month
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
                dz = dz[dz['DATA_MSG']<=datetime.date(hoje.year, m, helpers.lastDayOfMonth(datetime.date(hoje.year,m,1)).day).strftime('%Y-%m-%d')]
                dz = dz['VALOR'].sum()
                mon.append(dz)
            except: mon.append(None)
    # Assembly Data
    M5S_json = {
        '5S': {
            'meta': 90,
            'dia': 90,
            'acumulado': bn,
            'mes1': mon[0],
            'mes2': mon[1],
            'mes3': mon[2]
        }
    }
    # Return Data
    return M5S_json

#################################################################################################################################################

def sucata():
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
        return {}

    hoje = datetime.date.today()
    Tmeses = trims.get(
        ((hoje.month - 1) // 3) + 1
    )
    mon = list()
    mes = hoje.month
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
                dz = dz[dz['DATA_MSG']<=datetime.date(hoje.year, m, helpers.lastDayOfMonth(datetime.date(hoje.year,m,1)).day).strftime('%Y-%m-%d')]
                dz = dz['VALOR'].sum()
                mon.append(dz)
            except: mon.append(None)

    sucata_json = {
        'sucateamento': {
            'meta': 3,
            'dia': 0,
            'acumulado': bn,
            'mes1': mon[0],
            'mes2': mon[1],
            'mes3': mon[2]
        }
    }

    return sucata_json

#################################################################################################################################################
