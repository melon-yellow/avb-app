
#################################################################################################################################################

# Imports
from os import getenv, path
from pyodbc import connect

# Modules
from .helpers import execute

#################################################################################################################################################

# Get File-Paths
fileDir = path.dirname(path.abspath(__file__))
spec_sql = path.abspath(path.join(fileDir, '../sql/aciaria.spec.sql'))

##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################

class db:

    def ld():
        return connect(
            driver='ODBC Driver 17 for SQL Server',
            server=getenv('SPEC_LD_MSSQL_DSN'),
            uid=getenv('SPEC_LD_MSSQL_USER'),
            pwd=getenv('SPEC_LD_MSSQL_PASSWORD'),
            database='ANALYSES'
        )

    def fp():
        return connect(
            driver='ODBC Driver 17 for SQL Server',
            server=getenv('SPEC_FP_MSSQL_DSN'),
            uid=getenv('SPEC_FP_MSSQL_USER'),
            pwd=getenv('SPEC_FP_MSSQL_PASSWORD'),
            database='ANALYSES'
        )

#################################################################################################################################################

class query:

    def raw():
        return open(spec_sql).read()

    def fp():
        return query.raw().format('', '16', '')

    def ld():
        return query.raw().format(
            'corrida_gusa.value as \'Corrida Gusa\',',
            '17',
            '{} {} {}'.format(
                'LEFT JOIN Attributes corrida_gusa (nolock) ON',
                'corrida_gusa.LinkAnalyses = Elements.LinkAnalyses and',
                'corrida_gusa.LinkName = 21'
            )
        )

##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################

class ld:

    def espectrometro():
        # Connect to Server
        conn = db.ld()
        # Execute Query
        data = execute(conn, query.ld())
        # Return Data
        return data

#################################################################################################################################################

class fp:

    def espectrometro():
        # Connect to Server
        conn = db.fp()
        # Execute Query
        data = execute(conn, query.fp())
        # Return Data
        return data

##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################

