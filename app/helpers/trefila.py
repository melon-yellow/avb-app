
#################################################################################################################################################

# Imports
import io
import pandas
import datetime

# Modules
from . import homerico
from . import lastDayOfMonth

#################################################################################################################################################

def trimestre(registro: int):
    # Set Variables
    mon = []

    # Get Now
    now = datetime.datetime.now()
    trim = {
        1: [1,2,3],
        2: [4,5,6],
        3: [7,8,9],
        4: [10,11,12]
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
            mon.append(
                df['acumulado'].values[0]
            )
        # On Error
        except: mon.append(None)
    
    # Return Data
    return mon

#################################################################################################################################################

