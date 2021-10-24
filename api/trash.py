meses = {'1':[1,2,3],'2':[4,5,6],'3':[7,8,9],'4':[10,11,12]}
mes_nome = {
    1:'Jan', 2:'Fev', 3:'Mar', 4:'Abr',
    5:'Mai', 6:'Jun', 7:'Jul', 8:'Ago',
    9:'Set',10:'Out',11:'Nov',12:'Dez'
}

def last_day_of_month(date):
    if date.month == 12:
        return date.replace(day=31)
    return date.replace(month=date.month+1, day=1) - datetime.timedelta(days=1)


def extrai_data(date):

    datas = []
    date = date.replace('-','/')
    date = date.split()
    for dat in date:
        try:
            if re.search('^([0-9]|0[0-9]|1[0-9]|2[0-9]|3[0-1])(.|-)([0-9]|0[0-9]|1[0-2])(.|-|)20[0-9][0-9]$',dat):
                date_time_obj = datetime.datetime.strptime(dat, '%d/%m/%Y')
                datas.append(date_time_obj)
                datas.sort()

            elif re.search('^([0-9]|0[0-9]|1[0-9]|2[0-9]|3[0-1])(.|-)([0-9]|0[0-9]|1[0-2])(.|-|)[0-9][0-9]$',dat):
                date_time_obj = datetime.datetime.strptime(dat, '%d/%m/%y')
                datas.append(date_time_obj)
                datas.sort()


            elif re.search('^([0-9]|0[0-9]|1[0-9]|2[0-9]|3[0-1])(.|-)([0-9]|0[0-9]|1[0-2])$',dat):
                dat = dat + '/' +datetime.datetime.strftime(datetime.datetime.today(),'%y')
                date_time_obj = datetime.datetime.strptime(dat, '%d/%m/%y')
                datas.append(date_time_obj)

        except:
            pass
    if(len(datas)<2):
        datas.append(datas[0])
    return(datas)

def analisa(frase):
    try:
        saida = dict()
        user = frase.get('question')
        msg = clas.classifique(user)

        # producao
        if ('produção' in msg.keys()):
            #tem intervalo?
            if('ontem' in msg.keys() and msg['ontem']>1):
                d = datetime.datetime.now()- datetime.timedelta(days = 1)
                d = datetime.datetime.strftime(d, '%d/%m/%Y')
                d = '{} {}'.format(d,d)
                if(re.findall(r'(\d+\.\d+|\d+\,\d+)', user) and 'produto' in msg.keys()):
                    param = re.findall(r'(\d+\.\d+|\d+\,\d+)', user)
                    return busca_dados(d,param)
                else:
                    return busca_dados(d,'32')

            elif ('hoje' in msg.keys() and msg['hoje']>1):
                d = datetime.datetime.now()
                d = datetime.datetime.strftime(d, '%d/%m/%Y')
                d = '{} {}'.format(d,d)
                if(re.findall(r'(\d+\.\d+|\d+\,\d+)', user) and 'produto' in msg.keys()):
                    param = re.findall(r'(\d+\.\d+|\d+\,\d+)', user)
                    return busca_dados(d,param)
                else:
                    return busca_dados(d,'32')

            elif (extrai_data(user)):
                if(re.findall(r'(\d+\.\d+|\d+\,\d+)', user) and 'produto' in msg.keys()):
                    param = re.findall(r'(\d+\.\d+|\d+\,\d+)', user)
                    return busca_dados(user,param)
                else:
                    return busca_dados(user,'32')

            else:
                d = datetime.datetime.now()
                d = datetime.datetime.strftime(d, '%d/%m/%Y')
                d = '{} {}'.format(d,d)
                if(re.findall(r'(\d+\.\d+|\d+\,\d+)', user) and 'produto' in msg.keys()):
                    param = re.findall(r'(\d+\.\d+|\d+\,\d+)', user)
                    return busca_dados(d,param)
                else:
                    return busca_dados(d,'32')

        # qualidade
        if ('qualidade' in msg.keys()):
            #tem intervalo?
            if('ontem' in msg.keys()):
                if('média' in msg.keys()):
                    #chama calculo
                    pass
                elif('soma' in msg.keys()):
                    #chama calculo
                    pass
                else:
                    #chama calculo padrao
                    pass
            elif ('hoje' in msg.keys()):
                if('média' in msg.keys()):
                    #chama calculo
                    pass
                elif ('soma' in msg.keys()):
                    #chama calculo
                    pass
                else:
                    #chama calculo padrao
                    pass
            elif (extrai_data(user)):

                if('média' in msg.keys()):
                    #chama calculo
                    pass
                elif ('soma' in msg.keys()):
                    #chama calculo
                    pass
                else:
                    #chama calculo padrao
                    pass
        else:
            saida['answer'] = 'Sinceramente não entendi o que você falou ðﾟﾤﾔ!'
            return saida
    except:
        saida['answer'] = 'Ocorreu um erro enquanto eu fazia a consulta!'
        return saida

