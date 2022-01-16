defmodule OpcSx.IbaClient do
  use Agent

  @pid :opc_sx_iba_client_pid

  defp read_cert!(path), do: :opc_sx
    |> Application.app_dir("priv/certs/#{path}")
    |> File.read!

  defp cert_config!, do: [
    security_mode: 3,
    certificate: read_cert!("elixir-client_cert.der"),
    private_key: read_cert!("elixir-client_key.der")
  ]

  def start_link(_args) do
    try do
      {:ok, pid} = OpcUA.Client.start_link
      true = Process.register pid, @pid
      :ok = OpcUA.Client.set_config_with_certs pid, cert_config!()
      :ok = OpcUA.Client.connect_by_url pid, url: System.get_env("AVB_IBA_OPC_URL")
      {:ok, _} = OpcSx.IbaClient.Daemon.start_link
      {:ok, pid}
    catch _, reason -> {:error, reason}
    end
  end

  def read_node_value(nid), do:
    OpcUA.Client.read_node_value @pid, nid

end
