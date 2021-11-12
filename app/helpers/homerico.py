
#################################################################################################################################################

# Imports
import copy
import datetime

# Modules
from ..services import homerico as network

#################################################################################################################################################

#string to number
def num(string: str, ptbr: bool = False):
    if string == '': return None
    string = string.replace(' ','')
    if ptbr:
        string = string.replace('.','')
        string = string.replace(',','.')
    return float(string)

#################################################################################################################################################

#csv to matrix
def matrix(
    txt: str,
    columnbreak: str = ';',
    linebreak: str = '\n'
):
    return list(
        map(
            lambda line: line.split(columnbreak),
            txt.split(linebreak)
        )
    )

#################################################################################################################################################

# Get Last Day Of Month
def LastDayOfMonth(date: datetime.datetime):
    if date.month == 12: return date.replace(day=31)
    return (
        date.replace(month=(date.month + 1), day=1) -
        datetime.timedelta(days=1)
    )

#################################################################################################################################################
#                                                       HOMERICO GETTERS                                                                        #
#################################################################################################################################################

# relatorio gerencial parser
def RelatorioGerencialReport(
    idReport: int,
    registros: dict[str, int] = dict(),
    data: str = None
):
    if data == None:
        data = datetime.date.today().strftime('%d/%m/%Y')
    _registros = copy.deepcopy(registros)
    # private map function
    def _replace_reg(row):
        if row[0] in list(_registros.values()):
            for reg in _registros: row[0] = (
                reg if (row[0] == _registros[reg]) else row[0]
            )
            _registros[row[0]] = dict(
                meta = num(row[1],True),
                dia = num(row[2],True),
                acumulado = num(row[3],True))
        else: return None
        return row
    # get function
    for i in _registros: _registros[i] = str(_registros[i])
    homerico_csv = network.RelatorioGerencialReport(
        data=data,
        idReport=str(idReport)
    )
    list(map(_replace_reg, matrix(homerico_csv)))
    null_reg = dict(meta=None, dia=None, acumulado=None)
    for item in list(_registros):
        _registros[item] = (
            copy.deepcopy(null_reg)
            if (type(_registros[item]) != dict)
            else _registros[item]
        )
    return copy.deepcopy(_registros)

#################################################################################################################################################

# relatorio gerencial
def RelatorioGerencialTrimestre(
    idReport: int,
    registros: dict[str, int] = dict(),
    data: str = None
):
    if data == None:
        data = datetime.date.today().strftime('%d/%m/%Y')
    timed = datetime.datetime.strptime(data, '%d/%m/%Y')
    report = RelatorioGerencialReport(
        idReport=idReport,
        registros=registros,
        data=data
    )
    qt = (3 * (1 + ((timed.month - 1) // 3)))
    m = [qt-2, qt-1, qt]
    for i in m:
        last_day = LastDayOfMonth(
            datetime.date(timed.year, i, 1)
        ).day
        if i == timed.month: last_day = timed.day
        _date = datetime.date(timed.year, i, last_day).strftime('%d/%m/%Y')
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
    if data == None:
        data = datetime.date.today().strftime('%d/%m/%Y')
    homerico_csv = network.RelatorioGerencialRegistro(
        data=data,
        registro=str(registro)
    )
    return matrix(homerico_csv)

#################################################################################################################################################

# producao lista
def ProducaoLista(
    lista: int,
    data: str = None
):
    if data == None:
        data = datetime.date.today()
    last_day = LastDayOfMonth(data).strftime('%d/%m/%Y')
    homerico_csv = network.ProducaoLista(
        dataFinal=last_day,
        controle=str(lista)
    )
    dados = matrix(homerico_csv)
    dados.pop(0)
    d = list()
    for item in dados:
        if len(item) != 3: dados.pop(dados.index(item))
    for item in dados:
        data = '{}{}'.format(item[0][:2].zfill(2), last_day[2:])
        d.append(dict(data=data, peso=num(item[2], True)))
    return d

#################################################################################################################################################
