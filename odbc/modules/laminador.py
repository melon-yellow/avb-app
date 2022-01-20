
#################################################################################################################################################

# Imports
from os import getenv, path
from pyodbc import connect

# Modules
from .helpers import execute

#################################################################################################################################################

# Get File-Paths
fileDir = path.dirname(path.abspath(__file__))
blbp_sql = path.abspath(path.join(fileDir, '../sql/mill.blbp.sql'))
product_sql = path.abspath(path.join(fileDir, '../sql/mill.product.sql'))
rfal2_sql = path.abspath(path.join(fileDir, '../sql/mill.rfal2.sql'))
rfa_sql = path.abspath(path.join(fileDir, '../sql/mill.rfa.sql'))

##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################

class db:

    def iba():
        return connect(
            driver='ODBC Driver 17 for SQL Server',
            server=getenv('IBA_MSSQL_DSN'),
            uid=getenv('IBA_MSSQL_USER'),
            pwd=getenv('IBA_MSSQL_PASSWORD')
        )

    def l2():
        return connect(
            driver='ODBC Driver 17 for SQL Server',
            server=getenv('L2_MSSQL_DSN'),
            uid=getenv('L2_MSSQL_USER'),
            pwd=getenv('L2_MSSQL_PASSWORD')
        )

##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################

def produto():
    # Connect to Server
    conn = db.iba()
    # Execute Query
    data = execute(conn, open(product_sql).read())
    # Fix Product Name
    pname = data[0].get('CTR_PRODUCT_NAME')
    pname = pname.strip() if isinstance(pname, str) else None
    data[0]['CTR_PRODUCT_NAME'] = pname
    # Return Data
    return data[0]

#################################################################################################################################################

def blbp():
    # Connect to Server
    conn = db.iba()
    # Execute Query
    data = execute(conn, open(blbp_sql).read())
    # Return Data
    return data[0]

#################################################################################################################################################

def rfa():
    # Connect to Server
    conn = db.iba()
    # Execute Query
    data = execute(conn, open(rfa_sql).read())
    # Return Data
    return data[0]

#################################################################################################################################################

def rfal2():
    # Get Product Name
    product = produto().get('CTR_PRODUCT_NAME')
    # Connect to Server
    conn = db.l2()
    # Execute Query
    query = open(rfal2_sql).read().format(product)
    data = execute(conn, query)
    # Return Data
    return data[0]

##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################
