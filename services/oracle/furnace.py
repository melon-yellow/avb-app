
#################################################################################################################################################

# Imports
import os
import cx_Oracle

#################################################################################################################################################

fileDir = os.path.dirname(os.path.abspath(__file__))
gusaapp_sql = os.path.abspath(os.path.join(fileDir, './sql/furnace.gusaapp.sql'))

##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################

class connect:

    def furnace():
        return cx_Oracle.connect(
            dsn=os.getenv('FURNACE_ORACLE_DB_DSN'),
            user=os.getenv('FURNACE_ORACLE_DB_USER'),
            password=os.getenv('FURNACE_ORACLE_DB_PASSWORD'),
            encoding='UTF-8'
        )

#################################################################################################################################################

def exQuery(conn, query: str):
    # Execute Query
    cur = conn.cursor()
    cur.execute(query)
    # Parse to Dictionary
    data = [dict((cur.description[i][0], value)
        for i, value in enumerate(row)) for row in cur.fetchall()]
    data = data[0] if len(data) > 0 else {}
    # Return Data
    return data

#################################################################################################################################################

def gusaapp():
    try: # Connect to Server
        conn = connect.furnace()
        # Execute Query
        data = exQuery(conn, open(gusaapp_sql).read())
        # Return Data
        return data
    except: return {}

#################################################################################################################################################
