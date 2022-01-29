
##########################################################################################################################

# Imports
from json import dumps
from flask import Flask, request, Response

# Modules
from .modules.iba import clear
from .modules.sap import preditivas
from .modules.aciaria import fp, ld
from .modules.laminador import produto, blbp, rfa, rfal2

##########################################################################################################################

# Declare WSGI APP
app = Flask('odbc_client')

##########################################################################################################################

@app.route('/sap/preditivas/')
async def sapPreditivas():
    res = {}
    try:
        kwargs = request.json
        if not isinstance(kwargs, dict): raise Exception('bad request')
        if 'equip' not in kwargs: raise Exception('invalid argument "equip"')
        # Fetch Data
        (ok, data) = await preditivas(kwargs['equip'])
        if not ok: raise data
        # Return Data
        res = {'ok': True, 'data': data}
    except Exception as error:
        res = {'ok': False, 'error': f'{error}'}
    # Return View
    return Response(
        dumps(res),
        mimetype='application/json',
        status=200
    )

##########################################################################################################################

@app.route('/aciaria/ld/espectrometro/')
def aciariaLDEspectrometro():
    (ok, data) = ld.espectrometro()
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

@app.route('/aciaria/fp/espectrometro/')
def aciariaFPEspectrometro():
    (ok, data) = fp.espectrometro()
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

@app.route('/laminador/produto/')
def laminadorRFAL2():
    (ok, data) = produto()
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

@app.route('/laminador/blbp/')
def laminadorRFAL2():
    (ok, data) = blbp()
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

@app.route('/laminador/rfa/')
def laminadorRFA():
    (ok, data) = rfa()
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

@app.route('/laminador/rfal2/')
def laminadorRFAL2():
    (ok, data) = rfal2()
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

@app.route('/laminador/iba/clear/')
def laminadorIbaClear():
    (ok, data) = clear()
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
