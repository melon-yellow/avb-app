defmodule HomericoSx.Reports do

  @reports (
    Homerico.Reports.__info__(:functions)
      |> Enum.map(&Atom.to_string elem(&1, 0))
      |> Enum.filter(&!String.contains?(&1, "!"))
  )

  def apply!(report, params) when
    is_map(params) and
    is_atom(report) and
    report in @reports
  do
    apply(
      HomericoSx.Reports,
      report,
      params
    )
  end

  defp relatorio_lista(
    %Homerico.Connect.Config{} = config,
    %{
      "idProcesso" => id_processo,
      "dataInicial" => data_inicial,
      "dataFinal" => data_final
    }
  ) do
    config |> Homerico.Reports.relatorio_lista(
      id_processo,
      data_inicial,
      data_final
    )
  end

  defp relatorio_gerencial_registro(
    %Homerico.Connect.Config{} = config,
    %{
      "registro" => registro,
      "data" => data
    }
  ) do
    config |> Homerico.Reports.relatorio_gerencial_registro(
      registro,
      data
    )
  end

  defp relatorio_gerencial_report(
    %Homerico.Connect.Config{} = config,
    %{
      "idReport" => id_report,
      "data" => data
    }
  ) do
    config |> Homerico.Reports.relatorio_gerencial_report(
      id_report,
      data
    )
  end

  defp relatorio_boletim(
    %Homerico.Connect.Config{} = config,
    %{
      "idReport" => id_report,
      "dataInicial" => data_inicial,
      "dataFinal" => data_final
    }
  ) do
    config |> Homerico.Reports.relatorio_boletim(
      id_report,
      data_inicial,
      data_final
    )
  end

  defp producao_lista(
    %Homerico.Connect.Config{} = config,
    %{
      "controle" => controle,
      "dataFinal" => data_final
    }
  ) do
    config |> Homerico.Reports.relatorio_boletim(
      controle,
      data_final
    )
  end

  defp relatorio_ov(
    %Homerico.Connect.Config{} = config,
    %{
      "idProcessoGrupo" => id_processo_grupo,
      "data" => data
    }
  ) do
    config |> Homerico.Reports.relatorio_ov(
      id_processo_grupo,
      data
    )
  end

  defp relatorio_interrupcoes(
    %Homerico.Connect.Config{} = config,
    %{
      "idProceso" => id_processo,
      "data" => data
    }
  ) do
    config |> Homerico.Reports.relatorio_interrupcoes(
      id_processo,
      data
    )
  end
end
