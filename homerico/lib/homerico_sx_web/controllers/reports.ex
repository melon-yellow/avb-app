defmodule HomericoSxWeb.ReportsController do
  use HomericoSxWeb, :controller

  @reports (
    HomericoSx.Reports.__info__(:functions)
      |> Enum.map(&Atom.to_string elem(&1, 0))
      |> Enum.filter(&!String.contains?(&1, "!"))
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

  def handle(
    conn,
    %{"report" => report} = params
  ) when is_binary(report) do
    conn |> render("term.json",
      (apply! report, params)
    )
  end
end
