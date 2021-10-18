SELECT
    coalesce((ROUND(SUM(TEMPO),0)),1) AS OCC_SEC,
    DATEDIFF(SECOND, CONVERT(DATE,GETDATE()), GETDATE()) AS ATUAL_SEC
FROM
(
SELECT _Name, _Average, _MAX, _MIN,
CASE
	WHEN _Average = 0 AND _Name = 'STD01_TP_OCCU' THEN 0
   WHEN _Average = 1 AND _Name = 'STD01_TP_OCCU'  THEN 15
	WHEN _Average > 0 AND _Name = 'STD01_TP_OCCU'  AND _Average <> 1  THEN _Average * 15
	WHEN (_MAX - _MIN) <> 0 AND _Name = 'MILL - ROLLED COUNT' THEN (_MAX - _MIN) * 10
	ELSE 0
END AS TEMPO
FROM (
    SELECT *
    FROM
        [iba_db].[dbo].[VIEW_IBA_DAT] INNER JOIN
        (SELECT _FileId as ID
        FROM [iba_db].[dbo].[VIEW_IBA_DAT]
        WHERE
            _Name = 'STD01 M_ACT' AND
            _MAX > 10 AND
            YEAR(_TimeStamp) = YEAR(GETDATE()) AND
            MONTH(_TimeStamp) = MONTH(GETDATE()) AND
            DAY(_TimeStamp) = DAY(GETDATE())
        ) AS A
        ON A.ID = [iba_db].[dbo].[VIEW_IBA_DAT]._FileId
    ) AS B
) AS C
