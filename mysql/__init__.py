
##########################################################################################################################

# Imports
from json import dumps
from flask import Flask, Response
from asyncio import gather

# Modules
from .modules.trefila import utilizacao, metas
from .modules.homerico import trefila

##########################################################################################################################

# Declare WSGI APP
app = Flask('client_mysql')

##########################################################################################################################

@app.route('/trefila/utilizacao/')
def trefilaUtilizacao():
    (ok, csv) = utilizacao()
    if not ok: raise csv
    # Retrun Data
    return Response(
        csv,
        mimetype='text/csv',
        headers={
            'Content-disposition': (
                'attachment; filename=utilizacao.csv'
            )
        },
        status=200
    )

##########################################################################################################################

@app.route('/trefila/metas/5s/')
async def trefilaMetasS5():
    (ok, data) = await metas.s5()
    res = (
        {'ok': True, 'data': data} if ok else
        {'ok': False, 'error': f'{data}'}
    )
    return Response(
        dumps(res),
        mimetype='application/json',
        status=200
    )

##########################################################################################################################

@app.route('/trefila/metas/custo/')
async def trefilaMetasCusto():
    (ok, data) = await metas.custo()
    res = (
        {'ok': True, 'data': data} if ok else
        {'ok': False, 'error': f'{data}'}
    )
    return Response(
        dumps(res),
        mimetype='application/json',
        status=200
    )

##########################################################################################################################

@app.route('/trefila/metas/sucata/')
async def trefilaMetasSucata():
    (ok, data) = await metas.sucata()
    res = (
        {'ok': True, 'data': data} if ok else
        {'ok': False, 'error': f'{data}'}
    )
    return Response(
        dumps(res),
        mimetype='application/json',
        status=200
    )

##########################################################################################################################

@app.route('/trefila/metas/utilizacao/')
async def trefilaMetasUtilizacao():
    (ok, data) = await metas.utilizacao()
    res = (
        {'ok': True, 'data': data} if ok else
        {'ok': False, 'error': f'{data}'}
    )
    return Response(
        dumps(res),
        mimetype='application/json',
        status=200
    )

#################################################################################################################################################

@app.route('/trefila/metas/')
async def trefilaMetas():
    res = {}
    try:
        (
            (ok1, s5),
            (ok2, custo),
            (ok3, sucata),
            (ok4, outras),
            (ok5, utilizacao)
        ) = await gather(
            metas.s5(),
            metas.custo(),
            metas.sucata(),
            trefila.metas(),
            metas.utilizacao()
        )
        # Check Response
        if not ok1: raise s5
        if not ok2: raise custo
        if not ok3: raise sucata
        if not ok4: raise outras
        # if not ok5: raise utilizacao
        # Assembly Data
        data = {
            '5S': s5,
            'custo': custo,
            # 'utilizacao': utilizacao,
            'sucateamento': sucata
        }
        data.update(outras)
        # Return Data
        res = {'ok': True, 'data': data}
    except Exception as error:
        res = {'ok': False, 'error': f'{error}'}
    # Return Data
    return Response(
        dumps(res),
        mimetype='application/json',
        status=200
    )

##########################################################################################################################
