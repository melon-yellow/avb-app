
#################################################################################################################################################

def execute(conn, query: str):
    # Execute Query
    cur = conn.cursor()
    cur.execute(query)
    # Parse to Dictionary
    data = [dict((cur.description[i][0], value)
        for i, value in enumerate(row)) for row in cur.fetchall()]
    # Return Data
    return data

#################################################################################################################################################
