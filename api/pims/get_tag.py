
#################################################################################################################################################

# Imports
import pyodbc

#################################################################################################################################################

# old function
def py_get_pims(req, res):
    # Check for input Variable
    if ('tagname' not in req or
        not isinstance(req['tagname'], str)
        ): return dict(error='tagname missing')

    # Get Query String
    string = open('sql/pims_get_tag.sql').read()
    string = string.format(req['tagname'])

    # Connnect to pims SQL Plus server
    conn = pyodbc.connect('DSN=IP21;UID=Administrator;PWD=gnsa2011*')
    cursor = conn.cursor()

    # Execute query
    cursor.execute(string)
    res = [dict((cursor.description[i][0], value) \
        for i, value in enumerate(row)) for row in cursor.fetchall()]
    cursor.connection.close()

    # check length of result
    if len(res) > 0: res = res[0]
    else: res = dict(error='not found')

    # Return data
    return res

#################################################################################################################################################