#!/bin/bash

NAME=elixir-client
CA=priv/certs/localhost.crt

if [ ! -f "$CA" ]
then
    python3 priv/keygen/create-self-signed.py priv/certs -c "$NAME"
    cp "$CA" /usr/local/share/ca-certificates/
    update-ca-certificates
fi