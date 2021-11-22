
##########################################################################################################################

# Imports
import os
import json
import flask
import py_misc

# Routes
from .modules import furnace

##########################################################################################################################

# Declare HTTP API
app = py_misc.Express()

# Set API Port
app.port(
    int(os.getenv('ORACLE_SERVICE_PORT'))
)

#################################################################################################################################################

Request = flask.Request
Response = flask.Response

##########################################################################################################################

@app.route('/oracle/furnace/gusaapp/')
def furnaceGusaapp(req: Request, res: Response):
    data = furnace.gusaapp()
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
