
##########################################################################################################################

# Imports
import os
import json
import flask
import py_misc

# Modules
from . import laminador
from . import aciaria

##########################################################################################################################

# Declare HTTP API
app = py_misc.Express()

# Set API Port
app.port(
    int(os.getenv('ODBC_SERVICE_PORT'))
)

#################################################################################################################################################

Request = flask.Request
Response = flask.Response

##########################################################################################################################

@app.route('/odbc/aciaria/ld/espectrometro/')
def aciariaLDEspectrometro(req: Request, res: Response):
    data = aciaria.espectrometroLD()
    return res(
        json.dumps(data),
        mimetype='application/json',
        status=200
    )

##########################################################################################################################

@app.route('/odbc/aciaria/fp/espectrometro/')
def aciariaFPEspectrometro(req: Request, res: Response):
    data = aciaria.espectrometroFP()
    return res(
        json.dumps(data),
        mimetype='application/json',
        status=200
    )

##########################################################################################################################

@app.route('/odbc/laminador/produto/')
def laminadorRFAL2(req: Request, res: Response):
    data = laminador.produto()
    return res(
        json.dumps(data),
        mimetype='application/json',
        status=200
    )

##########################################################################################################################

@app.route('/odbc/laminador/blbp/')
def laminadorRFAL2(req: Request, res: Response):
    data = laminador.blbp()
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
