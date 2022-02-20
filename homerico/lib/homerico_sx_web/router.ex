defmodule HomericoSxWeb.Router do
  use HomericoSxWeb, :router

  pipeline :api do
    plug :accepts, ["json"]
  end

  scope "/", HomericoSxWeb do
    pipe_through :api

    post "/reports/:report", ReportsController, :read
  end
end
