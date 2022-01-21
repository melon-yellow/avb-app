
#################################################################################################################################################

# Imports
from io import StringIO
from json import loads
from pandas import read_csv
from datetime import datetime

# Modules
from .iba import read as fromIba
from .homerico import reports

#################################################################################################################################################

def trefila():
    # get date
    date = datetime.today().strftime('%d/%m/%Y')
    csv = reports.relatorio_lista(
        data_inicial=date, data_final=date, id_processo='50'
    )
    df = read_csv(StringIO(csv), sep=';')
    # Set Prod
    prod: dict[str, float] = {}
    df = df.filter(['Produto','Maquina','Peso do Produto'])
    df = df.stack().str.replace(',','.').unstack()
    df['Peso do Produto'] = df['Peso do Produto'].astype(float)
    df = df.groupby('Maquina').sum()
    df = df['Peso do Produto']
    prod.update(loads(df.to_json()))
    # get prod data
    data = {
        'p01': prod['Trefila 01'],
        'p02': prod['Trefila 02'],
        'p03': prod['Trefila 03'],
        'p04': prod['Trefila 04'],
        'p05': prod['Trefila 05']
    }
    # get util data
    (ok, util) = fromIba('0:23')
    if not ok: raise Exception(util)
    util: dict = loads(util)
    data.update({
        's': util['SEC'],
        'u01': util['m01']['UTIL'],
        'u02': util['m02']['UTIL'],
        'u03': util['m03']['UTIL'],
        'u04': util['m04']['UTIL'],
        'u05': util['m05']['UTIL'],
        't01': util['m01']['TEMPO_PARADO'],
        't02': util['m02']['TEMPO_PARADO'],
        't03': util['m03']['TEMPO_PARADO'],
        't04': util['m04']['TEMPO_PARADO'],
        't05': util['m05']['TEMPO_PARADO']
    })
    # Return Data
    return data

#################################################################################################################################################
