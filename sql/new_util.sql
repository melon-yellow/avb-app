SELECT
    ROUND(((UTIL/SEC)*100),1) AS UTIL,
    SEC,
    ROUND(((SEC-UTIL)/60),0) AS TEMPO_PARADO
FROM (
    SELECT
        ROUND(SUM(A._TIME),0) AS UTIL,
        DATEDIFF(SECOND,CONVERT(DATE,GETDATE()),GETDATE()) AS SEC
    FROM (
        SELECT (_Average*15) AS _TIME
        FROM [iba_db].[dbo].[VIEW_IBA_DAT]
        WHERE
            _Name = '{}'
        	AND YEAR(_TimeStamp) = YEAR(GETDATE())
        	AND MONTH(_TimeStamp) = MONTH(GETDATE())
        	AND DAY(_TimeStamp) = DAY(GETDATE())
    ) AS A
) AS B;
