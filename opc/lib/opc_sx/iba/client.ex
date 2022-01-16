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
      {:ok, _} = OpcSx.IbaClient.Daemon.start
      {:ok, pid}
    rescue reason -> {:error, reason}
    catch reason -> {:error, reason}
    end
  end

  defp set_node!(ns, s), do: OpcUA.NodeId.new(
    ns_index: ns, identifier_type: "string", identifier: s)

  defp read_node_value(node_id), do:
    OpcUA.Client.read_node_value @pid, node_id

  def read(ns, s) when is_number(ns) and is_binary(s), do:
    set_node!(ns, s) |> read_node_value

end

defmodule OpcSx.IbaClient.Daemon do

  @tag_prefix %{ns: 3, s: "V:0.3"}
  @tag_regex ~r/([0-9]+)((.|:){1})([0-9]+)/

  defp throw_tag!(valid) when valid, do: true
  defp throw_tag!(_), do: throw "invalid tag"

  defp check_tag!(text), do:
    text |> String.match?(@tag_regex) |> throw_tag!

  def node_from_tag(tag) when is_binary(tag) do
    try do
      check_tag! tag
      {dig, [mod, sig]} = case String.contains?(tag, ":") do
        true -> {"0", String.split(tag, ":")}
        false -> {"1", String.split(tag, ".")}
      end
      node = {
        @tag_prefix.ns,
        @tag_prefix.s <> ".#{mod}.#{dig}.#{sig}"
      }
      {:ok, node}
    rescue reason -> {:error, reason}
    catch reason -> {:error, reason}
    end
  end

  def node_from_tagname(tagname) when is_binary(tagname) do
    try do
      {:ok, nil}
    rescue reason -> {:error, reason}
    catch reason -> {:error, reason}
    end
  end

  def start do
    {:ok, pid} = OpcSx.IbaClient.State.start
    OpcSx.IbaClient.IoConfig.read
      |> OpcSx.IbaClient.State.set
    {:ok, self()}
  end

end

defmodule OpcSx.IbaClient.State do

  @pid :opc_sx_iba_io_config_pid

  defp loop(state) do
    receive do
      {:set, value} -> loop value
      {:get, caller} ->
        send caller, {@pid, state}
        loop state
    end
  end

  def start do
    {:ok, pid} = Task.start_link(fn -> loop nil end)
    Process.register pid, @pid
    {:ok, @pid}
  end

  def set(value) do
    send @pid, {:set, value}
  end

  def get do
    send @pid, {:get, self()}
    receive do {@pid, state} -> state end
  end

end
