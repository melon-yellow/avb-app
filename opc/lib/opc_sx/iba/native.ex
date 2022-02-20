import Unsafe.Handler

##########################################################################################################################

defmodule OpcSx.Iba.IoConfig do
  use Unsafe.Generator, handler: :bang!
  # use Rustler, otp_app: :opc_sx, crate: :io_config

  @unsafe [read: 0]

  def read_xml(_), do: :erlang.nif_error(:nif_not_loaded)
  def parse_config(_), do: :erlang.nif_error(:nif_not_loaded)

  def read do
    try do
      io = System.get_env("AVB_IBA_PDA_CONFIG_PATH")
        |> read_xml
        |> parse_config
      {:ok, io}
    catch _, reason -> {:error, reason}
    end
  end

end

##########################################################################################################################
