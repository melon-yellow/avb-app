defmodule HomericoSxWeb.ReportsController do
  use HomericoSxWeb, :controller

  @reports_raw (
    HomericoSx.Reports.__info__(:functions)
      |> Enum.map(&elem(&1, 0))
  )
  @reports (
    @reports_raw
      |> Enum.map(&Atom.to_string &1)
  )

  defp apply!(report, params) when
    is_map(params) and
    is_binary(report) and
    report in @reports
  do
    args = [HomericoSx.Connect.config!, params]
    func = String.to_existing_atom report
    apply HomericoSx.Reports, func, args
  end

  defp apply!(report, params) when
    is_map(params) and is_binary(report)
  do "report not found" end

  def handle(
    conn,
    %{"report" => report} = params
  ) when is_binary(report) do
    html conn, (apply! report, params)
  end
end
