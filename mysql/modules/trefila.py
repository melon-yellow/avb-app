
#################################################################################################################################################

# Imports
import os
import pandas
import datetime
import mysql.connector
from typing import Callable, Tuple

# Modules
from . import helpers

#################################################################################################################################################

# Get File-Paths
fileDir = os.path.dirname(os.path.abspath(__file__))
util_sql = os.path.abspath(os.path.join(fileDir, '../sql/trefila.utilizacao.sql'))

##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################

class connect:

    def iba():
        return mysql.connector.connect(
            host=os.getenv('IBA_MYSQL_HOST'),
            user=os.getenv('IBA_MYSQL_USER'),
            passwd=os.getenv('IBA_MYSQL_PASSWORD'),
            port=os.getenv('IBA_MYSQL_PORT'),
            database=os.getenv('IBA_MYSQL_DATABASE')
        )

    def bot():
        return mysql.connector.connect(
            host=os.getenv('BOT_MYSQL_HOST'),
            user=os.getenv('BOT_MYSQL_USER'),
            passwd=os.getenv('BOT_MYSQL_PASSWORD'),
            port=os.getenv('BOT_MYSQL_PORT'),
            database=os.getenv('BOT_MYSQL_DATABASE')
        )

#################################################################################################################################################

# Datetime Helpers
def date(year: int, month: int, day: int = 1):
    return datetime.date(year, month, day)

def dateFormat(year: int, month: int, day: int = 1):
    return pandas.to_datetime(date(year, month, day).strftime('%Y-%m-%d')).date()

##########################################################################################################################

def getMetaDay(
    df: pandas.DataFrame,
    now: datetime.datetime
):
    # Meta Dia
    ed = dateFormat(now.year, now.month, now.day)
    return df[df['DATA_MSG'] >= ed]['VALOR'].sum()

#################################################################################################################################################

# Iterate over Months
def trimStartEndDates(
    month: int,
    now: datetime.datetime
) -> Tuple[datetime.datetime, datetime.datetime]:
    if month > now.month: return (None, None)
    day = (
        now.day if month == now.month else
        helpers.lastDayOfMonth(date(now.year, month, 1)).day
    )
    start_date = dateFormat(now.year, month, 1)
    end_date = dateFormat(now.year, now.month, day)
    return (start_date, end_date)

#################################################################################################################################################

def getMetaTrim(
    df: pandas.DataFrame,
    now: datetime.datetime,
    parser: Callable[
        [pandas.DataFrame, Tuple[datetime.datetime, datetime.datetime]],
        float
    ]
):
    # Trimestre
    tlst = dict[int, tuple[int, int, int]]
    trims: tlst = { 1: (1, 2, 3), 2: (4, 5, 6), 3: (7, 8, 9), 4: (10, 11, 12) }
    trim = trims[1 + ((now.month - 1) // 3)]
    # Helper Lambdas
    helper = lambda m: (m, helpers.lastDayOfMonth(date(now.year, m, 1)))
    # Return Data
    return {
        'acumulado': parser(df, trimStartEndDates(trim[0], now)),
        'mes1': parser(df, trimStartEndDates(*helper(trim[0]))),
        'mes2': parser(df, trimStartEndDates(*helper(trim[1]))),
        'mes3': parser(df, trimStartEndDates(*helper(trim[2])))
    }

#################################################################################################################################################

# Iterate over Months
def metaTrimParser(
    df: pandas.DataFrame,
    dates: Tuple[datetime.datetime, datetime.datetime]
) -> float:
    query = (dates[0] <= df['DATA_MSG']) & (df['DATA_MSG'] <= dates[1])
    return df[query]['VALOR'].sum()

#################################################################################################################################################

# Iterate over Months
def utilTrimParser(
    df: pandas.DataFrame,
    dates: Tuple[datetime.datetime, datetime.datetime]
) -> float:
    query = (dates[0] <= df['_date']) & (df['_date'] <= dates[1])
    fltr = ['_date','M1','M2','M3','M4','M5','_0h','_8h','_16h']
    return df[query]['VALOR'].filter(fltr).drop(['M1'], axis=1).mean().mean()

##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################

def utilizacao():
    # Execute Query
    df = pandas.read_sql(
        open(util_sql).read(),
        connect.iba()
    )
    # Return Data
    return str(df.to_csv())

#################################################################################################################################################

# Metas Class
class metas:

    #################################################################################################################################################

    def custo():
        try: # Connect
            sql = 'SELECT * FROM wf_sap WHERE (YEAR(data_msg) = 2022)'
            df = pandas.read_sql(sql, connect.bot())
            # Datetime
            now = datetime.datetime.now()
            # Get Meta Parser
            day = getMetaDay(df, now)
            meta = getMetaTrim(df, now, metaTrimParser)
            meta.update({ 'meta': 110, 'dia': day })
            # Return Data
            return { 'custo': meta }
        # On Error
        except Exception as e:
            return { 'custo': { 'error': f'{e}' } }

    #################################################################################################################################################

    def cincos():
        try: # Connect
            sql = 'SELECT * FROM metas WHERE (YEAR(data_msg) = 2022) AND (nome_meta = "5S")'
            df = pandas.read_sql(sql, connect.bot())
            # Datetime
            now = datetime.datetime.now()
            # Get Meta Parser
            day = getMetaDay(df, now)
            meta = getMetaTrim(df, now, metaTrimParser)
            meta.update({ 'meta': 90, 'dia': day })
            # Return Data
            return { '5S': meta }
        # On Error
        except Exception as e:
            return { '5S': { 'error': f'{e}' } }

    #################################################################################################################################################

    def sucata():
        try: # Connect
            sql = 'SELECT * FROM metas WHERE (YEAR(data_msg) = 2022) AND (nome_meta = "sucateamento")'
            df = pandas.read_sql(sql, connect.bot())
            # Datetime
            now = datetime.datetime.now()
            # Get Meta Parser
            day = getMetaDay(df, now)
            meta = getMetaTrim(df, now, metaTrimParser)
            meta.update({ 'meta': 3, 'dia': day })
            # Return Data
            return { 'sucateamento': meta }
        # On Error
        except Exception as e:
            return { 'sucateamento': { 'error': f'{e}' } }

    #################################################################################################################################################

    def utilizacao():
        try: # Connect 
            sql = open(util_sql).read()
            df = pandas.read_sql(sql, connect.iba())
            # Datetime
            now = datetime.datetime.now()

            # Update Shift Helper
            eTurno = lambda row: helpers.escalaTurno(data=row)
            turnoIndex = lambda i: (lambda row : eTurno(row)[i][0])

            # Update Shift
            df['_0h'] = df['_date'].apply(turnoIndex(0))
            df['_8h'] = df['_date'].apply(turnoIndex(1))
            df['_16h'] = df['_date'].apply(turnoIndex(2))
            df['_date'] = df['_date'].astype('str')

            # Assembly Data
            meta = getMetaTrim(df, now, utilTrimParser)
            meta.update({ 'meta': 60, 'dia': 0 })
            # Return Data
            return { 'utilizacao': meta }
        # On Error
        except Exception as e:
            return { 'utilizacao': { 'error': f'{e}' } }

##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################
