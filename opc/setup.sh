#!/bin/bash

priv/keygen/keygen.sh

mix deps.get
mix do compile --force

while true
do
    MIX_ENV=prod mix phx.server
done
