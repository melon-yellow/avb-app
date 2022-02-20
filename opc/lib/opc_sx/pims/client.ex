import Unsafe.Handler

##########################################################################################################################

defmodule OpcSx.Pims do
  use Unsafe.Generator, handler: :bang!

  @unsafe [read_node_value: 1]

  def read_node_value(nid), do:
    OpcUA.Client.read_node_value PimsClient, nid

end

##########################################################################################################################

defmodule OpcSx.Pims.Client do
  use OpcUA.Client, restart: :transient, shutdown: 10_000

  def configuration(_user_init_state), do: [
    conn: [
      by_url: [url: System.get_env "AVB_PIMS_OPC_URL"]
    ],
    config: [
      set_config: %{
        "requestedSessionTimeout" => 1200000,
        "secureChannelLifeTime" => 600000,
        "timeout" => 50000
      }
    ]
  ]

end

##########################################################################################################################

defmodule OpcSx.Pims.Supervisor do
  use Supervisor

  def start_link(init_arg) when is_list(init_arg) do
    Supervisor.start_link(__MODULE__, init_arg, name: __MODULE__)
  end

  @impl true
  def init(_init_arg) do
    children = [
      # {OpcSx.Pims.Client, name: PimsClient},
    ]

    Supervisor.init(children, strategy: :one_for_one)
  end

end

##########################################################################################################################
