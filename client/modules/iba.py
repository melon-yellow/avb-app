
#################################################################################################################################################

# Imports
from os import getenv
from requests import post
from py_misc import elixir

#################################################################################################################################################

# Get Address
remote = getenv('OPC_SERVICE_ADDRESS')

#################################################################################################################################################

@elixir.Safe
def read(
    tag: str = None,
    tagname: str = None
) -> (bool | float | str):
    req = {}
    if tag: req.update({'tag': tag})
    if tagname: req.update({'tagname': tagname})
    # Request
    res = post(
        url=f'{remote}/iba/read',
        json=req
    ).json()
    if not res['ok']:
        raise Exception(res['error'])
    return res['data']

#################################################################################################################################################
