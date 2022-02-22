
##########################################################################################################################

defmodule OpcSx.Iba.IoConfig do
  use Unsafe.Generator, handler: {Unsafe.Handler, :bang!}
  use Rustler, otp_app: :opc_sx, crate: :io_config

  @unsafe [read: 0]

  @request Finch.build(:get,
    "https://raw.githubusercontent.com" <>
    "/melon-yellow/avb-iba/main/pda/pda.config.io"
  )

  defp read_xml, do:
    Finch.request @request, HTTPClient

  def parse_config(_), do: :erlang.nif_error(:nif_not_loaded)

  def read do
    try do
      io = read_xml |> parse_config
      {:ok, io}
    catch _, reason -> {:error, reason}
    end
  end

end

##########################################################################################################################
