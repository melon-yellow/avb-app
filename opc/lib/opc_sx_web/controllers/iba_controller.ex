defmodule OpcSxWeb.IbaController do
  use OpcSxWeb, :controller

  defp read!(%{"id" => %{"ns" => ns, "s" => s}})
  when is_number(ns) and (is_number(s) or is_binary(s)) do
    try do
      data = OpcSx.Utils.node_from!(ns: ns, s: s)
        |> OpcSx.IbaClient.read_node_value!
      {:ok, data}
    catch _, reason -> {:error, reason}
    end
  end
  defp read!(%{"tag" => tag}) when is_binary(tag) do
    try do
      data = OpcSx.IbaClient.Utils.node_from_tag!(tag)
        |> OpcSx.IbaClient.read_node_value!
      {:ok, data}
    catch _, reason -> {:error, reason}
    end
  end
  defp read!(%{"tagname" => tagname}) when is_binary(tagname) do
    try do
      data = OpcSx.IbaClient.Utils.node_from_tagname!(tagname)
        |> OpcSx.IbaClient.read_node_value!
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
