defmodule HomericoSxWeb.ReportsController do
  use HomericoSxWeb, :controller

  @reports (
    HomericoSx.Reports.__info__(:functions)
      |> Enum.map(&Atom.to_string elem(&1, 0))
      |> Enum.filter(&!String.contains?(&1, "!"))
  )

  def handle(
    _conn,
    %{"report" => report} = params
  ) when is_binary(report) do
    IO.inspect report
    IO.inspect @reports
    apply! report, params
  end

  defp apply!(report, params) when
    is_map(params) and
    is_binary(report) and
    report in @reports
  do
    args = [HomericoSx.Connect.config!, params]
    func = String.to_existing_atom report
    apply HomericoSx.Reports, func, args
  end
end
