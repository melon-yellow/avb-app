
#################################################################################################################################################

# Imports
from os import getenv
from requests import post

#################################################################################################################################################

# Get Address
remote = getenv('OPC_SERVICE_ADDRESS')

#################################################################################################################################################

async def read(
    tag: str = None,
    tagname: str = None
):
    try:
        req = {}
        if tag: req.update({'tag': tag})
        if tagname: req.update({'tagname': tagname})
        # Request
        res = post(
            url=f'{remote}/iba/read',
            json=req
        ).json()
        # Check Return
        if not res['ok']: raise Exception(res['error'])
        # Return Data
        return (True, res['data'])
    except Exception as error:
        return (False, error)

#################################################################################################################################################
