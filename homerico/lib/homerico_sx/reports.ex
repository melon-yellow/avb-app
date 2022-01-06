defmodule HomericoSx.Reports do

  def relatorio_lista(
    %Homerico.Connect.Config{} = config,
    %{"id_processo" => id_processo, "data_inicial" => data_inicial, "data_final" => data_final}
  ), do: Homerico.Reports.relatorio_lista! config, id_processo, data_inicial, data_final

  def relatorio_gerencial_registro(
    %Homerico.Connect.Config{} = config,
    %{"registro" => registro, "data" => data}
  ), do: Homerico.Reports.relatorio_gerencial_registro! config, registro, data

  def relatorio_gerencial_report(
    %Homerico.Connect.Config{} = config,
    %{"id_report" => id_report, "data" => data}
  ), do: Homerico.Reports.relatorio_gerencial_report! config, id_report, data

  def relatorio_boletim(
    %Homerico.Connect.Config{} = config,
    %{"id_report" => id_report, "data_inicial" => data_inicial,"data_final" => data_final}
  ), do: Homerico.Reports.relatorio_boletim! config, id_report, data_inicial, data_final

  def producao_lista(
    %Homerico.Connect.Config{} = config,
    %{"controle" => controle, "data_final" => data_final}
  ), do: Homerico.Reports.producao_lista! config, controle, data_final

  def relatorio_ov(
    %Homerico.Connect.Config{} = config,
    %{"id_processo_grupo" => id_processo_grupo, "data" => data}
  ), do: Homerico.Reports.relatorio_ov! config, id_processo_grupo, data

  def relatorio_interrupcoes(
    %Homerico.Connect.Config{} = config,
    %{"id_proceso" => id_processo, "data" => data}
  ), do: Homerico.Reports.relatorio_interrupcoes! config, id_processo, data

end
