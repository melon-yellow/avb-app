
#################################################################################################################################################

# Imports
import os
import cx_Oracle

#################################################################################################################################################

fileDir = os.path.dirname(os.path.abspath(__file__))
gusaapp_sql = os.path.abspath(os.path.join(fileDir, './sql/furnace.gusaapp.sql'))

#################################################################################################################################################

def gusaapp():
    data = None
    try: # Connect to Server
        conn = cx_Oracle.connect(
            dsn=os.getenv('FURNACE_ORACLE_DB_DSN'),
            user=os.getenv('FURNACE_ORACLE_DB_USER'),
            password=os.getenv('FURNACE_ORACLE_DB_PASSWORD'),
            encoding='UTF-8'
        )
        # Execute Query
        cur = conn.cursor()
        cur.execute(open(gusaapp_sql).read())
        dls = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
        cur.connection.close()
        # Assign Data
        data = dls[0] if len(dls) > 0 else {}
    except: pass
    return data

#################################################################################################################################################
