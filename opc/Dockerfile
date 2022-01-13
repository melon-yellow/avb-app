FROM elixir:1.13

# Set Envs
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Fortaleza
ENV LANG C.UTF-8

# Install git tz and build-base
RUN apt-get update -y
RUN apt install software-properties-common -y
RUN apt-get install -y build-essential automake autoconf cmake git libmbedtls-dev squashfs-tools ssh-askpass pkg-config curl apt-transport-https ca-certificates gnupg lsb-release libwxgtk3.0-gtk3-dev libssl-dev libncurses5-dev tzdata -y
RUN ln -sf /usr/lib/x86_64-linux-gnu/libmbedcrypto.so /usr/lib/x86_64-linux-gnu/libmbedcrypto.so.1

# Install Python KeyGen deps
RUN apt-get install python3-pip -y
RUN pip3 install netifaces

# Install deps.
RUN mix local.hex --force
RUN mix local.rebar --force

WORKDIR /usr/app
