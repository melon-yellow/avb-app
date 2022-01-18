import Unsafe.Handler

defmodule OpcSx.PimsClient do
  use Unsafe.Generator, handler: :bang!
  use Agent

  @unsafe [read_node_value: 1]

  @pid :opc_sx_pims_client_pid

  def start_link(_args) do
    try do
      {:ok, pid} = OpcUA.Client.start_link
      true = Process.register pid, @pid
      :ok = OpcUA.Client.set_config pid
      :ok = OpcUA.Client.connect_by_url pid, url: System.get_env("AVB_PIMS_OPC_ADDRESS")
      {:ok, pid}
    catch _, reason -> {:error, reason}
    end
  end

  def read_node_value(nid), do:
    OpcUA.Client.read_node_value @pid, nid

end
