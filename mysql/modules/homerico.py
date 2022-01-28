
#################################################################################################################################################

# Imports
from os import getenv
from requests import get

#################################################################################################################################################

# Get Address
remote = getenv('CLIENT_SERVICE_ADDRESS')

#################################################################################################################################################

# Homerico Trefila Class
class trefila:

    #################################################################################################################################################

    async def metas():
        try:
            res = get(
                f'{remote}/trefila/metas/homerico/',
            ).json()
            # Check Response
            if not res['ok']:
                raise Exception(res['error'])
            # Return Data
            return (True, res['data'])
        except Exception as error:
            return (False, error)

#################################################################################################################################################
