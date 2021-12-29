defmodule HomericoSxWeb.ReportsController do
  use HomericoSxWeb, :controller

  @reports (
    Homerico.Reports.__info__(:functions)
      |> Enum.map(&Atom.to_string elem(&1, 0))
      |> Enum.filter(&!String.contains?(&1, "!"))
  )

  def handle(
    conn,
    %{"report" => report} = params
  ) when report in @reports do
    report
      |> &String.to_existing_atom/1
      |> execute!(params)
  end

  defp execute!(report, params) when
    is_atom(report) and
    is_map(params)
  do
    apply(Homerico.Reports, report, args)
  end
end
