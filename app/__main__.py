
##########################################################################################################################
#                                                        AVB-APP                                                         #
##########################################################################################################################
#                                                                                                                        #
#                                                  HTTP Rest API AVB                                                     #
#                                              Multi-language API for AVB                                                #
#                                 ---------------- Python3 -- NodeJS ----------------                                    #
#                                                * Under Development *                                                   #
#                                     https://github.com/anthony-freitas/avb-app                                         #
#                                                                                                                        #
##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################

# Imports
import os
import py_misc

# Services Interface
from .services import helpers
from .services import homerico
from .services import mysql
from .services import odbc
from .services import opc
from .services import oracle

# Routes
from . import routes

##########################################################################################################################

# Setup Homerico Connection
homerico.remote(
    address=os.getenv('HOMERICO_NETWORK_ADDRESS'),
    user=os.getenv('HOMERICO_NETWORK_USER'),
    password=os.getenv('HOMERICO_NETWORK_PASSWORD')
)

##########################################################################################################################

# Declare HTTP API
app = py_misc.Express()
app.port(
    int(os.getenv('AVB_APP_PORT'))
)

##########################################################################################################################

# Load Routes
routes.__load__(app)

##########################################################################################################################

# start server
app.start()

# keep main thread alive
py_misc.keepalive()

##########################################################################################################################
