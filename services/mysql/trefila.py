
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
util_sql = os.path.abspath(os.path.join(fileDir, './sql/trefila.utilizacao.sql'))

##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################

class connect:

    def iba():
        return mysql.connector.connect(
            host='192.168.17.61',
            user='jayron',
            passwd='123456',
            port='3306',
            database='iba_i'
        )

    def bot():
        return mysql.connector.connect(
            host='192.168.17.61',
            user='jayron',
            passwd='123456',
            port='1517',
            database='lam'
        )

#################################################################################################################################################

# Datetime Helper
def dateFormat(
    year: int,
    month: int,
    day: int
):
    return datetime.datetime(
        year, month, day
    ).strftime('%Y-%m-%d')

#################################################################################################################################################

def getMetaTrimestre(
    now: datetime.datetime,
    parser: Callable[[int, int, int], float]
):
    try:
        # Trimestre
        trim: tuple[int, int, int] = {
            1: (1, 2, 3), 2: (4, 5, 6),
            3: (7, 8, 9), 4: (10, 11, 12)
        }[1 + ((now.month - 1) // 3)]

        # Acumulado do Trimestre
        acc = parser(trim[0], now.month, now.day)

        # Iterate over Months
        def getMonths(month: int) -> float:
            # Check Input
            if month > now.month: raise Exception('invalid month')
            if month == now.month: return parser(month, month, now.day)
            if month < now.month: return parser(month, month,
                helpers.lastDayOfMonth(
                    datetime.datetime(now.year, month, 1)
                ).day
            )

        # Return Data
        return {
            'acumulado': acc,
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

def utilizacaoTurno():
    # Execute Query
    df = pandas.read_sql(
        open(util_sql).read(),
        connect.iba()
    )
    # Return Data
    return str(df.to_csv())

#################################################################################################################################################

def utilizacao():
    try:
        # Execute Query
        df = pandas.read_sql(
            open('sql/trf_util_shift.sql').read(),
            connect.iba()
        )
        # Datetime
        now = datetime.datetime.now()

        # Update Shift Helper
        escalaIndex = lambda i: (
            lambda row : helpers.escalaTurno(data=row)[i][0]
        )

        # Update Shift
        df['_0h'] = df['_date'].apply(escalaIndex(0))
        df['_8h'] = df['_date'].apply(escalaIndex(1))
        df['_16h'] = df['_date'].apply(escalaIndex(2))
        df['_date'] = df['_date'].astype('str')

        # Parser Function
        def parser(initMonth: int, month: int, day: int):
            s = dateFormat(now.year, initMonth, 1)
            e = dateFormat(now.year, month, day)
            return float(
                df[(s <= df['_date']) & (df['_date'] <= e)].filter([
                    '_date', 'M1','M2','M3', 'M4', 'M5', '_0h', '_8h','_16h'
                ]).drop(['M1'], axis=1).mean().mean()
            )

        # Assembly Data
        meta = getMetaTrimestre(now, parser)
        meta.update({ 'meta': 60, 'dia': 0 })
        # Return Data
        return { 'utilizacao': meta }
    # On Error
    except: return {}

#################################################################################################################################################

def custo():
    try: # Connect
        df = pandas.read_sql(
            'SELECT * FROM wf_sap WHERE YEAR(data_msg) = 2021',
            connect.bot()
        )
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
    except: return {}

#################################################################################################################################################

def cincos():
    try: # Connect
        df = pandas.read_sql(
            'SELECT * FROM metas WHERE (YEAR(data_msg) = 2021) and (nome_meta = "5S")',
            connect.bot()
        )
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
    except: return {}

#################################################################################################################################################

def sucata():
    try: # Connect
        df = pandas.read_sql(
            'SELECT * FROM metas WHERE (YEAR(data_msg) = 2021) and (nome_meta = "sucateamento")',
            connect.bot()
        )
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
    except: return {}

##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################
