
##########################################################################################################################

# Imports
from os import getenv
from json import dumps
from flask import Request, Response
from py_misc.express import Express

# Modules
from .modules import turno
from .modules import homerico
from .modules import rendimento
from .modules import produtividade

##########################################################################################################################

# Declare HTTP API
app = Express()

# Set API Port
app.port(int(getenv('CLIENT_SERVICE_PORT')))

#################################################################################################################################################

@app.route('/laminador/metas/')
def laminadorMetas(req: Request, res: Response):
    data = homerico.RelatorioGerencialTrimestre(
        idReport=10,
        registros={
            'BLBP': 1444,
            'SUCATEAMENTO': 1350,
            'ACIDENTE CPT': 1333,
            'PROD LAMINADO': 1336,
            'REND. METALICO': 1338
        }
    )
    return res(
        dumps(data),
        mimetype='application/json',
        status=200
    )

#################################################################################################################################################

@app.route('/trefila/metas/')
def trefilaMetas(req: Request, res: Response):
    report = homerico.RelatorioGerencialTrimestre(
        idReport=16,
        registros={
            'PRODUÇÃO': 2962,
            'PRODUÇÃO HORÁRIA': 2966,
            'RENDIMENTO METÁLICO': 2963,
            'PRODUÇÃO POR MÁQUINA': 2988
        }
    )
    return res(
        dumps(report),
        mimetype='application/json',
        status=200
    )

#################################################################################################################################################

@app.route('/trefila/producao/')
def trefilaProducao(req: Request, res: Response):
    data = homerico.ProducaoLista(lista=2361)
    return res(
        dumps(data),
        mimetype='application/json',
        status=200
    )

#################################################################################################################################################

@app.route('/laminador/producao/')
def laminadorProducao(req: Request, res: Response):
    data = homerico.ProducaoLista(lista=1269)
    return res(
        dumps(data),
        mimetype='application/json',
        status=200
    )

#################################################################################################################################################

@app.route('/aciaria/rendimento/')
def aciariaRendimento(req: Request, res: Response):
    data = rendimento.aciaria()
    return res(
        dumps(data),
        mimetype='application/json',
        status=200
    )

#################################################################################################################################################

@app.route('/trefila/produtividade/')
def trefilaProdutividade(req: Request, res: Response):
    data = produtividade.trefila()
    return res(
        dumps(data),
        mimetype='application/json',
        status=200
    )

#################################################################################################################################################

@app.route('/laminador/escala/')
def laminadorEscalaTurno(req: Request, res: Response):
    data = turno.escala()
    return res(
        dumps(data),
        mimetype='application/json',
        status=200
    )

#################################################################################################################################################

# Start Server
app.start()

# Keep Main Thread Alive
while True: pass

##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################
