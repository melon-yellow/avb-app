
##########################################################################################################################

# Imports
from os import getenv
from json import dumps
from flask import Request, Response
from py_misc import schedule, express

# Modules
from .modules import laminador
from .modules import aciaria
from .modules import sap
from .modules import iba

##########################################################################################################################

# Declare HTTP API
app = express.Express()

# Set API Port
app.port(int(getenv('ODBC_SERVICE_PORT')))

##########################################################################################################################

@app.route('/odbc/sap/preditivas/')
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

@app.route('/odbc/aciaria/ld/espectrometro/')
def aciariaLDEspectrometro(req: Request, res: Response):
    data = aciaria.ld.espectrometro()
    return res(
        dumps(data),
        mimetype='application/json',
        status=200
    )

##########################################################################################################################

@app.route('/odbc/aciaria/fp/espectrometro/')
def aciariaFPEspectrometro(req: Request, res: Response):
    data = aciaria.fp.espectrometro()
    return res(
        dumps(data),
        mimetype='application/json',
        status=200
    )

##########################################################################################################################

@app.route('/odbc/laminador/produto/')
def laminadorRFAL2(req: Request, res: Response):
    data = laminador.produto()
    return res(
        dumps(data),
        mimetype='application/json',
        status=200
    )

##########################################################################################################################

@app.route('/odbc/laminador/blbp/')
def laminadorRFAL2(req: Request, res: Response):
    data = laminador.blbp()
    return res(
        dumps(data),
        mimetype='application/json',
        status=200
    )

##########################################################################################################################

@app.route('/odbc/laminador/rfa/')
def laminadorRFA(req: Request, res: Response):
    data = laminador.rfa()
    return res(
        dumps(data),
        mimetype='application/json',
        status=200
    )

##########################################################################################################################

@app.route('/odbc/laminador/rfal2/')
def laminadorRFAL2(req: Request, res: Response):
    data = laminador.rfal2()
    return res(
        dumps(data),
        mimetype='application/json',
        status=200
    )

##########################################################################################################################

# Scheduled Actions
@schedule.each.one.hour.do.at('00:00')
def each_one_hour():
    iba.clear()

##########################################################################################################################

# Start Server
app.start()

# Keep Main Thread Alive
while True: pass

##########################################################################################################################
