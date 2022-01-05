FROM elixir:1.13

# Install git tz and build-base
RUN apt-get update

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Mexico_City

RUN apt-get install -y build-essential automake autoconf cmake git libmbedtls-dev squashfs-tools ssh-askpass pkg-config curl apt-transport-https ca-certificates gnupg lsb-release libwxgtk3.0-gtk3-dev libssl-dev libncurses5-dev tzdata
RUN ln -sf /usr/lib/x86_64-linux-gnu/libmbedcrypto.so /usr/lib/x86_64-linux-gnu/libmbedcrypto.so.1

# Install asdf 
RUN adduser --shell /bin/bash --home /asdf --disabled-password asdf
ENV PATH="${PATH}:/asdf/.asdf/shims:/asdf/.asdf/bin"

ENV LANG C.UTF-8

# Install deps.
RUN mix local.hex --force
RUN mix local.rebar --force

WORKDIR /usr/app
