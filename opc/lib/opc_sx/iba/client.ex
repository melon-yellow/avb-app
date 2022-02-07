import Unsafe.Handler

##########################################################################################################################

defmodule OpcSx.Iba do
  use Unsafe.Generator, handler: :bang!

  @unsafe [read_node_value: 1]

  def read_node_value(nid), do:
    OpcUA.Client.read_node_value IbaClient, nid

  defp cert!(path), do: :opc_sx
    |> Application.app_dir("priv/certs/#{path}")
    |> File.read!

  def config do
    try do
      config = [
        security_mode: 3,
        certificate: cert!("elixir-client_cert.der"),
        private_key: cert!("elixir-client_key.der")
      ]
      {:ok, config}
    catch _, reason -> {:error, reason}
    end
  end

end

##########################################################################################################################

defmodule OpcSx.Iba.Client do
  use OpcUA.Client, restart: :transient, shutdown: 10_000

  def start_link(init_arg) when is_list(init_arg) do
    try do
      {:ok, config} = OpcSx.Iba.config
      {:ok, pid} = OpcUA.Client.start_link(__MODULE__, init_arg)
      :ok = OpcUA.Client.set_config_with_certs pid, config
      :ok = OpcUA.Client.connect_by_url pid, url: System.get_env("AVB_IBA_OPC_URL")
      {:ok, pid}
    catch _, reason -> {:error, reason}
    end
  end

end

##########################################################################################################################

defmodule OpcSx.Iba.State do
  use SimpleState

  def start_link(_init_arg) do
    try do
      {:ok, config} = OpcSx.Iba.IoConfig.read
      SimpleState.start_link(__MODULE__, value: config)
    catch _, reason -> {:error, reason}
    end
  end

end

##########################################################################################################################

defmodule OpcSx.Iba.Supervisor do
  use Supervisor

  def start_link(init_arg) when is_list(init_arg) do
    Supervisor.start_link(__MODULE__, init_arg, name: __MODULE__)
  end

  @impl true
  def init(_init_arg) do
    children = [
      {OpcSx.Iba.Client, name: IbaClient},
      {OpcSx.Iba.State, name: IbaState}
    ]

    Supervisor.init(children, strategy: :one_for_one)
  end

end

##########################################################################################################################
