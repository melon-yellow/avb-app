
#################################################################################################################################################

# Imports
from os import getenv, path
from pyodbc import connect

# Modules
from .helpers import execute

#################################################################################################################################################

# Get File-Paths
fileDir = path.dirname(path.abspath(__file__))
equip_sql = path.abspath(path.join(fileDir, '../sql/sap.equip.sql'))
first_sql = path.abspath(path.join(fileDir, '../sql/sap.first.sql'))

##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################

class db:

    def sap():
        return connect(
            driver='ODBC Driver 17 for SQL Server',
            server=getenv('SAP_PM_MSSQL_DSN'),
            uid=getenv('SAP_PM_MSSQL_USER'),
            pwd=getenv('SAP_PM_MSSQL_PASSWORD'),
            database='ECP'
        )


##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################

def preditivas(equip: list[str]):
    # Check Input
    if not isinstance(equip, list):
        raise Exception('invalid argument "equip"')
    if not all(isinstance(i, str) for i in equip):
        raise Exception('invalid argument "equip"')
    # Connect to Server
    conn = db.sap()
    # Get Where Clause
    where = ' OR '.join(
        list(map(lambda e: f'("Equipamento" = {e})', equip))
    )
    # Execute Query
    query = open(equip_sql).read().format(where)
    data = execute(conn, query)
    # Get First Date
    queryf = open(first_sql).read().format(where)
    first = execute(conn, queryf)
    # Return Data
    return { 'data': data, 'first': first }

##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################

