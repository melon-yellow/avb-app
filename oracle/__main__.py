
##########################################################################################################################

# Imports
from os import getenv
from json import dumps
from flask import Request, Response
from py_misc import express

# Routes
from .modules import furnace

##########################################################################################################################

# Declare HTTP API
app = express.Express()

# Set API Port
app.port(int(getenv('ORACLE_SERVICE_PORT')))

##########################################################################################################################

@app.route('/laminador/forno/')
def furnaceGusaapp(req: Request, res: Response):
    data = furnace.gusaapp()
    data.update({
        'UTIL': iba.read('0:5'),
        'TEMPO_PARADO': iba.read('2:25') / 60
    })
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
