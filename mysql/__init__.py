
##########################################################################################################################

# Imports
from json import dumps
from flask import Flask, Response

# Modules
from .modules.trefila import utilizacao, metas, all_metas

##########################################################################################################################

# Declare WSGI APP
app = Flask('client_mysql')

##########################################################################################################################

@app.route('/trefila/utilizacao/')
def trefilaUtilizacao():
    (ok, data) = utilizacao()
    if not ok: return Response(
        dumps({'ok': False, 'error': f'{data}'}),
        mimetype='application/json',
        status=200
    )
    return Response(
        data,
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
    (ok, data) = await all_metas()
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
