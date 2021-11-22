
##########################################################################################################################

# Imports
import os
import json
import flask
import py_misc

# Routes
from .modules import trefila

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

@app.route('/mysql/trefila/utilizacao/')
def trefilaUtilizacaoTurno(req: Request, res: Response):
    data = trefila.utilizacao()
    return res(
        data,
        mimetype='text/csv',
        status=200
    )

##########################################################################################################################

@app.route('/mysql/trefila/metas/utilizacao/')
def trefilaUtilizacao(req: Request, res: Response):
    data = trefila.metas.utilizacao()
    return res(
        json.dumps(data),
        mimetype='application/json',
        status=200
    )

##########################################################################################################################

@app.route('/mysql/trefila/metas/custo/')
def trefilaCusto(req: Request, res: Response):
    data = trefila.metas.custo()
    return res(
        json.dumps(data),
        mimetype='application/json',
        status=200
    )

##########################################################################################################################

@app.route('/mysql/trefila/metas/sucata/')
def trefilaSucata(req: Request, res: Response):
    data = trefila.metas.sucata()
    return res(
        json.dumps(data),
        mimetype='application/json',
        status=200
    )

##########################################################################################################################

@app.route('/mysql/trefila/metas/cincos/')
def trefilaCincoS(req: Request, res: Response):
    data = trefila.metas.cincos()
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
