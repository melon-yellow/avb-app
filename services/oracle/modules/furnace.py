
#################################################################################################################################################

# Imports
import os
import cx_Oracle

# Modules
from . import helpers

#################################################################################################################################################

fileDir = os.path.dirname(os.path.abspath(__file__))
gusaapp_sql = os.path.abspath(os.path.join(fileDir, './sql/furnace.gusaapp.sql'))

##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################

class connect:

    def furnace():
        return cx_Oracle.connect(
            dsn=os.getenv('FURNACE_ORACLE_DB_DSN'),
            user=os.getenv('FURNACE_ORACLE_DB_USER'),
            password=os.getenv('FURNACE_ORACLE_DB_PASSWORD'),
            encoding='UTF-8'
        )

#################################################################################################################################################

def gusaapp():
    # Connect to Server
    conn = connect.furnace()
    # Execute Query
    data = helpers.execute(conn, open(gusaapp_sql).read())
    # Return Data
    return data[0]

#################################################################################################################################################
