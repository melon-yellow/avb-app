
##########################################################################################################################

# Imports
from json import dumps
from flask import Flask, Response

# Routes
from .modules.laminador import forno

##########################################################################################################################

# Declare HTTP API
app = Flask('oracle_client')

##########################################################################################################################

@app.route('/laminador/forno/')
async def laminadorForno():
    (ok, data) = await forno()
    res = (
        {'ok': ok, 'data': data}
        if ok else
        {'ok': ok, 'error': f'{data}'}
    )
    return Response(
        dumps(res),
        mimetype='application/json',
        status=200
    )

##########################################################################################################################
