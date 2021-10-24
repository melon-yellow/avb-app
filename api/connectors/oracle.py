
#################################################################################################################################################

# Imports
import cx_Oracle

#################################################################################################################################################

def gusaapp():
    r = None
    try:
        con = cx_Oracle.connect('gusaapp/gusaapp@10.20.6.66/orcl')
        cur = con.cursor()
        cur.execute(query_orcl)
        r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
        r = r[0] if len(r) > 0 else dict()
        cur.connection.close()
    except: r = None
    return r

#################################################################################################################################################
