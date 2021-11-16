declare @DATA as datetime
set @DATA = getdate() - 3

SELECT
    Elements.LinkAnalyses as 'ID',
    convert(varchar(10), analyses.Anadatetime, 103) AS data,
    convert(varchar(10), analyses.Anadatetime, 108) AS hora,
    origem.value as 'Origem',
    tipo_aço.Value as 'Tipo Aço', 
    {}
    substring(Attributes.Value, 1, 7) AS Corrida,
    Attributes.Value AS Corrida_Completa,
    turma.value as 'Turma',
    DisplayName.Name as 'Elemento',
    CASE
    WHEN DisplayName.Name like 'N' then Elements.Value * 10000
    ELSE Elements.Value
    end as 'Dados'

FROM
    Elements (nolock)
    INNER JOIN DisplayName (nolock) ON
    DisplayName.ID = Elements.LinkName
    INNER JOIN Analyses (nolock) ON
    Analyses.ID = Elements.LinkAnalyses
    INNER JOIN Attributes (nolock) ON
    Attributes.LinkAnalyses = Elements.LinkAnalyses and
    Attributes.LinkName = 4
    INNER JOIN Attributes origem (nolock) ON
    origem.LinkAnalyses = Elements.LinkAnalyses and
    origem.LinkName = 15
    INNER JOIN Attributes tipo_aço (nolock) ON
    tipo_aço.LinkAnalyses = Elements.LinkAnalyses and
    tipo_aço.LinkName = {}
    INNER JOIN Attributes turma (nolock) ON
    turma.LinkAnalyses = Elements.LinkAnalyses and
    turma.LinkName = 18
    {}

WHERE
    DisplayName.Name in ('P') and
    Attributes.Value like '%%' and
    anadatetime >= @DATA

ORDER BY analyses.Anadatetime DESC