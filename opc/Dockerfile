FROM rust:1.58-slim as rust

FROM elixir:1.13

# Set Envs
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Fortaleza
ENV LANG C.UTF-8

# Install git tz and build-base
RUN apt-get update -y
RUN apt-get install -y sudo software-properties-common \
    build-essential automake autoconf cmake git python3-pip \
    libmbedtls-dev squashfs-tools ssh-askpass pkg-config \
    curl apt-transport-https ca-certificates gnupg lsb-release \
    libwxgtk3.0-gtk3-dev libssl-dev libncurses5-dev tzdata \
    gcc libc6-dev make wget

RUN ln -sf /usr/lib/x86_64-linux-gnu/libmbedcrypto.so \
    /usr/lib/x86_64-linux-gnu/libmbedcrypto.so.1

ENV RUSTUP_HOME=/usr/local/rustup
ENV CARGO_HOME=/usr/local/cargo
ENV PATH=/usr/local/cargo/bin:$PATH

COPY --from=rust /usr/local/cargo /usr/local/cargo
COPY --from=rust /usr/local/rustup /usr/local/rustup
RUN rm -Rf _build

# Install Python KeyGen deps
RUN pip3 install netifaces

# Install deps.
RUN mix local.hex --force
RUN mix local.rebar --force

# Go to Workdir
WORKDIR /usr/app