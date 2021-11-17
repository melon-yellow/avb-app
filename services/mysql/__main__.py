
##########################################################################################################################

# Imports
import os
import json
import flask
import py_misc

# Routes
from . import trefila

##########################################################################################################################

# Declare HTTP API
app = py_misc.Express()

# Set API Port
app.port(
    int(os.getenv('MYSQL_SERVICE_PORT'))
)

#################################################################################################################################################

Request = flask.Request
Response = flask.Response

##########################################################################################################################

@app.route('/mysql/trefila/utilizacao/turno/')
def trefilaUtilizacaoTurno(req: Request, res: Response):
    try:
        data = trefila.utilizacaoTurno()
        return res(
            data,
            mimetype='text/csv',
            status=200
        )
    except Exception as e:
        return res(
            json.dumps({ 'error': str(e) }),
            mimetype='application/json',
            status=200
        )

##########################################################################################################################

@app.route('/mysql/trefila/utilizacao/')
def trefilaUtilizacao(req: Request, res: Response):
    data = trefila.utilizacao()
    return res(
        json.dumps(data),
        mimetype='application/json',
        status=200
    )

##########################################################################################################################

@app.route('/mysql/trefila/custo/')
def trefilaCusto(req: Request, res: Response):
    data = trefila.custo()
    return res(
        json.dumps(data),
        mimetype='application/json',
        status=200
    )

##########################################################################################################################

@app.route('/mysql/trefila/sucata/')
def trefilaSucata(req: Request, res: Response):
    data = trefila.sucata()
    return res(
        json.dumps(data),
        mimetype='application/json',
        status=200
    )

##########################################################################################################################

@app.route('/mysql/trefila/cincos/')
def trefilaCincoS(req: Request, res: Response):
    data = trefila.cincos()
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
