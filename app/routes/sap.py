
#################################################################################################################################################

# Imports
import json
import flask
import py_misc

# modules
from ..services import odbc

#################################################################################################################################################

Request = flask.Request
Response = flask.Response

#################################################################################################################################################

# Load Routes
def __load__(app: py_misc.Express):

    ##########################################################################################################################

    @app.route('/avb/sap/preditivas/')
    def sapPreditivas(req: Request, res: Response):
        try:
            input = req.json()
            # Check Input
            if not isinstance(input, dict): raise Exception('bad request')
            if 'equip' not in input: raise Exception('invalid argument "equip"')
            # Get Data
            data = odbc.sap.preditivas(input['equip'])
            return res(
                json.dumps(data),
                mimetype='application/json',
                status=200
            )
        except Exception as e:
            return res(
                json.dumps({ 'error': str(e) }),
                mimetype='application/json',
                status=200
            )

#################################################################################################################################################
