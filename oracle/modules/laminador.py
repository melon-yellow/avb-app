
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

async def get_util():
    try:
        (
            (ok1, util),
            (ok2, time_util),
            (ok3, time_plc)
        ) = await gather(
            fromIba('0:5'),
            fromIba('2:25'),
            fromIba('2:26')
        )
        # Check Response
        if not ok1: raise util
        if not ok2: raise time_util
        if not ok3: raise time_plc
        # Update Data
        stop = (time_plc - time_util) / 60
        data = {
            'UTIL': util,
            'TEMPO_PARADO': stop
        }
        # Return Data
        return (True, data)
    except Exception as error:
        return (False, error)

#################################################################################################################################################

async def forno():
    try:
        data = {}
        (
            (ok1, furnace),
            (ok2, util)
        ) = await gather(
            gusaapp(),
            get_util()
        )
        # Check Response
        if not ok1: raise furnace
        if not ok2: raise util
        # Update Data
        data.update(furnace)
        data.update(util)
        # Return Data
        return (True, data)
    except Exception as error:
        return (False, error)

#################################################################################################################################################
