
#################################################################################################################################################

# Imports
import os
import pyodbc

#################################################################################################################################################

# Get File-Paths
fileDir = os.path.dirname(__file__)
product_sql = os.path.join(fileDir, '..\\sql\\iba.mssql.product.sql')
rfa_lim_sql = os.path.join(fileDir, '..\\sql\\iba.mssql.rfa.lim.sql')
rfa_sql = os.path.join(fileDir, '..\\sql\\iba.mssql.rfa.sql')

#################################################################################################################################################

    @api.route('/api/util_csv/')
    def trf_util_csv(req: Request, res: Response):
        # MySQL Connection
        mydb = mysql.connector.connect(
            host='127.0.0.1',
            user='Jayron',
            passwd='123456',
            port='3306',
            database='iba_i'
        )
        sql = open('../sql/trefila.util.sql').read()
        df = pandas.read_sql(sql, mydb)
        mydb.close()
        # Processing
        meses = {'1':[1,2,3],'2':[4,5,6],'3':[7,8,9],'4':[10,11,12]}
        df['_0h'] = df._date.apply(lambda row : turno.escala.get(dia = row)[0][0])
        df['_8h'] = df._date.apply(lambda row : turno.escala.get(dia = row)[1][0])
        df['_16h'] = df._date.apply(lambda row : turno.escala.get(dia = row)[2][0])
        df['_date'] = df['_date'].astype('str')
        dz = df
        hoje = py_misc.datetime.date.today()
        #hoje = datetime.datetime.now()
        #hoje = datetime.date(2021,2,23)
        Trimestre = str((hoje.month-1)//3+1)
        Tmeses = meses.get(Trimestre)
        #mes = datetime.date(2021,3,23).month
        bn = df[df['_date'] >= py_misc.datetime.date(hoje.year, Tmeses[0], 1).strftime("%Y-%m-%d")]
        bn = bn[bn['_date'] <= hoje.strftime("%Y-%m-%d")]
        bn = bn.filter(['_date','M1','M2','M3','M4','M5','_0h','_8h','_16h'])
        bn = bn.drop(['M1'], axis=1)
        bn['Global'] = (bn['M2']+bn['M3']+bn['M4']+bn['M5']) / 4
        # Retrun Data
        return res(
            bn.to_csv(),
            mimetype = "text/csv",
            headers = {
                "Content-disposition": "attachment; filename=utilizacao.csv"
            }
        )

    #################################################################################################################################################

    @api.route('/api/util_csv_dia')
    def trf_util_csv_dia(req: Request, res: Response):
        # MySQL Connection
        mydb = mysql.connector.connect(
            host='127.0.0.1',
            user='Jayron',
            passwd='123456',
            port='3306',
            database='iba_i'
        )
        sql = open('sql/trf_util_day.sql').read()
        csv = pandas.read_sql(sql, mydb).to_csv()
        mydb.close()
        # Return Data
        return res(
            csv,
            mimetype = "text/csv",
            headers = {
                "Content-disposition": "attachment; filename=utilizacao-dia.csv"
            }
        )
