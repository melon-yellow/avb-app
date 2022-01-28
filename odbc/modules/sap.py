
#################################################################################################################################################

# Imports
from os import getenv, path
from pyodbc import connect
from asyncio import gather

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

async def read_from_sap(conn, path: str, where: str):
    try:
        query = open(path).read().format(where)
        data = execute(conn, query)
        # Return Data
        return (True, data)
    except Exception as error:
        return (False, error)

##########################################################################################################################

async def preditivas(equip: list[str]):
    try:
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
        (
            (ok1, equips),
            (ok2, first)
        ) = await gather(
            read_from_sap(conn, equip_sql, where),
            read_from_sap(conn, first_sql, where)
        )
        # Check Results
        if not ok1: raise equips
        if not ok2: raise first
        # Return Data
        data = {'data': equips, 'first': first}
        # Return Data
        return (True, data)
    except Exception as error:
        return (False, error)

##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################

