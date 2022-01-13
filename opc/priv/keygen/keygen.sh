#!/bin/bash

NAME=elixir-client
URI=urn:unconfigured:application

SCRIPT=priv/keygen/create-self-signed.py
SIZE=2048
DEST=priv/certs
CA=priv/certs/localhost.crt

if [ ! -f "$CA" ]
then
    python3 "$SCRIPT" "$DEST" -u "$URI" -k "$SIZE" -c "$NAME"
fi

cp "$CA" /usr/local/share/ca-certificates/
update-ca-certificates