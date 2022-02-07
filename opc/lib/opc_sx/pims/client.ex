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

  def start_link(init_arg) when is_list(init_arg) do
    try do
      {:ok, pid} = OpcUA.Client.start_link(__MODULE__, init_arg)
      :ok = OpcUA.Client.set_config pid
      :ok = OpcUA.Client.connect_by_url pid, url: System.get_env("AVB_PIMS_OPC_ADDRESS")
      {:ok, pid}
    catch _, reason -> {:error, reason}
    end
  end

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
