
#################################################################################################################################################

# Imports
from os import getenv, path
from cx_Oracle import connect

# Modules
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
    # Return Data
    return data[0]

#################################################################################################################################################
