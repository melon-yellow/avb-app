#!/bin/bash

WSGI=app:app
BIND=0.0.0.0:$ODBC_SERVICE_PORT

pip install -r requirements.txt
cd ..

while true
do
    gunicorn "$WSGI" -b "$BIND"
done
