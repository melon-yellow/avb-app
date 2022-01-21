
##########################################################################################################################

# Imports
from os import getenv
from json import dumps
from flask import Request, Response
from py_misc.express import Express
from py_misc.schedule import each

# Modules
from .modules import laminador
from .modules import aciaria
from .modules import sap
from .modules import iba

##########################################################################################################################

# Declare HTTP API
app = Express()

# Set API Port
app.port(int(getenv('ODBC_SERVICE_PORT')))

##########################################################################################################################

@app.route('/sap/preditivas/')
def sapPreditivas(req: Request, res: Response):
    kwargs = req.json
    if not isinstance(kwargs, dict): raise Exception('bad request')
    if 'equip' not in kwargs: raise Exception('invalid argument "equip"')
    # Execute Query
    data = sap.preditivas(kwargs['equip'])
    return res(
        dumps(data),
        mimetype='application/json',
        status=200
    )

##########################################################################################################################

@app.route('/aciaria/ld/espectrometro/')
def aciariaLDEspectrometro(req: Request, res: Response):
    data = aciaria.ld.espectrometro()
    return res(
        dumps(data),
        mimetype='application/json',
        status=200
    )

##########################################################################################################################

@app.route('/aciaria/fp/espectrometro/')
def aciariaFPEspectrometro(req: Request, res: Response):
    data = aciaria.fp.espectrometro()
    return res(
        dumps(data),
        mimetype='application/json',
        status=200
    )

##########################################################################################################################

@app.route('/laminador/produto/')
def laminadorRFAL2(req: Request, res: Response):
    data = laminador.produto()
    return res(
        dumps(data),
        mimetype='application/json',
        status=200
    )

##########################################################################################################################

@app.route('/laminador/blbp/')
def laminadorRFAL2(req: Request, res: Response):
    data = laminador.blbp()
    return res(
        dumps(data),
        mimetype='application/json',
        status=200
    )

##########################################################################################################################

@app.route('/laminador/rfa/')
def laminadorRFA(req: Request, res: Response):
    data = laminador.rfa()
    return res(
        dumps(data),
        mimetype='application/json',
        status=200
    )

##########################################################################################################################

@app.route('/laminador/rfal2/')
def laminadorRFAL2(req: Request, res: Response):
    data = laminador.rfal2()
    return res(
        dumps(data),
        mimetype='application/json',
        status=200
    )

##########################################################################################################################

# Scheduled Actions
@each.one.hour.do.at('00:00')
def each_one_hour():
    iba.clear()

##########################################################################################################################

# Start Server
app.start()

# Keep Main Thread Alive
while True: pass

##########################################################################################################################
