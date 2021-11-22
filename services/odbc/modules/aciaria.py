
#################################################################################################################################################

# Imports
import os
import pyodbc

# Modules
from . import helpers

#################################################################################################################################################

# Get File-Paths
fileDir = os.path.dirname(os.path.abspath(__file__))
spec_sql = os.path.abspath(os.path.join(fileDir, '../sql/aciaria.spec.sql'))

##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################

class connect:

    def ld():
        return pyodbc.connect(
            driver='ODBC Driver 17 for SQL Server',
            server=os.getenv('SPEC_LD_MSSQL_DSN'),
            uid=os.getenv('SPEC_LD_MSSQL_USER'),
            pwd=os.getenv('SPEC_LD_MSSQL_PASSWORD'),
            database='ANALYSES'
        )

    def fp():
        return pyodbc.connect(
            driver='ODBC Driver 17 for SQL Server',
            server=os.getenv('SPEC_FP_MSSQL_DSN'),
            uid=os.getenv('SPEC_FP_MSSQL_USER'),
            pwd=os.getenv('SPEC_FP_MSSQL_PASSWORD'),
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
        conn = connect.ld()
        # Execute Query
        data = helpers.execute(conn, query.ld())
        # Return Data
        return data

#################################################################################################################################################

class fp:

    def espectrometro():
        # Connect to Server
        conn = connect.fp()
        # Execute Query
        data = helpers.execute(conn, query.fp())
        # Return Data
        return data

##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################