def busca_dados(raw_intervalo, parametro):

    try:
        if(len(parametro)>1):
            parametro = parametro.replace(',','.')
        else:
            parametro = parametro[0].replace(',','.')

        saida = dict()
        e = []
        datas = extrai_data(raw_intervalo)

        delta = datas[1] - datas[0]

        if(delta !=0):
            delta = delta.days
        else:
            delta =1

        for d in datas:
            e.append(datetime.datetime.strftime(d, '%d/%m/%Y'))
        datas = e

    #if(1):
        homerico_csv = homerico.RelatorioLista(datas[0], datas[1], '32')
        csv_file = StringIO(homerico_csv)
        df = pd.read_csv(csv_file, sep=';',dtype='object')

        df['size'] = df['Produto'].str.findall(r'\d+(?:,\d+)?').str[-1]
        df['size'] = df['size'].str.replace(',','.')
        df['size'] = df['size'].apply(pd.to_numeric,errors='coerce')
        df['Peso do Produto'] = df['Peso do Produto'].apply(pd.to_numeric,errors='coerce')
        #df = df.drop_duplicates(subset = ['size'])
        if(parametro !='32'):
            df = df[df['size'] == float(parametro)]

        df = df.filter(['DATA','Produto','Peso do Produto'])
        df.sort_values(by='DATA', inplace=True)
        x = df['Peso do Produto'].mean()
        z = df['Peso do Produto'].sum().round()/1000
        df['Total'] = x

        df = df.groupby(['Produto']).sum()/1000
        df = df.round(1)
        #df.reset_index(inplace=True)
        #df.reset_index(drop=True,inplace=True)
        if not(df.empty):
            df = df.filter(['Produto','Peso do Produto']).to_string()
            df = df.split('\n',1)[1]
            if (delta >1 and parametro =='32' ):
                saida['answer'] = (df + '\n\nMédia dos ({})dias : *{} tons/dia*'.format(delta,(z/delta).round(1)) +
                    '\n\nTotal Geral produzido no período: *{} toneladas*\n'.format((z).round(1)) + '')
            else: saida['answer'] = df + '\n\nTotal Geral produzido: {} toneladas\n'.format(z.round(1))
        else: saida['answer'] = 'Não encontrei nada com esse critério'
    except: saida['answer'] = 'Ocorreu um erro enquanto eu fazia a consulta!'
    return saida

