
#################################################################################################################################################

# Imports
from os import getenv, path
from pandas import read_sql
from asyncio import gather
from datetime import datetime
from mysql.connector import connect

# Modules
from ..iba import read as fromIba
from .metas import getMetaDay, getMetaTrim, metaTrimParser, utilTrimParser
from ..homerico import trefila

#################################################################################################################################################

# Get File-Paths
fileDir = path.dirname(path.abspath(__file__))
s5_sql = path.abspath(path.join(fileDir, '../../sql/trefila.meta.5s.sql'))
custo_sql = path.abspath(path.join(fileDir, '../../sql/trefila.meta.custo.sql'))
sucata_sql = path.abspath(path.join(fileDir, '../../sql/trefila.meta.sucata.sql'))
util_sql = path.abspath(path.join(fileDir, '../../sql/trefila.meta.utilizacao.sql'))

##########################################################################################################################

class db:

    def iba():
        return connect(
            host=getenv('IBA_MYSQL_HOST'),
            user=getenv('IBA_MYSQL_USER'),
            passwd=getenv('IBA_MYSQL_PASSWORD'),
            port=getenv('IBA_MYSQL_PORT'),
            database=getenv('IBA_MYSQL_DATABASE')
        )

    def bot():
        return connect(
            host=getenv('BOT_MYSQL_HOST'),
            user=getenv('BOT_MYSQL_USER'),
            passwd=getenv('BOT_MYSQL_PASSWORD'),
            port=getenv('BOT_MYSQL_PORT'),
            database=getenv('BOT_MYSQL_DATABASE')
        )


##########################################################################################################################

def utilizacao():
    try:
        df = read_sql(
            open(util_sql).read(),
            db.iba()
        )
        csv = str(df.to_csv())
        # Return Data
        return (True, csv)
    except Exception as error:
        return (False, error)

#################################################################################################################################################

async def util_dia():
    try:
        [
            (ok1, u1),
            (ok2, u2),
            (ok3, u3),
            (ok4, u4),
            (ok5, u5)
        ] = await gather(
            fromIba('0:25'),
            fromIba('0:26'),
            fromIba('0:27'),
            fromIba('0:28'),
            fromIba('0:29')
        )
        # Check Response
        if not ok1: raise u1
        if not ok2: raise u2
        if not ok3: raise u3
        if not ok4: raise u4
        if not ok5: raise u5
        # Calc Total
        total: float = (u1 + u2 + u3 + u4 + u5)
        dia = (total / 4) * 100
        # Return Data
        return (True, dia)
    except Exception as error:
        return (False, error)

#################################################################################################################################################

# Metas Class
class metas:

    #################################################################################################################################################

    async def s5():
        try:
            sql = open(s5_sql).read()
            df = read_sql(sql, db.bot())
            # Datetime
            now = datetime.now()
            # Get Meta Parser
            day = getMetaDay(df, now)
            meta = getMetaTrim(df, now, metaTrimParser)
            meta.update({ 'meta': 90, 'dia': day })
            # Return Data
            return (True, meta)
        except Exception as error:
            return (False, error)

    #################################################################################################################################################

    async def custo():
        try: # Connect
            sql = open(custo_sql).read()
            df = read_sql(sql, db.bot())
            # Datetime
            now = datetime.now()
            # Get Meta Parser
            day = getMetaDay(df, now)
            meta = getMetaTrim(df, now, metaTrimParser)
            meta.update({ 'meta': 110, 'dia': day })
            # Return Data
            return (True, meta)
        except Exception as error:
            return (False, error)

    #################################################################################################################################################

    async def sucata():
        try:
            sql = open(sucata_sql).read()
            df = read_sql(sql, db.bot())
            # Datetime
            now = datetime.now()
            # Get Meta Parser
            day = getMetaDay(df, now)
            meta = getMetaTrim(df, now, metaTrimParser)
            meta.update({ 'meta': 3, 'dia': day })
            # Return Data
            return (True, meta)
        except Exception as error:
            return (False, error)

    #################################################################################################################################################

    async def utilizacao():
        try:
            sql = open(util_sql).read()
            df = read_sql(sql, db.iba())
            # Datetime
            now = datetime.now()
            # Update Shift
            df['DATA'] = df['DATA'].astype('str')
            # Assembly Data
            meta = getMetaTrim(df, now, utilTrimParser)
            # Get Util Trf Dia
            (ok, dia) = await util_dia()
            if not ok: raise dia
            meta.update({ 'meta': 60, 'dia': dia })
            # Return Data
            return (True, meta)
        except Exception as error:
            return (False, error)

##########################################################################################################################

async def all_metas():
    try:
        (
            (ok1, s5),
            (ok2, custo),
            (ok3, sucata),
            (ok4, outras),
            # (ok5, utilizacao)
        ) = await gather(
            metas.s5(),
            metas.custo(),
            metas.sucata(),
            trefila.metas(),
            # metas.utilizacao()
        )
        # Check Response
        if not ok1: raise s5
        if not ok2: raise custo
        if not ok3: raise sucata
        if not ok4: raise outras
        # if not ok5: raise utilizacao
        # Assembly Data
        data = {
            '5S': s5,
            'custo': custo,
            # 'utilizacao': utilizacao,
            'sucateamento': sucata
        }
        data.update(outras)
        # Return Data
        return (True, data)
    except Exception as error:
        return (False, error)

##########################################################################################################################
