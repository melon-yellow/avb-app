
#################################################################################################################################################

# Imports
import os
import pandas
import datetime
import mysql.connector
from typing import Callable

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
    return date(year, month, day).strftime('%Y-%m-%d')

#################################################################################################################################################

def getMetaTrimestre(
    now: datetime.datetime,
    parser: Callable[[int, int, int], float]
):
    try:
        # Iterate over Months
        def getMonths(month: int) -> float:
            if month > now.month: return
            else: return parser(month, month,
                now.day if month == now.month else
                helpers.lastDayOfMonth(date(now.year, month)).day
            )
        
        # Trimestre
        trims = { 1: (1, 2, 3), 2: (4, 5, 6), 3: (7, 8, 9), 4: (10, 11, 12) }
        trim: tuple[int, int, int] = trims[1 + ((now.month - 1) // 3)]

        # Return Data
        return {
            'acumulado': parser(trim[0], now.month, now.day),
            'mes1': getMonths(trim[0]),
            'mes2': getMonths(trim[1]),
            'mes3': getMonths(trim[2])
        }
    # On Error
    except: return {}

##########################################################################################################################

def getMeta(
    now: datetime.datetime,
    df: pandas.DataFrame
):
    # Meta Dia
    ed = dateFormat(now.year, now.month, now.day)
    day = df.query(f'DATA_MSG >= "{ed}"')['VALOR'].sum()
    # Parser Function
    def parser(initMonth: int, month: int, day: int):
        s = dateFormat(now.year, initMonth, 1)
        e = dateFormat(now.year, month, day)
        return df.query(f'"{s}" <= DATA_MSG & DATA_MSG <= "{e}"')['VALOR'].sum()
    
    # Return Data
    return (day, parser)


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
            sql = 'SELECT * FROM wf_sap WHERE (YEAR(data_msg) = 2021)'
            df = pandas.read_sql(sql, connect.bot())
            # Datetime
            now = datetime.datetime.now()
            # Get Meta Parser
            (day, parser) = getMeta(now, df)
            # Assembly Data
            meta = getMetaTrimestre(now, parser)
            meta.update({ 'meta': 110, 'dia': day })
            # Return Data
            return { 'custo': meta }
        # On Error
        except Exception as e:
            return { 'custo': { 'error': f'{e}' } }

    #################################################################################################################################################

    def cincos():
        try: # Connect
            sql = 'SELECT * FROM metas WHERE (YEAR(data_msg) = 2021) AND (nome_meta = "5S")'
            df = pandas.read_sql(sql, connect.bot())
            # Datetime
            now = datetime.datetime.now()
            # Get Meta Parser
            (day, parser) = getMeta(now, df)
            # Assembly Data
            meta = getMetaTrimestre(now, parser)
            meta.update({ 'meta': 90, 'dia': 90 })
            # Return Data
            return { '5S': meta }
        # On Error
        except Exception as e:
            return { '5S': { 'error': f'{e}' } }

    #################################################################################################################################################

    def sucata():
        try: # Connect
            sql = 'SELECT * FROM metas WHERE (YEAR(data_msg) = 2021) AND (nome_meta = "sucateamento")'
            df = pandas.read_sql(sql, connect.bot())
            # Datetime
            now = datetime.datetime.now()
            # Get Meta Parser
            (day, parser) = getMeta(now, df)
            # Assembly Data
            meta = getMetaTrimestre(now, parser)
            meta.update({ 'meta': 3, 'dia': 0 })
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

            # Parser Function
            def parser(initMonth: int, month: int, day: int):
                s = dateFormat(now.year, initMonth, 1)
                e = dateFormat(now.year, month, day)
                return df.query(f'"{s}" <= _date & _date <= "{e}"').filter([
                    '_date','M1','M2','M3','M4','M5','_0h','_8h','_16h'
                ]).drop(['M1'], axis=1).mean().mean()

            # Assembly Data
            meta = getMetaTrimestre(now, parser)
            meta.update({ 'meta': 60, 'dia': 0 })
            # Return Data
            return { 'utilizacao': meta }
        # On Error
        except Exception as e:
            return { 'utilizacao': { 'error': f'{e}' } }

##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################