def get_trim(cod):
    now = datetime.datetime.now()
    qt = str((now.month-1)//3+1)
    m = meses.get(qt)
    me = datetime.date.today()
    mon = list()
    mes = me.month
    for i in m:
        if i > mes: mon.append(None)
        elif i == mes:
            try:
                data = datetime.date(me.year,i,me.day).strftime('%d/%m/%Y')
                homerico_csv = homerico.RelatorioGerencialRegistro(data, cod)
                csv_file = StringIO(homerico_csv)
                df = pd.read_csv(csv_file, sep=';')
                mon.append(df['acumulado'].values[0])
            except: mon.append(None)
        else:
            try:
                data = datetime.date(me.year,i,last_day_of_month(datetime.date(me.year,i,1)).day).strftime('%d/%m/%Y')
                homerico_csv = homerico.RelatorioGerencialRegistro(data, cod)
                csv_file = StringIO(homerico_csv)
                df = pd.read_csv(csv_file, sep=';')
                mon.append(df['acumulado'].values[0])
            except: mon.append(None)
    lista = list()
    for i in m: lista.append(mes_nome[i])
    meta_json['meses'] = lista
    return(mon)

def get_meta_util_trf():
    try:
        mydb12 = mysql.connector.connect(host='192.168.61.1', user='Jayron', passwd='123456', port='3306', database='iba_i')
        query = open('sql/trf_util_shift.sql').read()
        df = pd.read_sql(query, mydb12)

        try: mydb12.close()
        except: pass

    except: return

    df['_0h'] = df._date.apply(lambda row : getEscala(dia = row)[0][0])
    df['_8h'] = df._date.apply(lambda row : getEscala(dia = row)[1][0])
    df['_16h'] = df._date.apply(lambda row : getEscala(dia = row)[2][0])
    df['_date'] = df['_date'].astype('str')
    dz = df
    hoje = datetime.date.today()
    Trimestre = str((hoje.month-1)//3+1)
    Tmeses = meses.get(Trimestre)
    mon = list()
    mes = hoje.month

    bn = df[df['_date']>=datetime.date(hoje.year,Tmeses[0],1).strftime('%Y-%m-%d')]
    bn = bn[bn['_date']<=datetime.date(hoje.year,hoje.month,hoje.day).strftime('%Y-%m-%d')]
    bn = bn.filter(['_date', 'M1','M2','M3', 'M4', 'M5', '_0h', '_8h','_16h'])
    bn = bn.drop(['M1'], axis=1)
    bn = bn.mean()
    bn = bn.mean()
    for m in Tmeses:
        if m > mes: mon.append(None)
        elif m == mes:
            try:
                dz = df[df['_date']>=datetime.date(hoje.year,hoje.month,1).strftime('%Y-%m-%d')]
                dz = dz[dz['_date']<=datetime.date(hoje.year,hoje.month,hoje.day).strftime('%Y-%m-%d')]
                dz = dz.filter(['_date', 'M1','M2','M3', 'M4', 'M5', '_0h', '_8h','_16h'])
                dz = dz.drop(['M1'], axis=1)
                dz = dz.mean()
                dz = dz.mean()
                mon.append(dz)
            except: mon.append(None)
        else:
            try:
                dz = df[df['_date']>=datetime.date(hoje.year,m,1).strftime('%Y-%m-%d')]
                dz = dz[dz['_date']<=datetime.date(hoje.year,m,last_day_of_month(datetime.date(hoje.year,m,1)).day).strftime('%Y-%m-%d')]
                dz = dz.filter(['_date', 'M1','M2','M3', 'M4', 'M5', '_0h', '_8h','_16h'])
                dz = dz.drop(['M1'], axis=1)
                dz = dz.mean()
                dz = dz.mean()
                mon.append(dz)
            except: mon.append(None)
    util_json = {}

    util_json['utilizacao'] = { 'meta': 0.0, 'dia': 0.0, 'acumulado': 0, 'mes1': 0.0, 'mes2': 0, 'mes3': 0 }
    util_json['utilizacao']['meta'] = 60.0
    util_json['utilizacao']['dia'] = 0.0
    util_json['utilizacao']['mes1'] = mon[0]
    util_json['utilizacao']['mes2'] = mon[1]
    util_json['utilizacao']['mes3'] = mon[2]
    util_json['utilizacao']['acumulado'] = bn

    return(util_json)

def get_meta_custo_trf():
    try:
        dbCusto = mysql.connector.connect(host='192.168.61.1', user='jayron', passwd='123123', port='1517', database='lam')
        queryC = 'SELECT * FROM wf_sap WHERE YEAR(data_msg)=2021;'
        dfC = pd.read_sql(queryC, dbCusto)
    except:
        try: dbCusto.close()
        except: pass
        print('Erro na conexão sql')
        return

    hoje = datetime.date.today()
    #hoje = datetime.datetime.now()
    #hoje = datetime.date(2021,2,23)
    Trimestre = str((hoje.month-1)//3+1)
    Tmeses = meses.get(Trimestre)
    mon = list()
    mes = hoje.month
    #mes = datetime.date(2021,3,23).month
    dz = dfC

    #trimestre
    bn = dfC[dfC['DATA_MSG']>=datetime.date(hoje.year,Tmeses[0],1).strftime('%Y-%m-%d')]
    bn = bn[bn['DATA_MSG']<=datetime.date(hoje.year,hoje.month,hoje.day).strftime('%Y-%m-%d')]
    bn = bn['VALOR'].sum()
    ###########

    #dia
    bm = dfC[dfC['DATA_MSG']>=datetime.date(hoje.year,hoje.month,hoje.day).strftime('%Y-%m-%d')]
    bm = bm['VALOR'].sum()
    ###########

    for m in Tmeses:
        if m > mes: mon.append(None)
        elif m == mes:
            try:
                dz = dfC[dfC['DATA_MSG']>=datetime.date(hoje.year,hoje.month,1).strftime('%Y-%m-%d')]
                dz = dz[dz['DATA_MSG']<=datetime.date(hoje.year,hoje.month,hoje.day).strftime('%Y-%m-%d')]
                dz = dz['VALOR'].sum()
                mon.append(dz)
            except: mon.append(None)
        else:
            try:
                dz = dfC[dfC['DATA_MSG']>=datetime.date(hoje.year,m,1).strftime('%Y-%m-%d')]
                dz = dz[dz['DATA_MSG']<=datetime.date(hoje.year,m,last_day_of_month(datetime.date(hoje.year,m,1)).day).strftime('%Y-%m-%d')]
                dz = dz['VALOR'].sum()
                mon.append(dz)
            except: mon.append(None)

    custo_json = {}
    custo_json['custo'] = { 'meta': 0.0, 'dia': 0.0, 'acumulado': 0, 'mes1': 0.0, 'mes2': 0, 'mes3': 0 }
    custo_json['custo']['meta'] = 110.0
    custo_json['custo']['dia'] = bm
    custo_json['custo']['mes1'] = mon[0]
    custo_json['custo']['mes2'] = mon[1]
    custo_json['custo']['mes3'] = mon[2]
    custo_json['custo']['acumulado'] = bn

    return(custo_json)

def get_meta_5S_trf():
    try:
        db5S = mysql.connector.connect(host='192.168.61.1', user='jayron', passwd='123123', port='1517', database='lam')
        query5S = 'SELECT * FROM metas WHERE YEAR(data_msg)=2021 and nome_meta = "5S";'
        dfC = pd.read_sql(query5S, db5S)
    except:
        try: db5S.close()
        except: pass
        print('Erro na conexão sql')
        return

    hoje = datetime.date.today()
    #hoje = datetime.datetime.now()
    #hoje = datetime.date(2021,2,23)
    Trimestre = str((hoje.month-1)//3+1)
    Tmeses = meses.get(Trimestre)
    mon = list()
    mes = hoje.month
    #mes = datetime.date(2021,3,23).month
    dz = dfC
    dz['DATA_MSG'] = dz['DATA_MSG'].astype('datetime64[ns]')
    #trimestre
    bn = dfC[dfC['DATA_MSG']>=datetime.date(hoje.year,Tmeses[0],1).strftime('%Y-%m-%d')]
    bn = bn[bn['DATA_MSG']<=datetime.date(hoje.year,hoje.month,hoje.day).strftime('%Y-%m-%d')]
    bn = bn['VALOR'].sum()
    ###########
    #dia
    bm = dfC[dfC['DATA_MSG']>=datetime.date(hoje.year,hoje.month,hoje.day).strftime('%Y-%m-%d')]
    bm = bm['VALOR'].sum()
    ###########

    for m in Tmeses:
        if m > mes: mon.append(None)
        elif m == mes:
            try:
                dz = dfC[dfC['DATA_MSG']>=datetime.date(hoje.year,hoje.month,1).strftime('%Y-%m-%d')]
                dz = dz[dz['DATA_MSG']<=datetime.date(hoje.year,hoje.month,hoje.day).strftime('%Y-%m-%d')]
                dz = dz['VALOR'].sum()
                mon.append(dz)
            except: mon.append(None)
        else:
            try:
                dz = dfC[dfC['DATA_MSG']>=datetime.date(hoje.year,m,1).strftime('%Y-%m-%d')]
                dz = dz[dz['DATA_MSG']<=datetime.date(hoje.year,m,last_day_of_month(datetime.date(hoje.year,m,1)).day).strftime('%Y-%m-%d')]
                dz = dz['VALOR'].sum()
                mon.append(dz)
            except: mon.append(None)

    M5S_json = {}
    M5S_json['5S'] = { 'meta': 0.0, 'dia': 0.0, 'acumulado': 0, 'mes1': 0.0, 'mes2': 0, 'mes3': 0 }
    M5S_json['5S']['meta'] = 90.0
    M5S_json['5S']['dia'] = 90
    M5S_json['5S']['mes1'] = mon[0]
    M5S_json['5S']['mes2'] = mon[1]
    M5S_json['5S']['mes3'] = mon[2]
    M5S_json['5S']['acumulado'] = bn

    return(M5S_json)

def get_meta_suca_trf():
    try:
        dbSuca = mysql.connector.connect(host='192.168.61.1', user='jayron', passwd='123123', port='1517', database='lam')
        querysuca = 'SELECT * FROM metas WHERE YEAR(data_msg)=2021 and nome_meta = "sucateamento";'
        dfC = pd.read_sql(querysuca, dbSuca)
    except:
        try: dbSuca.close()
        except: pass
        print('Erro na conexão sql')
        return

    hoje = datetime.date.today()
    #hoje = datetime.datetime.now()
    #hoje = datetime.date(2021,2,23)
    Trimestre = str((hoje.month-1)//3+1)
    Tmeses = meses.get(Trimestre)
    mon = list()
    mes = hoje.month
    #mes = datetime.date(2021,3,23).month
    dz = dfC
    dz['DATA_MSG'] = dz['DATA_MSG'].astype('datetime64[ns]')
    #trimestre
    bn = dfC[dfC['DATA_MSG']>=datetime.date(hoje.year,Tmeses[0],1).strftime('%Y-%m-%d')]
    bn = bn[bn['DATA_MSG']<=datetime.date(hoje.year,hoje.month,hoje.day).strftime('%Y-%m-%d')]
    bn = bn['VALOR'].sum()
    ###########
    #dia
    bm = dfC[dfC['DATA_MSG']>=datetime.date(hoje.year,hoje.month,hoje.day).strftime('%Y-%m-%d')]
    bm = bm['VALOR'].sum()
    ###########

    for m in Tmeses:
        if m > mes: mon.append(None)
        elif m == mes:
            try:
                dz = dfC[dfC['DATA_MSG']>=datetime.date(hoje.year,hoje.month,1).strftime('%Y-%m-%d')]
                dz = dz[dz['DATA_MSG']<=datetime.date(hoje.year,hoje.month,hoje.day).strftime('%Y-%m-%d')]
                dz = dz['VALOR'].sum()
                mon.append(dz)
            except: mon.append(None)
        else:
            try:
                dz = dfC[dfC['DATA_MSG']>=datetime.date(hoje.year,m,1).strftime('%Y-%m-%d')]
                dz = dz[dz['DATA_MSG']<=datetime.date(hoje.year,m,last_day_of_month(datetime.date(hoje.year,m,1)).day).strftime('%Y-%m-%d')]
                dz = dz['VALOR'].sum()
                mon.append(dz)
            except: mon.append(None)

    sucata_json = {}
    sucata_json['sucateamento'] = { 'meta': 0.0, 'dia': 0.0, 'acumulado': 0, 'mes1': 0.0, 'mes2': 0, 'mes3': 0 }
    sucata_json['sucateamento']['meta'] = 3.0
    sucata_json['sucateamento']['dia'] = 0
    sucata_json['sucateamento']['mes1'] = mon[0]
    sucata_json['sucateamento']['mes2'] = mon[1]
    sucata_json['sucateamento']['mes3'] = mon[2]
    sucata_json['sucateamento']['acumulado'] = bn

    return(sucata_json)


registros = {'ACIDENTE CPT':1333,'PROD LAMINADO':1336,'REND. METALICO':1338,'BLBP':1444,'SUCATEAMENTO':1350}
values = {'dia':0,'meta':'N/A'}

meta_json = {
    'ACIDENTE CPT':{'meta':'','dia':0,'acumulado':0,'mes1':0,'mes2':0,'mes3':0},
    'PROD LAMINADO':{'meta':'','dia':0,'acumulado':0,'mes1':0,'mes2':0,'mes3':0},
    'REND. METALICO':{'meta':'','dia':0,'acumulado':0,'mes1':0,'mes2':0,'mes3':0},
    'BLBP':{'meta':'','dia':0,'acumulado':0,'mes1':0,'mes2':0,'mes3':0},
    'SUCATEAMENTO':{'meta':'','dia':0,'acumulado':0,'mes1':0,'mes2':0,'mes3':0},
    'meses':0
}

produto = ''
