
#################################################################################################################################################

# Imports
from os import getenv, path
from datetime import datetime, date
from pandas import DataFrame, read_sql, to_datetime
from mysql.connector import connect
from typing import Callable

# Modules
from .helpers import escalaTurno, lastDayOfMonth

#################################################################################################################################################

# Get File-Paths
fileDir = path.dirname(path.abspath(__file__))
util_sql = path.abspath(path.join(fileDir, '../sql/trefila.utilizacao.sql'))

##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################

class db:

    def iba():
        return connect(
            host=getenv('IBA_MYSQL_HOST'),
            user=getenv('IBA_MYSQL_USER'),
            passwd=getenv('IBA_MYSQL_PASSWORD'),
            port=getenv('IBA_MYSQL_PORT'),
            database=getenv('IBA_MYSQL_DATABASE')
        )

    def bot():
        return connect(
            host=getenv('BOT_MYSQL_HOST'),
            user=getenv('BOT_MYSQL_USER'),
            passwd=getenv('BOT_MYSQL_PASSWORD'),
            port=getenv('BOT_MYSQL_PORT'),
            database=getenv('BOT_MYSQL_DATABASE')
        )

##########################################################################################################################

def getMetaDay(
    df: DataFrame,
    now: datetime
) -> float:
    dt = to_datetime(date(now.year, now.month, now.day))
    return df[df['DATA_MSG'] >= dt]['VALOR'].sum()

#################################################################################################################################################

# Iterate over Months
def trimStartEndDates(
    month: int,
    now: datetime
) -> tuple[str, str]:
    if month > now.month: return (None, None)
    day = (
        now.day if month == now.month else
        lastDayOfMonth(date(now.year, month, 1)).day
    )
    sdate = date(now.year, month, 1)
    edate = date(now.year, now.month, day)
    return (sdate, edate)

#################################################################################################################################################

def getMetaTrim(
    df: DataFrame,
    now: datetime,
    parser: Callable[
        [DataFrame, tuple[date, date]],
        float
    ]
) -> dict[str, float]:
    # Trimestre
    tlst = dict[int, tuple[int, int, int]]
    trims: tlst = { 1: (1, 2, 3), 2: (4, 5, 6), 3: (7, 8, 9), 4: (10, 11, 12) }
    trim = trims[1 + ((now.month - 1) // 3)]
    # Helper Lambdas
    helper = lambda m: (m, lastDayOfMonth(date(now.year, m, 1)))
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
    df: DataFrame,
    dates: tuple[date, date]
) -> float:
    dts = (to_datetime(dates[0]), to_datetime(dates[1]))
    query = (dts[0] <= df['DATA_MSG']) & (df['DATA_MSG'] <= dts[1])
    return df[query]['VALOR'].sum()

#################################################################################################################################################

# Iterate over Months
def utilTrimParser(
    df: DataFrame,
    dates: tuple[date, date]
) -> float:
    dts = (to_datetime(dates[0]), to_datetime(dates[1]))
    query = (dts[0] <= df['_date']) & (df['_date'] <= dts[1])
    fltr = ['_date','M1','M2','M3','M4','M5','_0h','_8h','_16h']
    return df[query]['VALOR'].filter(fltr).drop(['M1'], axis=1).mean().mean()

##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################

def utilizacao():
    # Execute Query
    df = read_sql(
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
            df = read_sql(sql, connect.bot())
            # Datetime
            now = datetime.now()
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
            df = read_sql(sql, connect.bot())
            # Datetime
            now = datetime.now()
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
            df = read_sql(sql, connect.bot())
            # Datetime
            now = datetime.now()
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
            df = read_sql(sql, connect.iba())
            # Datetime
            now = datetime.now()

            # Update Shift Helper
            eTurno = lambda row: escalaTurno(data=row)
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
