defmodule OpcSxWeb.PimsController do
  use OpcSxWeb, :controller

  defp api_format!({:ok, data}), do: %{done: true, data: data}
  defp api_format!({:error, reason}), do: %{done: false, error: "#{reason}"}

  def read(conn, %{"identifier" => id}) when is_binary(id), do:
    json conn, api_format!(OpcSx.PimsClient.read id)
  def read(conn, _), do:
    json conn, %{error: "invalid parameters"}

end
