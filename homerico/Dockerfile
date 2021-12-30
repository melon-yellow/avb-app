FROM elixir:1.13

# Install deps.
RUN mix local.hex --force
RUN mix local.rebar --force

WORKDIR /usr/app