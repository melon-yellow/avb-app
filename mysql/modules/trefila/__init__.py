
#################################################################################################################################################

# Imports
from os import getenv, path
from datetime import datetime
from pandas import read_sql
from mysql.connector import connect

# Modules
from ..iba import read as fromIba
from .metas import getMetaDay, getMetaTrim, metaTrimParser, utilTrimParser
from ..helpers import escalaTurno

#################################################################################################################################################

# Get File-Paths
fileDir = path.dirname(path.abspath(__file__))
util_sql = path.abspath(path.join(fileDir, '../sql/trefila.utilizacao.sql'))

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
        except Exception as error:
            return { 'custo': { 'error': f'{error}' } }

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
        except Exception as error:
            return { '5S': { 'error': f'{error}' } }

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
        except Exception as error:
            return { 'sucateamento': { 'error': f'{error}' } }

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
            # util trf dia
            util = fromIba('0:45')
            total = (
                util['m01']['UTIL'] +
                util['m02']['UTIL'] +
                util['m03']['UTIL'] +
                util['m04']['UTIL'] +
                util['m05']['UTIL']
            )
            dia = (total / 4) * 100
            # update util
            meta.update({ 'meta': 60, 'dia': dia })
            # Return Data
            return { 'utilizacao': meta }
        # On Error
        except Exception as error:
            return { 'utilizacao': { 'error': f'{error}' } }

##########################################################################################################################
