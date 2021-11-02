
#################################################################################################################################################

# Imports
import os
import cx_Oracle

#################################################################################################################################################

fileDir = os.path.dirname(os.path.abspath(__file__))
gusaapp_sql = os.path.abspath(os.path.join(fileDir, '../sql/furl2.oracle.gusaapp.sql'))

#################################################################################################################################################

def gusaapp():
    r = None
    try:
        conn = cx_Oracle.connect('gusaapp/gusaapp@10.20.6.66/orcl')
        cur = conn.cursor()
        cur.execute(open(gusaapp_sql).read())
        r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
        r = r[0] if len(r) > 0 else dict()
        cur.connection.close()
    except: r = None
    return r

#################################################################################################################################################
