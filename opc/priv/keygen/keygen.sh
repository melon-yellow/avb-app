#!/bin/bash

FILE=priv/certs/new.crt

if [ ! -f "$FILE" ]
then
    python3 priv/keygen/create-self-signed.py priv/certs
    cp priv/certs/new.crt /usr/local/share/ca-certificates/
    update-ca-certificates
fi