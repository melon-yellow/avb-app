
##########################################################################################################################

defmodule HomericoSx.Reports do

  def relatorio_lista(
    %{"id_processo" => id_processo, "data_inicial" => data_inicial, "data_final" => data_final}
  ), do: Homerico.Reports.relatorio_lista! HomericoClient, id_processo, data_inicial, data_final

  def relatorio_gerencial_registro(
    %{"registro" => registro, "data" => data}
  ), do: Homerico.Reports.relatorio_gerencial_registro! HomericoClient, registro, data

  def relatorio_gerencial_report(
    %{"id_report" => id_report, "data" => data}
  ), do: Homerico.Reports.relatorio_gerencial_report! HomericoClient, id_report, data

  def relatorio_boletim(
    %{"id_report" => id_report, "data_inicial" => data_inicial,"data_final" => data_final}
  ), do: Homerico.Reports.relatorio_boletim! HomericoClient, id_report, data_inicial, data_final

  def producao_lista(
    %{"controle" => controle, "data_final" => data_final}
  ), do: Homerico.Reports.producao_lista! HomericoClient, controle, data_final

  def relatorio_ov(
    %{"id_processo_grupo" => id_processo_grupo, "data" => data}
  ), do: Homerico.Reports.relatorio_ov! HomericoClient, id_processo_grupo, data

  def relatorio_interrupcoes(
    %{"id_proceso" => id_processo, "data" => data}
  ), do: Homerico.Reports.relatorio_interrupcoes! HomericoClient, id_processo, data

end

##########################################################################################################################
