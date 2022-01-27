
#################################################################################################################################################

# Imports
from asyncio import gather
from os import getenv, path
from cx_Oracle import connect

# Modules
from .iba import read as fromIba
from .helpers import execute

#################################################################################################################################################

fileDir = path.dirname(path.abspath(__file__))
gusaapp_sql = path.abspath(path.join(fileDir, '../sql/furnace.gusaapp.sql'))

##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################

class db:

    def furnace():
        return connect(
            dsn=getenv('FURNACE_ORACLE_DB_DSN'),
            user=getenv('FURNACE_ORACLE_DB_USER'),
            password=getenv('FURNACE_ORACLE_DB_PASSWORD'),
            encoding='UTF-8'
        )

#################################################################################################################################################

async def gusaapp():
    try:
        # Connect to Server
        conn = db.furnace()
        # Execute Query
        data = execute(conn, open(gusaapp_sql).read())
        # Return Data
        return (True, data[0])
    except Exception as error:
        return (False, error)

#################################################################################################################################################

async def forno():
    try:
        # Read Data
        (
            (ok1, data),
            (ok2, util),
            (ok3, time_util),
            (ok4, time_plc)
        ) = await gather(
            gusaapp(),
            fromIba('0:5'),
            fromIba('2:25'),
            fromIba('2:26')
        )
        # check errors
        if not ok1: raise data
        if not ok2: raise util
        if not ok3: raise time_util
        if not ok4: raise time_plc
        # Update Data
        time_stopped = (time_plc - time_util) / 60
        data.update({'UTIL': util, 'TEMPO_PARADO': time_stopped})
        # Return Data
        return (True, data)
    except Exception as error:
        return (False, error)

#################################################################################################################################################
