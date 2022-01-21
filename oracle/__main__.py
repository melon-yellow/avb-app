
##########################################################################################################################

# Imports
from os import getenv
from json import dumps
from flask import Request, Response
from py_misc.express import Express

# Routes
from .modules.furnace import gusaapp

##########################################################################################################################

# Declare HTTP API
app = Express()

# Set API Port
app.port(int(getenv('ORACLE_SERVICE_PORT')))

##########################################################################################################################

@app.route('/laminador/forno/')
def furnaceGusaapp(req: Request, res: Response):
    data = gusaapp()
    return res(
        dumps(data),
        mimetype='application/json',
        status=200
    )

##########################################################################################################################

# Start Server
app.start()

# Keep Main Thread Alive
while True: pass

##########################################################################################################################
