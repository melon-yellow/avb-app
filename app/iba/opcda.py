
#################################################################################################################################################

# Imports
import os
import json
import requests

#################################################################################################################################################

# Get Data From PDA Server
def tag(tagname: str | list[str]):
    # Check for input Variable
    if (not isinstance(tagname, str) and
        not isinstance(tagname, list)
        ): return dict(error='tagname missing')

    try: # Request PDA Server
        res = requests.post(
            json={ 'tagname': tagname },
            url=os.getenv('AVB_APP_IBA_ENDNODE'),
            auth=(
                os.getenv('AVB_APP_IBA_USER'),
                os.getenv('AVB_APP_IBA_PASSWORD')
            )
        )
        res = json.loads(res.text)
    except: # If Server Not Responding
        res = dict(value=None, name=None, status='server down')

    # Return data
    return res

#################################################################################################################################################
