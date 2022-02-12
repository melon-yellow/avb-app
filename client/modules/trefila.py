
#################################################################################################################################################

# Imports
from io import StringIO
from json import loads
from pandas import read_csv
from asyncio import gather
from datetime import date

# Modules
from .iba import read as fromIba
from .homerico import reports

#################################################################################################################################################

async def get_prod():
    try:
        data = date.today().strftime('%d/%m/%Y')
        (ok, csv) = reports.relatorio_lista(
            data_inicial=data,
            data_final=data,
            id_processo='50'
        )
        if not ok: raise csv
        # Parse Prod
        prod: dict[str, float] = {}
        df = read_csv(StringIO(csv), sep=';')
        df = df.filter(['Produto','Maquina','Peso do Produto'])
        df = df.stack().str.replace(',','.').unstack()
        df['Peso do Produto'] = df['Peso do Produto'].astype(float)
        df = df.groupby('Maquina').sum()
        df = df['Peso do Produto']
        prod.update(loads(df.to_json()))
        # Assembly Data
        dat = {
            'p01': prod['Trefila 01'],
            'p02': prod['Trefila 02'],
            'p03': prod['Trefila 03'],
            'p04': prod['Trefila 04'],
            'p05': prod['Trefila 05']
        }
        # Return Data
        return (True, dat)
    except Exception as error:
        return (False, error)

#################################################################################################################################################

async def get_util():
    try:
        (
            (ok1, util1),
            (ok2, util2),
            (ok3, util3),
            (ok4, util4),
            (ok5, util5),
            (ok1t, time1),
            (ok2t, time2),
            (ok3t, time3),
            (ok4t, time4),
            (ok5t, time5),
            (okt, time_plc)
        ) = await gather(
            fromIba(''), # util 1
            fromIba(''), # util 2
            fromIba(''), # util 3
            fromIba(''), # util 4
            fromIba(''), # util 5
            fromIba(''), # time util 1
            fromIba(''), # time util 2
            fromIba(''), # time util 3
            fromIba(''), # time util 4
            fromIba(''), # time util 5
            fromIba('')  # time plc
        )
        # Check Response
        if not ok1: raise util1
        if not ok2: raise util2
        if not ok3: raise util3
        if not ok4: raise util4
        if not ok5: raise util5
        if not ok1t: raise time1
        if not ok2t: raise time2
        if not ok3t: raise time3
        if not ok4t: raise time4
        if not ok5t: raise time5
        if not okt: raise time_plc
        # Check Response
        if not isinstance(time_plc, (int, float)):
            raise Exception(f'invalid response: time_plc: {time_plc}')
        # Calc Time Stopped
        stop1 = (time_plc - time1) / 60
        stop2 = (time_plc - time2) / 60
        stop3 = (time_plc - time3) / 60
        stop4 = (time_plc - time4) / 60
        stop5 = (time_plc - time5) / 60
        # Check Result
        if not isinstance(util1, (int, float)): raise Exception(f'invalid response: util1: {util1}')
        if not isinstance(util2, (int, float)): raise Exception(f'invalid response: util2: {util2}')
        if not isinstance(util3, (int, float)): raise Exception(f'invalid response: util3: {util3}')
        if not isinstance(util4, (int, float)): raise Exception(f'invalid response: util4: {util4}')
        if not isinstance(util5, (int, float)): raise Exception(f'invalid response: util5: {util5}')
        if not isinstance(stop1, (int, float)): raise Exception(f'invalid response: stop1: {stop1}')
        if not isinstance(stop2, (int, float)): raise Exception(f'invalid response: stop2: {stop2}')
        if not isinstance(stop3, (int, float)): raise Exception(f'invalid response: stop3: {stop3}')
        if not isinstance(stop4, (int, float)): raise Exception(f'invalid response: stop4: {stop4}')
        if not isinstance(stop5, (int, float)): raise Exception(f'invalid response: stop5: {stop5}')
        # Assembly Data
        data: dict[str, float] = {
            'u01': util1,
            'u02': util2,
            'u03': util3,
            'u04': util4,
            'u05': util5,
            't01': stop1,
            't02': stop2,
            't03': stop3,
            't04': stop4,
            't05': stop5,
            's': time_plc
        }
        # Return Data
        return (True, data)
    except Exception as error:
        return (False, error)

#################################################################################################################################################

async def produtividade():
    try:
        data: dict[str, float] = {}
        (
            (ok1, prod),
            (ok2, util)
        ) = await gather(
            get_prod(),
            get_util()
        )
        # Check Result
        if not ok1: raise prod
        if not ok2: raise util
        # Update Data
        data.update(prod)
        data.update(util)
        # Return Data
        return (True, data)
    except Exception as error:
        return (False, error)

#################################################################################################################################################
