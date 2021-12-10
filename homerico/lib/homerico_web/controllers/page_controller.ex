defmodule HomericoWeb.PageController do
  use HomericoWeb, :controller

  def index(conn, _params) do
    render(conn, "index.html")
  end
end
