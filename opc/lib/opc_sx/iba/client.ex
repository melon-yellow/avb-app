
##########################################################################################################################

defmodule OpcSx.Iba do
  use Unsafe.Generator, handler: {Unsafe.Handler, :bang!}

  @unsafe [read_node_value: 1]

  def read_node_value(nid), do:
    OpcUA.Client.read_node_value IbaClient, nid

end

##########################################################################################################################

defmodule OpcSx.Iba.Client do
  use OpcUA.Client, restart: :transient, shutdown: 10_000

  defp read_cert!(path), do: :opc_sx
    |> Application.app_dir("priv/certs/#{path}")
    |> File.read!

  def configuration(_user_init_state), do: [
    conn: [
      by_url: [url: System.get_env "AVB_IBA_OPC_URL"]
    ],
    config: [
      set_config_with_certs: [
        security_mode: 3,
        certificate: (read_cert! "elixir-client_cert.der"),
        private_key: (read_cert! "elixir-client_key.der")
      ],
      set_config: %{
        "requestedSessionTimeout" => 1200000,
        "secureChannelLifeTime" => 600000,
        "timeout" => 50000
      }
    ]
  ]

end

##########################################################################################################################

defmodule OpcSx.Iba.State do
  use Agent

  def start_link(init_arg) when is_list(init_arg), do:
    Agent.start_link OpcSx.Iba.IoConfig, :read!, [], init_arg

end

##########################################################################################################################

defmodule OpcSx.Iba.Supervisor do
  use Supervisor

  def start_link(init_arg) when is_list(init_arg) do
    Supervisor.start_link(__MODULE__, init_arg, name: __MODULE__)
  end

  @impl true
  def init(_init_arg) do
    children = [
      {OpcSx.Iba.Client, name: IbaClient},
      {OpcSx.Iba.State, name: IbaState}
    ]

    Supervisor.init(children, strategy: :one_for_one)
  end

end

##########################################################################################################################
