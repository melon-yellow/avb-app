defmodule OpcSx.IbaClient do
  use Agent

  alias OpcUA.Client

  @pid :opc_sx_iba_client_pid

  @certs_config &Application.app_dir(:opc_sx, "priv/certificates/#{&1}")
    |> &[
      security_mode: 3,
      certificate: &1("iba-client-cert.der") |> File.read!,
      private_key: &1("iba-client-key.der") |> File.read!
    ]

  def pid!, do: @pid

  def start_link(_args) do
    {:ok, pid} = Client.start_link
    :ok = Client.set_config pid
    :ok = Client.connect_by_url pid, url: System.get_env("AVB_IBA_OPC_ADDRESS")
    Process.register pid, @pid
    {:ok, pid}
  end

end
