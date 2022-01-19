
##########################################################################################################################
#                                                        AVB-APP                                                         #
##########################################################################################################################
#                                                                                                                        #
#                                                  HTTP Rest API AVB                                                     #
#                                              Multi-language API for AVB                                                #
#                                 ---------------- Python3 -- NodeJS ----------------                                    #
#                                                * Under Development *                                                   #
#                                       https://github.com/melon-yellow/avb-app                                          #
#                                                                                                                        #
##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################

# Imports
import os
import json
import flask

# Modules
from .modules import turno
from .modules import homerico
from .modules import rendimento
from .modules import produtividade

##########################################################################################################################

Request = flask.Request
Response = flask.Response

##########################################################################################################################

# Declare HTTP API
app = flask.Flask()

# Set API Port
app.listen(
    port=int(os.getenv('AVB_APP_PORT'))
)

#################################################################################################################################################

@app.route('/client/laminador/metas/')
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
        json.dumps(data),
        mimetype='application/json',
        status=200
    )

#################################################################################################################################################

@app.route('/client/trefila/metas/')
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
        json.dumps(report),
        mimetype='application/json',
        status=200
    )

#################################################################################################################################################

@app.route('/client/trefila/producao/')
def trefilaProducao(req: Request, res: Response):
    data = homerico.ProducaoLista(lista=2361)
    return res(
        json.dumps(data),
        mimetype='application/json',
        status=200
    )

#################################################################################################################################################

@app.route('/client/laminador/producao/')
def laminadorProducao(req: Request, res: Response):
    data = homerico.ProducaoLista(lista=1269)
    return res(
        json.dumps(data),
        mimetype='application/json',
        status=200
    )

#################################################################################################################################################

@app.route('/client/aciaria/rendimento/')
def aciariaRendimento(req: Request, res: Response):
    data = rendimento.aciaria()
    return res(
        json.dumps(data),
        mimetype='application/json',
        status=200
    )

#################################################################################################################################################

@app.route('/client/trefila/produtividade/')
def trefilaProdutividade(req: Request, res: Response):
    data = produtividade.trefila()
    return res(
        json.dumps(data),
        mimetype='application/json',
        status=200
    )

#################################################################################################################################################

@app.route('/client/laminador/escalaTurno/')
def laminadorEscalaTurno(req: Request, res: Response):
    data = turno.escala()
    return res(
        json.dumps(data),
        mimetype='application/json',
        status=200
    )

#################################################################################################################################################

# Start Server
app.start()

# Keep Main Thread Alive
py_misc.keepalive()

##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################
