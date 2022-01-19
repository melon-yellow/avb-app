
#################################################################################################################################################

# Imports
import datetime

#################################################################################################################################################

# string to number
def num(string: str, ptbr: bool = False):
    if string == '': return None
    string = string.replace(' ','')
    if ptbr:
        string = string.replace('.','')
        string = string.replace(',','.')
    return float(string)

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
def lastDayOfMonth(date: datetime.datetime):
    if date.month == 12: return date.replace(day=31)
    return (
        date.replace(month=(date.month + 1), day=1) -
        datetime.timedelta(days=1)
    )

#################################################################################################################################################
