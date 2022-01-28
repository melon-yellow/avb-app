
#################################################################################################################################################

# Imports
from typing import TypedDict
from asyncio import gather
from datetime import date

# Modules
from .reports import reports
from ..helpers import num, matrix, lastDayOfMonth

#################################################################################################################################################

class MetaMes(TypedDict):
    meta: float
    dia: float
    acumulado: float

#################################################################################################################################################

def set_report_replace(registros: dict[int, str]):
    def replacer(item: tuple[str, int]) -> dict[str, 'MetaMes']:
        if not item[0].isdigit(): return {}
        if int(item[0]) not in registros: return {}
        return {
            registros[int(item[0])]: {
                'meta': num(item[1]),
                'dia': num(item[2]),
                'acumulado': num(item[3])
            }
        }
    return replacer

#################################################################################################################################################

async def relatorio_gerencial_report(
    idReport: int,
    registros: dict[int, str] = {},
    data: date = date.today()
):
    try:
        (ok, csv) = reports.relatorio_gerencial_report(
            data=data.strftime('%d/%m/%Y'),
            id_report=str(idReport)
        )
        if not ok: raise csv
        # Set Replace
        replace = set_report_replace(registros)
        items: dict[str, 'MetaMes'] = {}
        items.update({key:None for key in registros.values()})
        # Map Items
        for item in matrix(csv):
            items.update(replace(item))
        # Return Data
        return (True, items)
    except Exception as error:
        return (False, error)

#################################################################################################################################################

class MetaTrim(TypedDict):
    meta: float
    dia: float
    mes1: float
    mes2: float
    mes3: float

#################################################################################################################################################

def last_date(data: date, month: int):
    return lastDayOfMonth(
        date(data.year, month, 1)
    )

#################################################################################################################################################

def trim_dates(data: date):
    qt = (3 * (1 + ((data.month - 1) // 3)))
    return (
        (2 + data.month - qt),
        (
            last_date(data, qt-2),
            last_date(data, qt-1),
            last_date(data, qt)
        )
    )

#################################################################################################################################################

async def relatorio_gerencial_trimestre(
    idReport: int,
    registros: dict[int, str] = dict(),
    data: date = date.today()
):
    try:
        (offset, dates) = trim_dates(data)
        get_report = (lambda d: relatorio_gerencial_report(
            idReport=idReport, registros=registros, data=d
        ))
        # Get Reports
        (
            (ok1, mes1),
            (ok2, mes2),
            (ok3, mes3)
        ) = await gather(
            get_report(dates[0]),
            get_report(dates[1]),
            get_report(dates[2])
        )
        # Check Response
        if not ok1: raise mes1
        if not ok2: raise mes2
        if not ok3: raise mes3
        # Update Data
        items: dict[str, 'MetaTrim'] = {}
        items.update((mes1, mes2, mes3)[offset])
        # Get Month Metas
        for item in items:
            items[item].pop('acumulado')
            items[item].update({
                'mes1': mes1[item].get('acumulado'),
                'mes2': mes2[item].get('acumulado'),
                'mes3': mes3[item].get('acumulado')
            })
        # Return Data
        return (True, items)
    except Exception as error:
        return (False, error)

#################################################################################################################################################

async def relatorio_gerencial_registro(
    registro: int,
    data: date = date.today()
):
    try:
        (ok, csv) = reports.relatorio_gerencial_registro(
            data=data.strftime('%d/%m/%Y'),
            registro=str(registro)
        )
        if not ok: raise csv
        # Get Data
        dat = matrix(csv)
        # Return Data
        return (True, dat)
    except Exception as error:
        return (False, error)

#################################################################################################################################################

class Producao(TypedDict):
    data: str
    peso: float

#################################################################################################################################################

def set_prod_replacer(postfix: str):
    def replacer(item: list[str]) -> 'Producao':
        if len(item) != 3: return
        return {
            'data': f'{item[0][:2].zfill(2)}{postfix}',
            'peso': num(item[2])
        }
    return replacer

#################################################################################################################################################

async def producao_lista(
    lista: int,
    data: date = date.today()
):
    try:
        last = lastDayOfMonth(data)
        (ok, csv) = reports.producao_lista(
            data_final=last.strftime('%d/%m/%Y'),
            controle=str(lista)
        )
        if not ok: raise csv
        # Assembly Data
        replace = set_prod_replacer(
            last.strftime("%d/%m/%Y")[2:]
        )
        items = matrix(csv)
        items.pop(0)
        dat: list['Producao'] = []
        # Map Days of Month
        for item in items:
            prod = replace(item)
            if prod: dat.append(prod)
        # Return Data
        return (True, dat)
    except Exception as error:
        return (False, error)

#################################################################################################################################################
