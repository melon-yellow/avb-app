
#################################################################################################################################################

# Imports
import pyodbc

#################################################################################################################################################

def iba_mssql():
    r = None
    try:
        conn = pyodbc.connect('DSN=iba;UID=sa;PWD=avb2020')
        cur = conn.cursor()
        cur.execute(query_mssql)
        r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
        r = r[0] if len(r) > 0 else dict()
        pname = r.get('CTR_PRODUCT_NAME')
        pname = pname.strip() if isinstance(pname, str) else None
        if pname != None: r['CTR_PRODUCT_NAME'] = pname
        cur.connection.close()
    except: r = None
    return r

#################################################################################################################################################
