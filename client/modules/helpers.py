
#################################################################################################################################################

# Imports
from datetime import datetime, timedelta

#################################################################################################################################################

# string to number
def num(text: str, sep: str = ',', rem: str = '.'):
    mem = str(text).replace(' ','')
    mem = mem.replace(rem, '').replace(sep, '.')
    return float(mem)

#################################################################################################################################################

# csv to matrix
def matrix(
    txt: str,
    columnbreak: str = ';',
    linebreak: str = '\n'
):
    return list(
        map(
            lambda line: line.split(columnbreak),
            txt.split(linebreak)
        )
    )

#################################################################################################################################################

# Get Last Day Of Month
def lastDayOfMonth(date: datetime):
    if date.month == 12: return date.replace(day=31)
    return (
        date.replace(month=(date.month + 1), day=1) -
        timedelta(days=1)
    )

#################################################################################################################################################
