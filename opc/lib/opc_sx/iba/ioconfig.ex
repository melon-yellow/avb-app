
##########################################################################################################################

defmodule OpcSx.Iba.IoConfig do
  use Unsafe.Generator, handler: {Unsafe.Handler, :bang!}
  use Rustler, otp_app: :opc_sx, crate: :io_config
  alias OpcSx.Iba.IoConfig.HTTP

  @unsafe [read: 0]

  def parse(_), do: :erlang.nif_error(:nif_not_loaded)

  def read do
    try do
      io = HTTP.get |> parse()
      {:ok, io}
    catch _, reason -> {:error, reason}
    end
  end

end

##########################################################################################################################

defmodule OpcSx.Iba.IoConfig.HTTP do
  @address (
    "https://raw.githubusercontent.com" <>
    "/melon-yellow/avb-iba/main/pda/pda.config.io"
  )

  defp handle_http!({:ok, %{status_code: 200, body: body}}), do: body
  defp handle_http!({:ok, %{status_code: status}}), do: throw "http status: #{status}"
  defp handle_http!({:error, %{reason: reason}}), do: throw reason

  def get, do: @address
    |> HTTPoison.get
    |> handle_http!

end

##########################################################################################################################
