
#################################################################################################################################################

# Imports
import cx_Oracle

#################################################################################################################################################

def gusaapp():
    r = None
    try:
        sql = open('sql/furl2.oracle.gusaapp.sql').read()
        con = cx_Oracle.connect('gusaapp/gusaapp@10.20.6.66/orcl')
        cur = con.cursor()
        cur.execute(sql)
        r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
        r = r[0] if len(r) > 0 else dict()
        cur.connection.close()
    except: r = None
    return r

#################################################################################################################################################
