#!/bin/bash

WSGI=app.wsgi:app
BIND=0.0.0.0:$ORACLE_SERVICE_PORT

pip install -r requirements.txt
cd ..

while true
do
    gunicorn "$WSGI" -b "$BIND"
done
