defmodule HomericoSxWeb.ReportsController do
  use HomericoSxWeb, :controller

  @atoms :functions
    |> HomericoSx.Reports.__info__
    |> Enum.map(&elem(&1, 0))

  @reports @atoms
    |> Enum.map(&Atom.to_string/1)

  defp throw_report!(valid) when valid, do: true
  defp throw_report!(_), do: throw "invalid report"

  defp report_function!(report) when report in @reports do
    atom = String.to_existing_atom report
    throw_report!(atom in @atoms)
    atom
  end
  defp report_function!(_), do: throw "invalid report"

  defp handle(report, params) when
    is_binary(report) and is_map(params)
  do
    try do
      fun = report_function! report
      data = apply HomericoSx.Reports, fun, [params]
      {:ok, data}
    catch _, reason -> {:error, reason}
    end
  end

  defp format({:ok, data}), do: %{ok: true, data: data}
  defp format({:error, reason}), do: %{ok: false, error: "#{reason}"}

  def read(conn, %{"report" => report} = params)
    when is_binary(report),
  do: json conn, format handle(report, params)

end
