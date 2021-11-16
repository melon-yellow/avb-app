
#################################################################################################################################################

# Imports
import os
import pyodbc

# Modules
from . import helpers

#################################################################################################################################################

# Get File-Paths
fileDir = os.path.dirname(os.path.abspath(__file__))
blbp_sql = os.path.abspath(os.path.join(fileDir, './sql/mill.blbp.sql'))
product_sql = os.path.abspath(os.path.join(fileDir, './sql/mill.product.sql'))
rfal2_sql = os.path.abspath(os.path.join(fileDir, './sql/mill.rfal2.sql'))
rfa_sql = os.path.abspath(os.path.join(fileDir, './sql/mill.rfa.sql'))

##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################

class connect:

    def iba():
        return pyodbc.connect(
            driver='ODBC Driver 17 for SQL Server',
            server=os.getenv('IBA_MSSQL_DSN'),
            uid=os.getenv('IBA_MSSQL_USER'),
            pwd=os.getenv('IBA_MSSQL_PASSWORD')
        )

    def l2():
        return pyodbc.connect(
            driver='ODBC Driver 17 for SQL Server',
            server=os.getenv('L2_MSSQL_DSN'),
            uid=os.getenv('L2_MSSQL_USER'),
            pwd=os.getenv('L2_MSSQL_PASSWORD')
        )

##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################

def produto():
    # Connect to Server
    conn = connect.iba()
    # Execute Query
    data = helpers.execute(conn, open(product_sql).read())
    # Fix Product Name
    pname = data.get('CTR_PRODUCT_NAME')
    pname = pname.strip() if isinstance(pname, str) else None
    data['CTR_PRODUCT_NAME'] = pname
    # Return Data
    return data

#################################################################################################################################################

def blbp():
    # Connect to Server
    conn = connect.iba()
    # Execute Query
    data = helpers.execute(conn, open(blbp_sql).read())
    # Return Data
    return data

#################################################################################################################################################

def rfa():
    # Connect to Server
    conn = connect.iba()
    # Execute Query
    data = helpers.execute(conn, open(rfa_sql).read())
    # Return Data
    return data

#################################################################################################################################################

def rfal2():
    # Get Product Name
    product = produto().get('CTR_PRODUCT_NAME')
    # Connect to Server
    conn = connect.l2()
    # Execute Query
    query = open(rfal2_sql).read().format(product)
    data = helpers.execute(conn, query)
    # Return Data
    return data

##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################
