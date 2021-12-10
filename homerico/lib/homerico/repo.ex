defmodule HomericoApp.Repo do
  use Ecto.Repo,
    otp_app: :homerico,
    adapter: Ecto.Adapters.Postgres
end
