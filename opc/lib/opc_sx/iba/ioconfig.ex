
##########################################################################################################################

defmodule OpcSx.Iba.IoConfig do
  use Agent
  alias OpcSx.Iba.IoConfig.Get

  def start_link(init_arg) when is_list(init_arg), do:
    Agent.start_link Get, :config!, [], init_arg

end

##########################################################################################################################

defmodule OpcSx.Iba.IoConfig.Get do
  use Unsafe.Generator, handler: {Unsafe.Handler, :bang!}
  use Rustler, otp_app: :opc_sx, crate: :io_config

  @unsafe [read: 0]

  @address (
    "https://raw.githubusercontent.com" <>
    "/melon-yellow/avb-iba/main/pda/pda.config.io"
  )

  def parse(_xml), do: :erlang.nif_error(:nif_not_loaded)

  defp handle_http!({:ok, %{status_code: 200, body: body}}), do: body
  defp handle_http!({:ok, %{status_code: status}}), do: throw "http status: #{status}"
  defp handle_http!({:error, %{reason: reason}}), do: throw reason

  def get, do: @address
    |> HTTPoison.get
    |> handle_http!

  def config do
    try do {:ok, parse get}
    catch _, reason -> {:error, reason}
    end
  end

end

##########################################################################################################################
