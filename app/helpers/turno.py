
#################################################################################################################################################

# Imports
import os
import datetime
from collections import deque

#################################################################################################################################################

# Escala
class escala:
    def get(
        self,
        day: datetime.datetime = None,
        sample: dict[str,tuple[str,str,str,str]] = None
    ):
        # Check Inputs
        if day == None: day = datetime.date.today()
        if sample == None: sample = {
            '2021-04-02': ['B','C','C','C']
        }
        # Set Refrence Variables
        dx = [
            'D','D','D','A','A','B','B',
            'C','C','C','D','D','A','A',
            'B','B','B','C','C','D','D',
            'A','A','A','B','B','C','C'
        ]
        dy = deque(dx.copy())
        # Get Source Dates
        sourceDates = list(sample.keys())
        # Get Delta Time
        delta = day - (
            datetime.datetime.strptime(
                sourceDates[0],
                '%Y-%m-%d'
            )
        )
        # Iterate Over Dates
        b = sample.get(sourceDates[0])
        for i in range(len(dx)):
            if dx[i : i + len(b)] == b:
                dy.rotate(-i)
        # Rotates
        dy.rotate(-delta.days)
        t1 = list(dy)
        dy.rotate(-7)
        t2 = list(dy)
        dy.rotate(13)
        t3 = list(dy)
        # Return Data
        return (t1, t2, t3)

#################################################################################################################################################
