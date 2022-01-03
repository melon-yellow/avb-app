defmodule HomericoSxWeb.ReportsController do
  use HomericoSxWeb, :controller

  @reports_raw (:functions
    |> HomericoSx.Reports.__info__
    |> Enum.map(&elem(&1, 0))
  )
  @reports (@reports_raw
    |> Enum.map(&Atom.to_string/1)
  )

  defp apply!(report, params) when
    is_map(params) and is_binary(report) and report in @reports
  do
    func = String.to_existing_atom report
    args = [HomericoSx.Connect.config!(), params]
    try do apply HomericoSx.Reports, func, args
    rescue _ -> "invalid arguments"
    catch _ -> "invalid arguments"
    end
  end

  defp apply!(report, params)
    when is_map(params) and is_binary(report), do:
      "report not found"

  def handle(conn, %{"report" => report} = params)
    when is_binary(report), do:
      html conn, (apply! report, params)

end
