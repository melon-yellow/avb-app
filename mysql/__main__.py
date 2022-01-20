
##########################################################################################################################

# Imports
from os import getenv
from json import dumps
from flask import Request, Response
from py_misc import express

# Modules
from .modules import trefila, homerico

##########################################################################################################################

# Declare HTTP API
app = express.Express()

# Set API Port
app.port(int(getenv('MYSQL_SERVICE_PORT')))

##########################################################################################################################

@app.route('/mysql/trefila/utilizacao/')
def trefilaUtilizacao(req: Request, res: Response):
    # Query Data
    csv = trefila.utilizacao()
    # Retrun Data
    return res(
        csv,
        mimetype='text/csv',
        headers={
            'Content-disposition': (
                'attachment; filename=utilizacao.csv'
            )
        },
        status=200
    )

##########################################################################################################################

@app.route('/mysql/trefila/metas/utilizacao/')
def trefilaMetasUtilizacao(req: Request, res: Response):
    data = trefila.metas.utilizacao()
    return res(
        dumps(data),
        mimetype='application/json',
        status=200
    )

##########################################################################################################################

@app.route('/mysql/trefila/metas/custo/')
def trefilaMetasCusto(req: Request, res: Response):
    data = trefila.metas.custo()
    return res(
        dumps(data),
        mimetype='application/json',
        status=200
    )

##########################################################################################################################

@app.route('/mysql/trefila/metas/sucata/')
def trefilaMetasSucata(req: Request, res: Response):
    data = trefila.metas.sucata()
    return res(
        dumps(data),
        mimetype='application/json',
        status=200
    )

##########################################################################################################################

@app.route('/mysql/trefila/metas/cincos/')
def trefilaMetasCincoS(req: Request, res: Response):
    data = trefila.metas.cincos()
    return res(
        dumps(data),
        mimetype='application/json',
        status=200
    )


#################################################################################################################################################

@app.route('/mysql/trefila/metas/')
def trefilaMetas(req: Request, res: Response):
    # Read Metas
    report = homerico.trefila.metas()
    # Append Metas
    try: report.update(trefila.metas.custo())
    except: pass
    try: report.update(trefila.metas.sucata())
    except: pass
    try: report.update(trefila.metas.cincos())
    except: pass
    try: # Utilizacao
        metaUtil = trefila.metas.utilizacao()
        # util trf dia
        utilTrefila = iba.read('UTIL')
        total = (
            utilTrefila.get('m01', {}).get('UTIL') +
            utilTrefila.get('m02', {}).get('UTIL') +
            utilTrefila.get('m03', {}).get('UTIL') +
            utilTrefila.get('m04', {}).get('UTIL') +
            utilTrefila.get('m05', {}).get('UTIL')
        )
        # update util
        metaUtil['utilizacao'].update({
            'dia': (total / 4) * 100
        })
        # update metas
        report.update(metaUtil)
    except: pass

    # Return Data
    return res(
        dumps(report),
        mimetype='application/json',
        status=200
    )

##########################################################################################################################

# Start Server
app.start()

# Keep Main Thread Alive
while True: pass

##########################################################################################################################
