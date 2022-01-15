defmodule OpcSxWeb.PimsController do
  use OpcSxWeb, :controller

  defp api_format!({:ok, data}), do: %{done: true, data: data}
  defp api_format!({:error, reason}), do: %{done: false, error: "#{reason}"}

  defp read!(%{"id" => %{"ns" => ns, "s" => s}})
    when is_number(ns) and is_binary(s) do
    OpcSx.PimsClient.read(ns, s)
  end
  defp read!(_), do: {:error, "invalid parameters"}

  def read(conn, params), do:
    json conn, api_format!(read! params)

end
