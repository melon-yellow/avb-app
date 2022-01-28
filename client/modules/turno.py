
#################################################################################################################################################

# Imports
from datetime import datetime, date
from collections import deque

#################################################################################################################################################

# Refrence Constant
ref = {'2021-04-02': ['B','C','C','C']}

# Matrix Reference
matrix = [
    'D','D','D','A','A','B','B',
    'C','C','C','D','D','A','A',
    'B','B','B','C','C','D','D',
    'A','A','A','B','B','C','C'
]

#################################################################################################################################################

# Get Escala
def escala(
    data: date = date.today(),
    referencia: dict[str,tuple[str,str,str,str]] = ref
):
    try:
        dy = deque(matrix.copy())
        # Get Source Dates
        sourceDates = list(referencia.keys())
        # Get Delta Time
        delta = (data - (
            datetime.strptime(sourceDates[0], '%Y-%m-%d')
        ))
        # Iterate Over Dates
        b = referencia.get(sourceDates[0])
        for i in range(len(matrix)):
            if matrix[i : i + len(b)] == b:
                dy.rotate(-i)
        # Rotates
        dy.rotate(-(delta.days))
        t1 = list(dy)
        dy.rotate(-7)
        t2 = list(dy)
        dy.rotate(13)
        t3 = list(dy)
        # Assembly Data
        dat = (t1, t2, t3)
        # Return Data
        return (True, dat)
    except Exception as error:
        return (False, error)

#################################################################################################################################################
