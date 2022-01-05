defmodule OpcSxWeb.PimsController do
  use OpcSxWeb, :controller

  def read(conn, %{"identifier" => id}) when is_binary(id), do:
    json conn, OpcSx.IbaClient.read(id)
  def read(conn, _), do:
    json conn, %{error: "invalid parameters"}

end
