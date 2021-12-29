defmodule HomericoSx.Reports do

  @reports (
    __MODULE__.__info__(:functions)
      |> Enum.map(&Atom.to_string elem(&1, 0))
      |> Enum.filter(&!String.contains?(&1, "!"))
  )

  def apply!(report, params) when
    is_map(params) and
    is_atom(report) and
    report in @reports
  do
    HomericoSx.Connect.config!
      |> &apply(__MODULE__, report, [&1, params])
  end

  def relatorioLista(
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

  def relatorioGerencialRegistro(
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

  def relatorioGerencialReport(
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

  def relatorioBoletim(
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

  def producaoLista(
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

  def relatorioOv(
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

  def relatorioInterrupcoes(
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
