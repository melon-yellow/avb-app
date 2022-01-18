defmodule OpcSxWeb.PimsController do
  use OpcSxWeb, :controller

  defp fetch(%{"id" => %{"ns" => ns, "s" => s}})
  when is_number(ns) and (is_number(s) or is_binary(s)) do
    try do
      data = OpcSx.Utils.node_from!(ns: ns, s: s)
        |> OpcSx.PimsClient.read_node_value!
      {:ok, data}
    catch _, reason -> {:error, reason}
    end
  end
  defp fetch(_), do: {:error, "invalid parameters"}

  defp api_format!({:ok, data}), do: %{done: true, data: data}
  defp api_format!({:error, reason}), do: %{done: false, error: "#{Kernel.inspect reason}"}

  def read(conn, params), do:
    json conn, api_format!(fetch params)

end
