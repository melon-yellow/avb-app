defmodule OpcSxWeb.Router do
  use OpcSxWeb, :router

  pipeline :api do
    plug :accepts, ["json"]
  end

  scope "/", OpcSxWeb do
    pipe_through :api

    post "/opc/iba/read", IbaController, :read
    post "/opc/pims/read", PimsController, :read
  end
end
