
##########################################################################################################################

defmodule OpcSx.Iba.IoConfig do
  use Unsafe.Generator, handler: {Unsafe.Handler, :bang!}
  use Rustler, otp_app: :opc_sx, crate: :io_config
  alias OpcSx.Iba.IoConfig.Network

  @unsafe [read: 0]

  def parse(_), do: :erlang.nif_error(:nif_not_loaded)

  def read do
    try do
      io = Network.get |> parse()
      {:ok, io}
    catch _, reason -> {:error, reason}
    end
  end

end

##########################################################################################################################

defmodule OpcSx.Iba.IoConfig.Network do

  @request Finch.build(:get,
    "https://raw.githubusercontent.com" <>
    "/melon-yellow/avb-iba/main/pda/pda.config.io"
  )

  defp handle_http!({:ok, %{status_code: 200, body: body}}), do: handle_data!(body)
  defp handle_http!({:ok, %{status_code: 404}}), do: throw "(404) could not reach the link"
  defp handle_http!({:error, %{reason: reason}}), do: throw reason

  def get, do: @request
    |> Finch.request(HTTPClient)
    |> handle_http!()

end

##########################################################################################################################
