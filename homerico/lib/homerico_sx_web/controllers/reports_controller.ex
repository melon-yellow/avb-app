defmodule HomericoSxWeb.ReportsController do
  use HomericoSxWeb, :controller

  @report_atoms (:functions
    |> HomericoSx.Reports.__info__
    |> Enum.map(&elem(&1, 0))
  )
  @reports (@report_atoms
    |> Enum.map(&Atom.to_string/1)
  )

  def handle(conn, %{"report" => report} = params)
    when is_binary(report), do: json conn,
      (apply!(report, params) |> api_format!)

  defp api_format!({:ok, data}), do: %{done: true, data: data}
  defp api_format!({:error, reason}), do:_%{done: false, error: reason}

  defp get_report!(report) when report in @reports, do:
    String.to_existing_atom report
  defp get_report!(_), do: throw "report not found"

  defp apply!(report, params)
    when is_binary(report) and is_map(params) do
    try do
      func = get_report! report
      args = [HomericoSx.Connect.config!, params]
      data = apply HomericoSx.Reports, func, args
      {:ok, data}
    rescue reason -> {:error, reason}
    catch reason -> {:error, reason}
    end
  end

end
