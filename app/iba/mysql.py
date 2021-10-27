
#################################################################################################################################################

# Imports
import os
import pandas
import mysql.connector
import datetime

# Modules
from .. import turno

#################################################################################################################################################

# Get File-Paths
fileDir = os.path.dirname(__file__)
util_sql = os.path.abspath(os.path.join(fileDir, '../sql/trefila.util.sql'))
util_day_sql = os.path.abspath(os.path.join(fileDir, '../sql/trefila.util.dia.sql'))

#################################################################################################################################################

def UtilizacaoTrefila():
    # MySQL Connection
    mydb = mysql.connector.connect(
        host='127.0.0.1',
        user='Jayron',
        passwd='123456',
        port='3306',
        database='iba_i'
    )
    df = pandas.read_sql(
        open(util_sql).read(),
        mydb
    )
    mydb.close()
    # Processing
    meses = {'1':[1,2,3],'2':[4,5,6],'3':[7,8,9],'4':[10,11,12]}
    df['_0h'] = df._date.apply(lambda row : turno.escala.get(dia = row)[0][0])
    df['_8h'] = df._date.apply(lambda row : turno.escala.get(dia = row)[1][0])
    df['_16h'] = df._date.apply(lambda row : turno.escala.get(dia = row)[2][0])
    df['_date'] = df['_date'].astype('str')
    hoje = datetime.date.today()
    Trimestre = str((hoje.month-1)//3+1)
    Tmeses = meses.get(Trimestre)
    bn = df[df['_date'] >= datetime.date(hoje.year, Tmeses[0], 1).strftime("%Y-%m-%d")]
    bn = bn[bn['_date'] <= hoje.strftime("%Y-%m-%d")]
    bn = bn.filter(['_date','M1','M2','M3','M4','M5','_0h','_8h','_16h'])
    bn = bn.drop(['M1'], axis=1)
    bn['Global'] = (bn['M2']+bn['M3']+bn['M4']+bn['M5']) / 4
    # Retrun Data
    return str(bn.to_csv())

#################################################################################################################################################

def UtilizacaoDiaTrefila():
    # MySQL Connection
    mydb = mysql.connector.connect(
        host='127.0.0.1',
        user='Jayron',
        passwd='123456',
        port='3306',
        database='iba_i'
    )
    csv = str(
        pandas.read_sql(
            open(util_day_sql).read(),
            mydb
        ).to_csv()
    )
    mydb.close()
    # Return Data
    return csv

#################################################################################################################################################
