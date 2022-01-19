
#################################################################################################################################################

# Imports
import os
import requests
import pylixir as Elixir
from typing import TypedDict

#################################################################################################################################################

# Get Address
remote = os.getenv('OPC_SERVICE_ADDRESS')

#################################################################################################################################################

class NodeId(TypedDict):
    s:  int | str
    ns: int

#################################################################################################################################################

@Elixir.Safe
def read(
    tag: str = None,
    tagname: str = None,
    nid: 'NodeId' = None
) -> (bool | float | str):
    req = {}
    if nid: req.update({'id': nid})
    if tag: req.update({'tag': tag})
    if tagname: req.update({'tagname': tagname})
    # Request
    res = requests.post(
        url=f'{remote}/iba/read',
        json=req
    ).json()
    if not res['ok']:
        raise Exception(res['error'])
    return res['data']

#################################################################################################################################################
