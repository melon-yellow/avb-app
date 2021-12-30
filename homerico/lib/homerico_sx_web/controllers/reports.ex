defmodule HomericoSxWeb.ReportsController do
  use HomericoSxWeb, :controller

  @reports HomericoSx.Reports.__info__(:functions)

  def handle(
    conn,
    %{ "report" => report } = params
  ) when is_binary(report) do
    String.to_existing_atom(report)
      |> apply!(params)
  end

  defp apply!(report, params) when
    is_map(params) and
    is_atom(report) and
    report in @reports
  do
    apply(HomericoSx.Reports, report, [
      HomericoSx.Connect.config!,
      params
    ])
  end
end
