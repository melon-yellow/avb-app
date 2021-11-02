
#################################################################################################################################################

# Imports
import os
import json
import requests

#################################################################################################################################################

# Get data from PIMS
def tag(tagname: str | list[str]):
    # Check for input Variable
    if (not isinstance(tagname, str) and
        not isinstance(tagname, list)
        ): return dict(error='tagname missing')

    try: # Request PIMS Server
        res = requests.post(
            json={ 'tagname': tagname },
            url=os.getenv('AVB_APP_PIMS_ENDNODE'),
            auth=(
                os.getenv('AVB_APP_PIMS_USER'),
                os.getenv('AVB_APP_PIMS_PASSWORD')
            )
        )
        res = json.loads(res.text)
    except: # If Server Not Responding
        res = dict(value=None, name=None, status='server down')

    # Return data
    return res

#################################################################################################################################################
