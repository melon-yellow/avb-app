
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
    try:
        (ok, data) = await forno()
        if not ok: raise data
        return Response(
            dumps(data),
            mimetype='application/json',
            status=200
        )
    except Exception as error:
        print(error)

##########################################################################################################################
