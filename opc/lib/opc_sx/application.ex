defmodule OpcSx.Application do
  # See https://hexdocs.pm/elixir/Application.html
  # for more information on OTP Applications
  @moduledoc false

  use Application

  @impl true
  def start(_type, _args) do
    children = [
      # Start the Telemetry supervisor
      OpcSxWeb.Telemetry,
      # Start the PubSub system
      {Phoenix.PubSub, name: OpcSx.PubSub},
      # Start the Endpoint (http/https)
      OpcSxWeb.Endpoint
      # Start a worker by calling: OpcSx.Worker.start_link(arg)
      # {OpcSx.Worker, arg}
      {OpcSx.Iba.Supervisor, []},
      {OpcSx.Pims.Supervisor, []},
    ]

    # See https://hexdocs.pm/elixir/Supervisor.html
    # for other strategies and supported options
    opts = [strategy: :one_for_one, name: OpcSx.Supervisor]
    Supervisor.start_link(children, opts)
  end

  # Tell Phoenix to update the endpoint configuration
  # whenever the application is updated.
  @impl true
  def config_change(changed, _new, removed) do
    OpcSxWeb.Endpoint.config_change(changed, removed)
    :ok
  end
end
