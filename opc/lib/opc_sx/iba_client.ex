defmodule OpcSx.IbaClient do
  use Agent

  @pid :opc_sx_iba_client_pid

  @config %{ns: 3, s: "V:0.3."}

  defp read_cert!(path), do:
    Application.app_dir :opc_sx, "priv/ca/#{path}"

  defp cert_config!, do: [
    security_mode: 2,
    certificate: read_cert!("ca.crt.der"),
    private_key: read_cert!("ca.key.der")
  ]

  def start_link(_args) do
    {:ok, pid} = OpcUA.Client.start_link
    # :ok = OpcUA.Client.set_config pid
    :ok = OpcUA.Client.set_config_with_certs pid, cert_config!()
    :ok = OpcUA.Client.connect_by_url pid, url: System.get_env("AVB_IBA_OPC_ADDRESS")
    Process.register pid, @pid
    {:ok, pid}
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
