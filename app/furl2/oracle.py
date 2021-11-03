
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
        conn = cx_Oracle.connect(
            dsn=os.getenv('ORACLE_DB_FURNACE_DSN'),
            user=os.getenv('ORACLE_DB_FURNACE_USER'),
            password=os.getenv('ORACLE_DB_FURNACE_PASSWORD'),
            encoding='UTF-8'
        )
        cur = conn.cursor()
        cur.execute(open(gusaapp_sql).read())
        r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
        r = r[0] if len(r) > 0 else dict()
        cur.connection.close()
    except: pass
    return r

#################################################################################################################################################
