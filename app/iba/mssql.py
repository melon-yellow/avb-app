
#################################################################################################################################################

# Imports
import os
import pyodbc

#################################################################################################################################################

# Get File-Paths
fileDir = os.path.dirname(os.path.abspath(__file__))
product_sql = os.path.abspath(os.path.join(fileDir, '../sql/iba.mssql.product.sql'))
rfa_lim_sql = os.path.abspath(os.path.join(fileDir, '../sql/iba.mssql.rfa.lim.sql'))
rfa_sql = os.path.abspath(os.path.join(fileDir, '../sql/iba.mssql.rfa.sql'))

#################################################################################################################################################

def product():
    # Connect to Server
    conn = pyodbc.connect(
        dsn=os.getenv('IBA_MSSQL_DB_DSN'),
        uid=os.getenv('IBA_MSSQL_DB_USER'),
        pwd=os.getenv('IBA_MSSQL_DB_PASSWORD')
    )
    # Execute Query
    cur = conn.cursor()
    cur.execute(open(product_sql).read())
    # Parse to Dictionary
    r = [dict((cur.description[i][0], value)
        for i, value in enumerate(row)) for row in cur.fetchall()]
    r = r[0] if len(r) > 0 else {}
    # Close Connection
    cur.connection.close()
    # Fix Product Name
    pname = r.get('CTR_PRODUCT_NAME')
    pname = pname.strip() if isinstance(pname, str) else None
    if pname != None: r['CTR_PRODUCT_NAME'] = pname
    # Return Data
    return r

#################################################################################################################################################

def rfa():
    # Connect to Server
    conn = pyodbc.connect(
        dsn=os.getenv('IBA_MSSQL_DB_DSN'),
        uid=os.getenv('IBA_MSSQL_DB_USER'),
        pwd=os.getenv('IBA_MSSQL_DB_PASSWORD')
    )
    # Execute Query
    cur = conn.cursor()
    cur.execute(open(rfa_sql).read())
    # Parse to Dictionary
    r = [dict((cur.description[i][0], value)
        for i, value in enumerate(row)) for row in cur.fetchall()]
    r = r[0] if len(r) > 0 else {}
    # Close Connection
    cur.connection.close()
    # Fix Product Name
    pname = r.get('CTR_PRODUCT_NAME')
    pname = pname.strip() if isinstance(pname, str) else None
    if pname != None: r['CTR_PRODUCT_NAME'] = pname
    # Return Data
    return r

#################################################################################################################################################

def rfaLim():
    # Get Product Name
    produto = product().get('CTR_PRODUCT_NAME')
    # Connect to Server
    conn = pyodbc.connect(
        dsn=os.getenv('L2_SERVER_DB_DSN'),
        uid=os.getenv('L2_SERVER_DB_USER'),
        pwd=os.getenv('L2_SERVER_DB_PASSWORD')
    )
    # Execute Query
    cur = conn.cursor()
    cur.execute(open(rfa_lim_sql).read().format(produto))
    # Parse to Dictionary
    r = [dict((cur.description[i][0], value)
        for i, value in enumerate(row)) for row in cur.fetchall()]
    r = r[0] if len(r) > 0 else dict()
    # Close Connection
    cur.connection.close()
    # Return Data
    return r

#################################################################################################################################################
