defmodule OpcSx.PimsClient do
  use Agent

  @pid :opc_sx_pims_client_pid

  @config %{ns: 2, s: ""}

  def start_link(_args) do
    try do
      {:ok, pid} = OpcUA.Client.start_link
      :ok = OpcUA.Client.set_config pid
      :ok = OpcUA.Client.connect_by_url pid, url: System.get_env("AVB_PIMS_OPC_ADDRESS")
      Process.register pid, @pid
      {:ok, pid}
    rescue reason -> {:error, reason}
    catch reason -> {:error, reason}
    end
  end

  defp set_node!(id), do: %OpcUA.NodeId{
    ns_index: @config.ns,
    identifier_type: "string",
    identifier: @config.s <> id
  }

  defp read_node_value!(node_id), do:
    OpcUA.Client.read_node_value @pid, node_id

  def read(id) when is_binary(id), do:
    id |> set_node! |> read_node_value!

end
