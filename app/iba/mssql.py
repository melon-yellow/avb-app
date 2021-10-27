
#################################################################################################################################################

# Imports
import os
import pyodbc

#################################################################################################################################################

# Get File-Paths
fileDir = os.path.dirname(__file__)
product_sql = os.path.join(fileDir, '..\\sql\\iba.mssql.product.sql')
rfa_lim_sql = os.path.join(fileDir, '..\\sql\\iba.mssql.rfa.lim.sql')
rfa_sql = os.path.join(fileDir, '..\\sql\\iba.mssql.rfa.sql')

#################################################################################################################################################

def product():
    r = None
    try:
        conn = pyodbc.connect('DSN=iba;UID=sa;PWD=avb2020')
        cur = conn.cursor()
        cur.execute(open(product_sql).read())
        r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
        r = r[0] if len(r) > 0 else {}
        pname = r.get('CTR_PRODUCT_NAME')
        pname = pname.strip() if isinstance(pname, str) else None
        if pname != None: r['CTR_PRODUCT_NAME'] = pname
        cur.connection.close()
    except: r = None
    return r

#################################################################################################################################################

def rfa():
    r = None
    try:
        conn = pyodbc.connect('DSN=iba;UID=sa;PWD=avb2020')
        cur = conn.cursor()
        cur.execute(open(rfa_sql).read())
        r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
        r = r[0] if len(r) > 0 else {}
        pname = r.get('CTR_PRODUCT_NAME')
        pname = pname.strip() if isinstance(pname, str) else None
        if pname != None: r['CTR_PRODUCT_NAME'] = pname
        cur.connection.close()
    except: r = None
    return r

#################################################################################################################################################

def rfaLim():
    produto = product().get('CTR_PRODUCT_NAME')
    conn = pyodbc.connect('DSN=L2_SERVER;UID=sa;PWD=avb2020')
    cur = conn.cursor()
    cur.execute(open(rfa_lim_sql).read().format(produto))
    r = [dict((cur.description[i][0], value)
        for i, value in enumerate(row)) for row in cur.fetchall()]
    r = r[0] if len(r) > 0 else dict()
    cur.connection.close()
    return r

#################################################################################################################################################
