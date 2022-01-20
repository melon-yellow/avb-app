
#################################################################################################################################################

# Imports
from copy import deepcopy
from datetime import datetime, date

# Modules
from .reports import reports
from ..helpers import num, matrix, lastDayOfMonth

#################################################################################################################################################
#                                                       HOMERICO GETTERS                                                                        #
#################################################################################################################################################

# relatorio gerencial parser
def RelatorioGerencialReport(
    idReport: int,
    registros: dict[str, int] = {},
    data: str = None
):
    # get Inputs
    if data == None:
        data = date.today().strftime('%d/%m/%Y')
    _registros = deepcopy(registros)

    # Private Map Function
    def _replace_reg(row):
        if row[0] in list(_registros.values()):
            for reg in _registros:
                row[0] = reg if (row[0] == _registros[reg]) else row[0]
            _registros.update({
                row[0]: {
                    'meta': num(row[1], True),
                    'dia': num(row[2], True),
                    'acumulado': num(row[3], True)
                }
            })
        else: return None
        return row

    # Turn to String
    for i in _registros:
        _registros[i] = str(_registros[i])
    
    # Get Data
    csv = reports.relatorio_gerencial_report(
        data=data,
        id_report=str(idReport)
    )
    list(map(_replace_reg, matrix(csv)))

    # Fix Wrong Data
    for item in list(_registros):
        _registros[item] = (
            _registros[item]
            if isinstance(_registros[item], dict)
            else {
                'meta': None,
                'dia': None,
                'acumulado': None
            }
        )
    
    # Return Data
    return _registros

#################################################################################################################################################

# relatorio gerencial
def RelatorioGerencialTrimestre(
    idReport: int,
    registros: dict[str, int] = dict(),
    data: str = None
):
    if data == None:
        data = date.today().strftime('%d/%m/%Y')
    timed = datetime.strptime(data, '%d/%m/%Y')
    report = RelatorioGerencialReport(
        idReport=idReport,
        registros=registros,
        data=data
    )
    qt = (3 * (1 + ((timed.month - 1) // 3)))
    m = [qt-2, qt-1, qt]
    for i in m:
        last_day = lastDayOfMonth(
            date(timed.year, i, 1)
        ).day
        if i == timed.month: last_day = timed.day
        _date = date(timed.year, i, last_day).strftime('%d/%m/%Y')
        e = RelatorioGerencialReport(
            idReport=idReport,
            registros=registros,
            data=_date
        )
        for item in report:
            mes = 'mes{}'.format(i-qt+3)
            report[item][mes] = e[item]['acumulado']
    return report

#################################################################################################################################################

# relatorio gerencial
def RelatorioGerencialRegistro(
    registro: int,
    data: str = None
):
    if data == None: data = date.today().strftime('%d/%m/%Y')
    csv = reports.relatorio_gerencial_registro(
        data=data,
        registro=str(registro)
    )
    return matrix(csv)

#################################################################################################################################################

# producao lista
def ProducaoLista(
    lista: int,
    data: str = None
):
    if data == None: data = date.today()
    last_day = lastDayOfMonth(data).strftime('%d/%m/%Y')
    csv = reports.producao_lista(
        data_final=last_day,
        controle=str(lista)
    )
    dados = matrix(csv)
    dados.pop(0)
    d = list()
    for item in dados:
        if len(item) != 3: dados.pop(dados.index(item))
    for item in dados:
        data = '{}{}'.format(item[0][:2].zfill(2), last_day[2:])
        d.append({
            'data': data,
            'peso': num(item[2], True)
        })
    return d

#################################################################################################################################################
