
#################################################################################################################################################

# Imports
import py_misc
import cx_Oracle

#################################################################################################################################################

fileDir = py_misc.__schema__()
gusaapp_sql = py_misc.os.path.join(fileDir, '..\\sql\\furl2.oracle.gusaapp.sql')

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
