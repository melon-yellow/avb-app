defmodule OpcSxWeb.IbaController do
  use OpcSxWeb, :controller

  defp fetch(%{"id" => %{"ns" => ns, "s" => s}}) when
    is_number(ns) and (is_number(s) or is_binary(s))
  do
    try do
      data = OpcSx.NodeId.new!(ns: ns, s: s)
        |> OpcSx.Iba.read_node_value!
      {:ok, data}
    catch _, reason -> {:error, reason}
    end
  end
  defp fetch(%{"tag" => tag}) when is_binary(tag) do
    try do
      data = OpcSx.Iba.NodeId.from_tag!(tag)
        |> OpcSx.Iba.read_node_value!
      {:ok, data}
    catch _, reason -> {:error, reason}
    end
  end
  defp fetch(%{"tagname" => tagname}) when is_binary(tagname) do
    try do
      data = OpcSx.Iba.NodeId.from_tagname!(tagname)
        |> OpcSx.Iba.read_node_value!
      {:ok, data}
    catch _, reason -> {:error, reason}
    end
  end
  defp fetch(_), do: {:error, "invalid parameters"}

  defp api_format!({:ok, data}), do: %{ok: true, data: data}
  defp api_format!({:error, reason}), do: %{ok: false, error: "#{reason}"}

  def read(conn, params), do:
    json conn, api_format!(fetch params)

end
