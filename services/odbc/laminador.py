
#################################################################################################################################################

# Imports
import os
import pyodbc

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
            server=os.getenv('IBA_MSSQL_DB_DSN'),
            uid=os.getenv('IBA_MSSQL_DB_USER'),
            pwd=os.getenv('IBA_MSSQL_DB_PASSWORD')
        )

    def l2():
        return pyodbc.connect(
            driver='ODBC Driver 17 for SQL Server',
            server=os.getenv('L2_SERVER_DB_DSN'),
            uid=os.getenv('L2_SERVER_DB_USER'),
            pwd=os.getenv('L2_SERVER_DB_PASSWORD')
        )

#################################################################################################################################################

def exQuery(conn, query: str):
    # Execute Query
    cur = conn.cursor()
    cur.execute(query)
    # Parse to Dictionary
    data = [dict((cur.description[i][0], value)
        for i, value in enumerate(row)) for row in cur.fetchall()]
    data = data[0] if len(data) > 0 else {}
    # Return Data
    return data

##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################

def produto():
    # Connect to Server
    conn = connect.iba()
    # Execute Query
    data = exQuery(conn, open(product_sql).read())
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
    data = exQuery(conn, open(blbp_sql).read())
    # Return Data
    return data

#################################################################################################################################################

def rfa():
    # Connect to Server
    conn = connect.iba()
    # Execute Query
    data = exQuery(conn, open(rfa_sql).read())
    # Return Data
    return data

#################################################################################################################################################

def rfal2():
    # Get Product Name
    product = produto().get('CTR_PRODUCT_NAME')
    # Connect to Server
    conn = connect.l2()
    # Execute Query
    data = exQuery(conn, open(rfal2_sql).read().format(product))
    # Return Data
    return data

##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################
