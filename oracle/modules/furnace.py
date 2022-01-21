
#################################################################################################################################################

# Imports
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

def gusaapp():
    # Connect to Server
    conn = db.furnace()
    # Execute Query
    data = execute(conn, open(gusaapp_sql).read())
    # Update Data
    (ok, util) = fromIba('0:5')
    (ok, time_util) = fromIba('2:25')
    (ok, time_plc) = fromIba('2:26')
    time_stopped = (time_plc - time_util) / 60
    data[0].update({'UTIL': util, 'TEMPO_PARADO': time_stopped})
    # Return Data
    return data[0]

#################################################################################################################################################
