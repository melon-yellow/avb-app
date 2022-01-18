defmodule HomericoSxWeb.ReportsController do
  use HomericoSxWeb, :controller

  @report_atoms (:functions
    |> HomericoSx.Reports.__info__
    |> Enum.map(&elem(&1, 0))
  )
  @reports (@report_atoms
    |> Enum.map(&Atom.to_string/1)
  )

  defp report_to_atom!(report) when report in @reports do
    _ = @report_atoms # Force Atoms into Context
    String.to_existing_atom report
  end
  defp report_to_atom!(_), do: throw "report not found"

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
      (fetch(report, params) |> api_format!)

end
