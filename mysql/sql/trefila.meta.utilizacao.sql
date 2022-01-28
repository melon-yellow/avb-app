# Main Select Query
SELECT
	# General Info
	date_format(cte00._date, "%d-%m-%Y") AS 'DATA',
	# Maquina 02
	REPLACE(ROUND((cte16.TIME_TRF_02_SHIFT) / 864, 1),".",",") AS M2,
	# Maquina 03
	REPLACE(ROUND((cte16.TIME_TRF_03_SHIFT) / 864, 1),".",",") AS M3,
	# Maquina 04
	REPLACE(ROUND((cte16.TIME_TRF_04_SHIFT) / 592, 1),".",",") AS M4,
	# Maquina 05
	REPLACE(ROUND((cte16.TIME_TRF_05_SHIFT) / 864, 1),".",",") AS M5,
	# Utilizacao Global
	REPLACE(
		ROUND(
			((
				(cte16.TIME_TRF_02_SHIFT / 864) + 
				(cte16.TIME_TRF_03_SHIFT / 864) +
				(cte16.TIME_TRF_04_SHIFT / 592) +
				(cte16.TIME_TRF_05_SHIFT / 864)
			) / 4),
			1
		),
		".",
		","
	) AS GLOBAL

FROM
	(SELECT * FROM _sort_trf_util_2 WHERE TIME_PLC_TRF_SHIFT = 28800) AS cte00,
	(SELECT * FROM _sort_trf_util_2 WHERE TIME_PLC_TRF_SHIFT = 57600) AS cte08,
	(SELECT * FROM _sort_trf_util_2 WHERE TIME_PLC_TRF_SHIFT = 86400) AS cte16

WHERE 
	(cte00._date = cte08._date AND cte08._date = cte16._date)

ORDER BY cte00._date DESC;
