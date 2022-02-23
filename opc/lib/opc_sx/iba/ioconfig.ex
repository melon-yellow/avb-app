
##########################################################################################################################

defmodule OpcSx.Iba.IoConfig do
  use Agent
  alias OpcSx.Iba.IoConfig.Nif

  def start_link(init_arg) when is_list(init_arg), do:
    Agent.start_link Nif, :read!, [], init_arg

end

##########################################################################################################################

defmodule OpcSx.Iba.IoConfig.Nif do
  use Rustler, otp_app: :opc_sx, crate: :io_config

  @address (
    "https://raw.githubusercontent.com" <>
    "/melon-yellow/avb-iba/main/pda/pda.config.io"
  )

  def parse(_xml), do: :erlang.nif_error(:nif_not_loaded)

  defp handle_http!({:ok, %{status_code: 200, body: body}}), do: body
  defp handle_http!({:ok, %{status_code: status}}), do: throw "http status: #{status}"
  defp handle_http!({:error, %{reason: reason}}), do: throw reason

  defp get, do: @address
    |> HTTPoison.get
    |> handle_http!

  def read!, do:
    get() |> parse |> IO.inspect

end

##########################################################################################################################
