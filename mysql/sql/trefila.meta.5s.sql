SELECT *
FROM metas
WHERE (
    (YEAR(data_msg) = 2022) AND
    (nome_meta = "5S")
)