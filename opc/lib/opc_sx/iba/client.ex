import Unsafe.Handler

defmodule OpcSx.Iba.Client do
  use OpcUA.Client, restart: :transient, shutdown: 10_000
end

defmodule OpcSx.Iba do
  use Unsafe.Generator, handler: :bang!
  use GenServer

  @unsafe [read_node_value: 1]

  def start_link(_args) do
    try do
      {:ok, pid} = GenServer.start_link(__MODULE__, default)
      :ok = OpcUA.Client.set_config_with_certs IbaClient, cert_config!()
      :ok = OpcUA.Client.connect_by_url IbaClient, url: System.get_env("AVB_IBA_OPC_URL")
      {:ok, _} = OpcSx.Iba.Utils.start_link
      {:ok, pid}
    catch _, reason -> {:error, reason}
    end
  end

  def read_node_value(nid), do:
    OpcUA.Client.read_node_value IbaClient, nid

  defp read_cert!(path), do: :opc_sx
    |> Application.app_dir("priv/certs/#{path}")
    |> File.read!

  defp cert_config!, do: [
    security_mode: 3,
    certificate: read_cert!("elixir-client_cert.der"),
    private_key: read_cert!("elixir-client_key.der")
  ]

end
