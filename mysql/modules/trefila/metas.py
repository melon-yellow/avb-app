
#################################################################################################################################################

# Imports
from datetime import datetime, date
from pandas import DataFrame, to_datetime
from typing import Callable

# Modules
from ..helpers import lastDayOfMonth

##########################################################################################################################

def getMetaDay(
    df: DataFrame,
    now: datetime
) -> float:
    dt = to_datetime(date(now.year, now.month, now.day))
    return df[df['DATA_MSG'] >= dt]['VALOR'].sum()

#################################################################################################################################################

# Iterate over Months
def trimStartEndDates(
    month: int,
    now: datetime
) -> tuple[str, str]:
    if month > now.month: return (None, None)
    day = (
        now.day if month == now.month else
        lastDayOfMonth(date(now.year, month, 1)).day
    )
    sdate = date(now.year, month, 1)
    edate = date(now.year, now.month, day)
    return (sdate, edate)

#################################################################################################################################################

def getMetaTrim(
    df: DataFrame,
    now: datetime,
    parser: Callable[
        [DataFrame, tuple[date, date]],
        float
    ]
) -> dict[str, float]:
    # Trimestre
    tlst = dict[int, tuple[int, int, int]]
    trims: tlst = { 1: (1, 2, 3), 2: (4, 5, 6), 3: (7, 8, 9), 4: (10, 11, 12) }
    trim = trims[1 + ((now.month - 1) // 3)]
    # Helper Lambdas
    helper = lambda m: (m, lastDayOfMonth(date(now.year, m, 1)))
    # Return Data
    return {
        'acumulado': parser(df, trimStartEndDates(trim[0], now)),
        'mes1': parser(df, trimStartEndDates(*helper(trim[0]))),
        'mes2': parser(df, trimStartEndDates(*helper(trim[1]))),
        'mes3': parser(df, trimStartEndDates(*helper(trim[2])))
    }

#################################################################################################################################################

# Iterate over Months
def metaTrimParser(
    df: DataFrame,
    dates: tuple[date, date]
) -> float:
    dts = (to_datetime(dates[0]), to_datetime(dates[1]))
    query = (dts[0] <= df['DATA_MSG']) & (df['DATA_MSG'] <= dts[1])
    return df[query]['VALOR'].sum()

#################################################################################################################################################

# Iterate over Months
def utilTrimParser(
    df: DataFrame,
    dates: tuple[date, date]
) -> float:
    dts = (to_datetime(dates[0]), to_datetime(dates[1]))
    query = (dts[0] <= df['DATA']) & (df['DATA'] <= dts[1])
    fltr = ['DATA','M1','M2','M3','M4','M5']
    return df[query]['VALOR'].filter(fltr).drop(['M1'], axis=1).mean().mean()

#################################################################################################################################################
