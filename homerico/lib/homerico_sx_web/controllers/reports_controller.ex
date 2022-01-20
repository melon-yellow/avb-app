defmodule HomericoSxWeb.ReportsController do
  use HomericoSxWeb, :controller

  @atoms :functions
    |> HomericoSx.Reports.__info__
    |> Enum.map(&elem(&1, 0))

  @reports @atoms
    |> Enum.map(&Atom.to_string/1)

  defp throw_report!(valid) when valid, do: true
  defp throw_report!(_), do: throw "invalid report"

  defp report_to_atom!(report) when report in @reports do
    report_atom = String.to_existing_atom report
    throw_report!(report_atom in @atoms)
    report_atom
  end
  defp report_to_atom!(_), do: throw "invalid report"

  defp fetch(report, params) when
    is_binary(report) and is_map(params)
  do
    try do
      data = apply HomericoSx.Reports,
        report_to_atom!(report),
        [HomericoSx.Connect.config, params]
      {:ok, data}
    catch _, reason -> {:error, reason}
    end
  end

  defp api_format!({:ok, data}), do: %{done: true, data: data}
  defp api_format!({:error, reason}), do: %{done: false, error: "#{reason}"}

  def handle(conn, %{"report" => report} = params)
    when is_binary(report), do: json conn,
      (report |> fetch(params) |> api_format!)

end
