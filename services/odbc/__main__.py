
##########################################################################################################################

# Imports
import os
import json
import flask
import py_misc

# Routes
from . import laminador

##########################################################################################################################

# Declare HTTP API
app = py_misc.Express()

# Set API Port
app.port(
    int(os.getenv('ODBC_NETWORK_PORT'))
)

#################################################################################################################################################

Request = flask.Request
Response = flask.Response

##########################################################################################################################

@app.route('/odbc/laminador/produto/')
def laminadorRFAL2(req: Request, res: Response):
    data = laminador.product()
    return res(
        json.dumps(data),
        mimetype='application/json',
        status=200
    )

##########################################################################################################################

@app.route('/odbc/laminador/rfa/')
def laminadorRFA(req: Request, res: Response):
    data = laminador.rfa()
    return res(
        json.dumps(data),
        mimetype='application/json',
        status=200
    )

##########################################################################################################################

@app.route('/odbc/laminador/rfal2/')
def laminadorRFAL2(req: Request, res: Response):
    data = laminador.rfal2()
    return res(
        json.dumps(data),
        mimetype='application/json',
        status=200
    )

##########################################################################################################################

# Start Server
app.start()

# Keep Main Thread Alive
py_misc.keepalive()

##########################################################################################################################
