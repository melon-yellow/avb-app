defmodule HomericoSxWeb.ReportsController do
  use HomericoSxWeb, :controller

  def handle(
    conn,
    %{ "report" => report } = params
  ) when is_binary(report) do
    report
      |> &String.to_existing_atom/1
      |> HomericoSx.Reports.apply!(params)
  end
end
