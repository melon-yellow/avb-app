defmodule OpcSxWeb.PimsController do
  use OpcSxWeb, :controller

  defp fetch(module, fun, args) do
    try do
      data = apply(module, fun, args)
        |> OpcSx.Pims.read_node_value!
      {:ok, data}
    catch _, reason -> {:error, reason}
    end
  end

  defp handle(%{"id" => %{"ns" => ns, "s" => s}}) when
    is_number(ns) and (is_number(s) or is_binary(s)),
  do:
    fetch OpcSx.NodeId, :new!, [ns: ns, s: s]

  defp handle(_), do: {:error, "invalid parameters"}

  defp format({:ok, data}), do: %{ok: true, data: data}
  defp format({:error, reason}), do: %{ok: false, error: "#{reason}"}

  def read(conn, params), do:
    json conn, format handle(params)

end
