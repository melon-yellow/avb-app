defmodule HomericoSxWeb.Router do
  use HomericoSxWeb, :router

  pipeline :api do
    plug :accepts, ["json"]
  end

  scope "/", HomericoSxWeb do
    pipe_through :api

    post "/homerico/:report", ReportsController, :handle
  end

end
