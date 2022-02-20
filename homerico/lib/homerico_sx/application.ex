defmodule HomericoSx.Application do
  # See https://hexdocs.pm/elixir/Application.html
  # for more information on OTP Applications
  @moduledoc false

  use Application

  @impl true
  def start(_type, _args) do
    children = [
      # Start the Telemetry supervisor
      HomericoSxWeb.Telemetry,
      # Start the PubSub system
      {Phoenix.PubSub, name: HomericoSx.PubSub},
      # Start the Endpoint (http/https)
      HomericoSxWeb.Endpoint
      # Start a worker by calling: HomericoSx.Worker.start_link(arg)
      # {HomericoSx.Worker, arg}
      {HomericoSx.Client, name: HomericoClient}
    ]

    # See https://hexdocs.pm/elixir/Supervisor.html
    # for other strategies and supported options
    opts = [strategy: :one_for_one, name: HomericoSx.Supervisor]
    Supervisor.start_link(children, opts)
  end

  # Tell Phoenix to update the endpoint configuration
  # whenever the application is updated.
  @impl true
  def config_change(changed, _new, removed) do
    HomericoSxWeb.Endpoint.config_change(changed, removed)
    :ok
  end
end
