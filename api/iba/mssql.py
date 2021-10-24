
#################################################################################################################################################

# Imports
import pyodbc

#################################################################################################################################################

def product():
    r = None
    try:
        sql = open('sql/iba.mssql.product.sql').read()
        conn = pyodbc.connect('DSN=iba;UID=sa;PWD=avb2020')
        cur = conn.cursor()
        cur.execute(sql)
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
        sql = open('sql/iba.mssql.rfa.sql').read()
        conn = pyodbc.connect('DSN=iba;UID=sa;PWD=avb2020')
        cur = conn.cursor()
        cur.execute(sql)
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
    sql = open('sql/iba.mssql.rfaLim.sql').read().format(produto)
    conn = pyodbc.connect('DSN=L2_SERVER;UID=sa;PWD=avb2020')
    cur = conn.cursor()
    cur.execute(sql)
    r = [dict((cur.description[i][0], value)
        for i, value in enumerate(row)) for row in cur.fetchall()]
    r = r[0] if len(r) > 0 else dict()
    cur.connection.close()
    return r

#################################################################################################################################################
