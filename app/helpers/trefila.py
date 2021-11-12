
#################################################################################################################################################

# Imports
import io
import json
import pandas
import datetime

# Modules
from . import homerico
from . import lastDayOfMonth

#################################################################################################################################################

# Get Registro Trimestre
def trimestre(registro: int):
    # Set Variables
    acc: list[float] = []

    # Get Now
    now = datetime.datetime.now()
    trim: tuple[int, int, int] = {
        1: (1, 2, 3),
        2: (4, 5, 6),
        3: (7, 8, 9),
        4: (10, 11, 12)
    }.get(
        ((now.month - 1) // 3) + 1
    )

    # Iterate over Months
    for month in trim:
        try:
            # Check Month
            day = 0
            if month > now.month: raise Exception('invalid month')
            if month < now.month: day = lastDayOfMonth(
                datetime.date(now.year, month, 1)
            ).day
            if month == now.month: day = now.day
            # Get Data
            data = datetime.date(now.year, month, day).strftime('%d/%m/%Y')
            csv = homerico.network.RelatorioGerencialRegistro(
                data=data,
                registro=str(registro)
            )
            df = pandas.read_csv(
                io.StringIO(csv),
                sep=';'
            )
            acc.append(
                df['acumulado'].values[0]
            )
        # On Error
        except: acc.append(None)

    # Turn to Tuple
    tacc: tuple[
        float | None,
        float | None,
        float | None
    ] = tuple(acc)
    
    # Return Data
    return tacc

#################################################################################################################################################

# Get Proucao Maquinas
def producaoMaquinas():
    # get date
    date = datetime.datetime.today().strftime('%d/%m/%Y')

    # read meta
    csv = homerico.network.RelatorioLista(
        dataInicial=date,
        dataFinal=date,
        idProcesso='50'
    )
    df = pandas.read_csv(
        io.StringIO(csv),
        sep=';'
    )

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

    # Return Data
    return data

#################################################################################################################################################
