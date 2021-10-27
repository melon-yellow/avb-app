
#################################################################################################################################################

# Imports
import io
import re
import pandas
import datetime

# Modules
from .. import homerico
from . import classification as clas

#################################################################################################################################################

def extract(date: str):
    datas = []
    date = date.replace('-','/')
    date = date.split()
    # Iter Over Dates
    for dat in date:
        try:
            if re.search(
                '^([0-9]|0[0-9]|1[0-9]|2[0-9]|3[0-1])(.|-)([0-9]|0[0-9]|1[0-2])(.|-|)20[0-9][0-9]$',
                dat
            ):
                date_time_obj = datetime.datetime.strptime(dat, '%d/%m/%Y')
                datas.append(date_time_obj)
                datas.sort()
            elif re.search(
                '^([0-9]|0[0-9]|1[0-9]|2[0-9]|3[0-1])(.|-)([0-9]|0[0-9]|1[0-2])(.|-|)[0-9][0-9]$',
                dat
            ):
                date_time_obj = datetime.datetime.strptime(dat, '%d/%m/%y')
                datas.append(date_time_obj)
                datas.sort()
            elif re.search(
                '^([0-9]|0[0-9]|1[0-9]|2[0-9]|3[0-1])(.|-)([0-9]|0[0-9]|1[0-2])$',
                dat
            ):
                dat = dat + '/' + datetime.datetime.strftime(
                    datetime.datetime.today(),
                    '%y'
                )
                date_time_obj = datetime.datetime.strptime(dat, '%d/%m/%y')
                datas.append(date_time_obj)
        # Exception
        except: pass

    # Check Date Length
    if len(datas) < 2: datas.append(datas[0])
    return datas

#################################################################################################################################################

def message(txt: str):
    try:
        saida = dict()
        msg = clas.classifique(txt)

        # producao
        if ('produção' in msg.keys()):
            #tem intervalo?
            if('ontem' in msg.keys() and msg['ontem'] > 1):
                d = datetime.datetime.now() - datetime.timedelta(days = 1)
                d = datetime.datetime.strftime(d, '%d/%m/%Y')
                d = '{} {}'.format(d,d)
                if('produto' in msg.keys() and 
                    re.findall(r'(\d+\.\d+|\d+\,\d+)', txt)
                ):
                    param = re.findall(r'(\d+\.\d+|\d+\,\d+)', txt)
                    return search(d,param)
                else:
                    return search(d,'32')

            elif ('hoje' in msg.keys() and msg['hoje'] > 1):
                d = datetime.datetime.now()
                d = datetime.datetime.strftime(d, '%d/%m/%Y')
                d = '{} {}'.format(d,d)
                if ('produto' in msg.keys() and
                    re.findall(r'(\d+\.\d+|\d+\,\d+)', txt)
                ):
                    param = re.findall(r'(\d+\.\d+|\d+\,\d+)', txt)
                    return search(d,param)
                else:
                    return search(d,'32')

            elif (extract(txt)):
                if('produto' in msg.keys() and
                    re.findall(r'(\d+\.\d+|\d+\,\d+)', txt)):
                    param = re.findall(r'(\d+\.\d+|\d+\,\d+)', txt)
                    return search(txt, param)
                else:
                    return search(txt,'32')

            else:
                d = datetime.datetime.now()
                d = datetime.datetime.strftime(d, '%d/%m/%Y')
                d = '{} {}'.format(d,d)
                if('produto' in msg.keys() and 
                    re.findall(r'(\d+\.\d+|\d+\,\d+)', txt)):
                    param = re.findall(r'(\d+\.\d+|\d+\,\d+)', txt)
                    return search(d,param)
                else:
                    return search(d,'32')

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
            elif (extract(txt)):

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

def search(raw_intervalo, parametro):

    try:
        if(len(parametro)>1):
            parametro = parametro.replace(',','.')
        else:
            parametro = parametro[0].replace(',','.')

        saida = dict()
        e = []
        datas = extract(raw_intervalo)

        delta = datas[1] - datas[0]

        if(delta !=0):
            delta = delta.days
        else:
            delta =1

        for d in datas:
            e.append(datetime.datetime.strftime(d, '%d/%m/%Y'))
        datas = e

    #if(1):
        csv = homerico.__dll__.RelatorioLista(datas[0], datas[1], '32')
        df = pandas.read_csv(io.StringIO(csv), sep=';', dtype='object')
        df['size'] = df['Produto'].str.findall(r'\d+(?:,\d+)?').str[-1]
        df['size'] = df['size'].str.replace(',','.')
        df['size'] = df['size'].apply(pandas.to_numeric, errors='coerce')
        df['Peso do Produto'] = df['Peso do Produto'].apply(pandas.to_numeric, errors='coerce')
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
            if (delta > 1 and parametro == '32'):
                saida['answer'] = (df + '\n\nMédia dos ({})dias : *{} tons/dia*'.format(delta,(z/delta).round(1)) +
                    '\n\nTotal Geral produzido no período: *{} toneladas*\n'.format((z).round(1)) + '')
            else: saida['answer'] = df + '\n\nTotal Geral produzido: {} toneladas\n'.format(z.round(1))
        else: saida['answer'] = 'Não encontrei nada com esse critério'
    except: saida['answer'] = 'Ocorreu um erro enquanto eu fazia a consulta!'
    return saida

#################################################################################################################################################
