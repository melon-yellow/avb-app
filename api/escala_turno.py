from collections import deque
import datetime

def getEscala(sample = {'2021-04-02':['B','C','C','C']},dia = datetime.date.today()):
    t = []
    std = ['D','D','D','A','A','B','B','C','C','C','D','D','A','A','B','B','B','C','C','D','D','A','A','A','B','B','C','C']
    dy = deque(std)
    dx = std.copy()
    d0 = datetime.datetime.strptime(list(sample.keys())[0], '%Y-%m-%d').date()
    #d1 = datetime.datetime.strptime(dia, '%Y-%m-%d').date()
    d1 = dia
    delta = d1 - d0
    days = delta.days

    b = list(sample.keys())[0]
    b = sample.get(b)

    for i in range(len(dx)):
        if dx[i:i+len(b)] == b:
            dy.rotate(i*-1)
    dy.rotate(-1*(days))
    t0 = dy.copy()

    dy.rotate(-7)
    t1 = dy.copy()

    dy.rotate(13)
    t2 = dy.copy()

    t0 = list(t0)
    t1 = list(t1)
    t2 = list(t2)

    t.append(t0)
    t.append(t1)
    t.append(t2)

    return (t)

#print(getEscala())
