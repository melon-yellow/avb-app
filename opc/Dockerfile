FROM elixir:1.13

# Run as Root
USER root

# Set Envs
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Fortaleza
ENV LANG C.UTF-8

# Install git tz and build-base
RUN apt-get update -y
#RUN apt-get install -y sudo software-properties-common \
#    build-essential automake autoconf cmake git python3-pip \
#    libmbedtls-dev squashfs-tools ssh-askpass pkg-config \
#    curl apt-transport-https ca-certificates gnupg lsb-release \
#    libwxgtk3.0-gtk3-dev libssl-dev libncurses5-dev tzdata
#
#RUN ln -sf /usr/lib/x86_64-linux-gnu/libmbedcrypto.so \
#    /usr/lib/x86_64-linux-gnu/libmbedcrypto.so.1
#
## Install Python KeyGen deps
#RUN pip3 install netifaces
#
## Install deps.
#RUN mix local.hex --force
#RUN mix local.rebar --force
#
## Install Rust
#RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
#RUN echo 'source $HOME/.cargo/env' >> $HOME/.bashrc

# Creates an unprivileged user
RUN groupadd container
RUN adduser user --group container -h /home/user --shell /bin/sh
RUN chown -R user /home/user
USER user

# Go to Workdir
WORKDIR /usr/app
