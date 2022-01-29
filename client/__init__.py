
##########################################################################################################################

# Imports
from json import dumps
from flask import Flask, Response

# Modules
from .modules.turno import escala
from .modules.aciaria import rendimento
from .modules.trefila import produtividade
from .modules.homerico import producao_lista, relatorio_gerencial_trimestre

##########################################################################################################################

# Declare WSGI APP
app = Flask('app_client')

#################################################################################################################################################

@app.route('/laminador/metas/')
async def laminadorMetas():
    (ok, data) = await relatorio_gerencial_trimestre(
        idReport=10,
        registros={
            1444: 'BLBP',
            1350: 'SUCATEAMENTO',
            1333: 'ACIDENTE CPT',
            1336: 'PROD LAMINADO',
            1338: 'REND. METALICO'
        }
    )
    res = (
        {'ok': True, 'data': data} if ok else
        {'ok': False, 'error': f'{data}'}
    )
    return Response(
        dumps(res),
        mimetype='application/json',
        status=200
    )

#################################################################################################################################################

@app.route('/trefila/metas/homerico/')
async def trefilaMetasHomerico():
    (ok, data) = await relatorio_gerencial_trimestre(
        idReport=16,
        registros={
            2962: 'PRODUÇÃO',
            2966: 'PRODUÇÃO HORÁRIA',
            2963: 'RENDIMENTO METÁLICO',
            2988: 'PRODUÇÃO POR MÁQUINA'
        }
    )
    res = (
        {'ok': True, 'data': data} if ok else
        {'ok': False, 'error': f'{data}'}
    )
    return Response(
        dumps(res),
        mimetype='application/json',
        status=200
    )

#################################################################################################################################################

@app.route('/trefila/producao/')
async def trefilaProducao():
    (ok, data) = await producao_lista(lista=2361)
    res = (
        {'ok': True, 'data': data} if ok else
        {'ok': False, 'error': f'{data}'}
    )
    return Response(
        dumps(res),
        mimetype='application/json',
        status=200
    )

#################################################################################################################################################

@app.route('/laminador/producao/')
async def laminadorProducao():
    (ok, data) = await producao_lista(lista=1269)
    res = (
        {'ok': True, 'data': data} if ok else
        {'ok': False, 'error': f'{data}'}
    )
    return Response(
        dumps(res),
        mimetype='application/json',
        status=200
    )

#################################################################################################################################################

@app.route('/aciaria/rendimento/')
async def aciariaRendimento():
    (ok, data) = await rendimento()
    res = (
        {'ok': True, 'data': data} if ok else
        {'ok': False, 'error': f'{data}'}
    )
    return Response(
        dumps(res),
        mimetype='application/json',
        status=200
    )

#################################################################################################################################################

@app.route('/trefila/produtividade/')
async def trefilaProdutividade():
    (ok, data) = await produtividade()
    res = (
        {'ok': True, 'data': data} if ok else
        {'ok': False, 'error': f'{data}'}
    )
    return Response(
        dumps(res),
        mimetype='application/json',
        status=200
    )

#################################################################################################################################################

@app.route('/laminador/escala/')
def laminadorEscalaTurno():
    (ok, data) = escala()
    res = (
        {'ok': True, 'data': data} if ok else
        {'ok': False, 'error': f'{data}'}
    )
    return Response(
        dumps(res),
        mimetype='application/json',
        status=200
    )

#################################################################################################################################################
