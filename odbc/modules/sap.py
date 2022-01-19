
#################################################################################################################################################

# Imports
import os
import pyodbc

# Modules
from . import helpers

#################################################################################################################################################

# Get File-Paths
fileDir = os.path.dirname(os.path.abspath(__file__))
equip_sql = os.path.abspath(os.path.join(fileDir, '../sql/sap.equip.sql'))
first_sql = os.path.abspath(os.path.join(fileDir, '../sql/sap.first.sql'))

##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################

class connect:

    def sap():
        return pyodbc.connect(
            driver='ODBC Driver 17 for SQL Server',
            server=os.getenv('SAP_PM_MSSQL_DSN'),
            uid=os.getenv('SAP_PM_MSSQL_USER'),
            pwd=os.getenv('SAP_PM_MSSQL_PASSWORD'),
            database='ECP'
        )


##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################

def preditivas(equip: list[str]):
    if not isinstance(equip, list): raise Exception('invalid argument "equip"')
    if not all(isinstance(i, str) for i in equip): raise Exception('invalid argument "equip"')
    # Connect to Server
    conn = connect.sap()
    # Get Where Clause
    where = ' OR '.join(
        list(map(lambda e: f'("Equipamento" = {e})', equip))
    )
    # Execute Query
    query = open(equip_sql).read().format(where)
    data = helpers.execute(conn, query)
    # Get First Date
    queryf = open(first_sql).read().format(where)
    first = helpers.execute(conn, queryf)
    # Return Data
    return { 'data': data, 'first': first }

##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################

