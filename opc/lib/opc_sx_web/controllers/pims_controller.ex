defmodule OpcSxWeb.PimsController do
  use OpcSxWeb, :controller

  defp read!(%{"id" => %{"ns" => ns, "s" => s}})
  when is_number(ns) and (s_number(s) or is_binary(s)) do
    try do
      data = OpcSx.Utils.node_from!(ns: ns, s: s)
        |> OpcSx.PimsClient.read_node_value!
      {:ok, data}
    catch _, reason -> {:error, reason}
    end
  end
  defp read!(_), do: {:error, "invalid parameters"}

  defp api_format!({:ok, data}), do: %{done: true, data: data}
  defp api_format!({:error, reason}), do: %{done: false, error: "#{reason}"}

  def read(conn, params), do:
    json conn, api_format!(read! params)

end
