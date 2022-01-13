defmodule OpcSx.IbaClient do
  use Agent

  @pid :opc_sx_iba_client_pid

  @config %{ns: 3, s: "V:0.3."}

  defp read_cert!(path), do: :opc_sx
    |> Application.app_dir("priv/certs/#{path}")
    |> File.read!

  defp cert_config!, do: [
    security_mode: 2,
    certificate: read_cert!("elixir-client_cert.der"),
    private_key: read_cert!("elixir-client_key.der")
  ]

  def start_link(_args) do
    try do
      {:ok, pid} = OpcUA.Client.start_link
      :ok = OpcUA.Client.set_config_with_certs pid, cert_config!()
      :ok = OpcUA.Client.connect_by_url pid, url: System.get_env("AVB_IBA_OPC_URL")
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
