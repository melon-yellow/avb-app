
#################################################################################################################################################

import io
import json
import pandas
import datetime

from . import homerico

#################################################################################################################################################

def trefila():
    # get date
    date = datetime.datetime.today().strftime('%d/%m/%Y')
    csv = homerico.network.relatorio_lista(
        data_inicial=date, data_final=date, id_processo='50'
    )
    df = pandas.read_csv(io.StringIO(csv), sep=';')
    # Set Prod
    prod: dict[str, float] = {}
    try:
        df = df.filter(['Produto','Maquina','Peso do Produto'])
        df = df.stack().str.replace(',','.').unstack()
        df['Peso do Produto'] = df['Peso do Produto'].astype(float)
        df = df.groupby('Maquina').sum()
        df = df['Peso do Produto']
        prod.update(json.loads(df.to_json()))
    except: pass
    # get prod data
    data = {
        'p01': prod.get('Trefila 01'),
        'p02': prod.get('Trefila 02'),
        'p03': prod.get('Trefila 03'),
        'p04': prod.get('Trefila 04'),
        'p05': prod.get('Trefila 05')
    }
    # get util data
    utilTrefila = iba.read('UTIL')
    data.update({
        's': utilTrefila.get('SEC'),
        'u01': utilTrefila.get('m01', {}).get('UTIL'),
        'u02': utilTrefila.get('m02', {}).get('UTIL'),
        'u03': utilTrefila.get('m03', {}).get('UTIL'),
        'u04': utilTrefila.get('m04', {}).get('UTIL'),
        'u05': utilTrefila.get('m05', {}).get('UTIL'),
        't01': utilTrefila.get('m01', {}).get('TEMPO_PARADO'),
        't02': utilTrefila.get('m02', {}).get('TEMPO_PARADO'),
        't03': utilTrefila.get('m03', {}).get('TEMPO_PARADO'),
        't04': utilTrefila.get('m04', {}).get('TEMPO_PARADO'),
        't05': utilTrefila.get('m05', {}).get('TEMPO_PARADO')
    })
    # Return Data
    return data

#################################################################################################################################################
