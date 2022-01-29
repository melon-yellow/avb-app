import Unsafe.Handler

defmodule OpcSx.Pims.Client do
  use OpcUA.Client, restart: :transient, shutdown: 10_000
end

defmodule OpcSx.Pims do
  use Unsafe.Generator, handler: :bang!
  use GenServer

  @unsafe [read_node_value: 1]

  def start_link(_args) do
    try do
      {:ok, pid} = GenServer.start_link(__MODULE__, default)
      :ok = OpcUA.Client.set_config PimsClient
      :ok = OpcUA.Client.connect_by_url PimsClient, url: System.get_env("AVB_PIMS_OPC_ADDRESS")
      {:ok, pid}
    catch _, reason -> {:error, reason}
    end
  end

  def read_node_value(nid), do:
    OpcUA.Client.read_node_value PimsClient, nid

end
