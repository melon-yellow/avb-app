SELECT
    coalesce(ATUAL_HORA_PESO,0) AS ATUAL_HORA_PESO,
    coalesce(ULTIMA_HORA_PESO,0) AS ULTIMA_HORA_PESO,
    coalesce(PESO_TOTAL,0) AS PESO_TOTAL,
    coalesce(ROUND((ATUAL_HORA_PESO+(ATUAL_HORA_PESO/(extract(minute from systimestamp)))*(60-extract(minute from systimestamp))),2),0) AS RITIMO_HORA,
    ROUND((PESO_TOTAL+(PESO_TOTAL/TEMPO_ATUAL)*TEMPO_RESTANTE),1) AS RITIMO_DIA,
    ROUND(PESO_TOTAL*3600/TEMPO_ATUAL,1) AS VAZAO_MEDIA,
    coalesce(ROUND(ATUAL_HORA_PESO*60/(extract(minute from systimestamp)),2),0) AS VAZAO_INST,
    ROUND(QTD_PECAS*3600/TEMPO_ATUAL,1) AS VAZAO2_M_HORA,
    ROUND(ATUAL_HORA_PECAS/(extract(minute from systimestamp)),1) AS VAZAO2_H_MINUTO,
    QTD_PECAS, ATUAL_HORA_PECAS, ULTIMA_HORA_PECAS
FROM
    (SELECT
        to_number(to_char(sysdate,'sssss')) AS TEMPO_ATUAL,
        (86400 - to_number(to_char(sysdate,'sssss'))) AS TEMPO_RESTANTE,
        to_timestamp(to_char((systimestamp - extract(minute from systimestamp)/24/60 - extract(second from systimestamp)/24/60/60),'YYYY-MM-DD hh24:mi:ss'),'YYYY-MM-DD HH24:MI:SS') as HORA_ATUAL,
        to_timestamp(to_char((systimestamp - extract(minute from systimestamp)/24/60 - extract(second from systimestamp)/24/60/60 -1/24),'YYYY-MM-DD hh24:mi:ss'),'YYYY-MM-DD HH24:MI:SS') as ULTIMA_HORA
    FROM dual
    ),
    (select SUM(measured_weight*0.967)/1000 AS ATUAL_HORA_PESO from fladc04 where to_timestamp(to_char(discharge_time, 'YYYY-MM-DD HH24:MI:SS'), 'YYYY-MM-DD HH24:MI:SS') > to_timestamp(to_char((systimestamp - extract(minute from systimestamp)/24/60 - extract(second from systimestamp)/24/60/60),'YYYY-MM-DD hh24:mi:ss'),'YYYY-MM-DD HH24:MI:SS')),
    (select SUM(measured_weight*0.967)/1000 AS ULTIMA_HORA_PESO from fladc04 where to_timestamp(to_char(discharge_time, 'YYYY-MM-DD HH24:MI:SS'), 'YYYY-MM-DD HH24:MI:SS') between to_timestamp(to_char((systimestamp - extract(minute from systimestamp)/24/60 - extract(second from systimestamp)/24/60/60 -1/24+1/24/60/60),'YYYY-MM-DD hh24:mi:ss'),'YYYY-MM-DD HH24:MI:SS') and to_timestamp(to_char((systimestamp - extract(minute from systimestamp)/24/60 - extract(second from systimestamp)/24/60/60),'YYYY-MM-DD hh24:mi:ss'),'YYYY-MM-DD HH24:MI:SS')),
    (select sum(measured_weight*0.967)/1000 as PESO_TOTAL from fladc04 where to_char(discharge_time, 'YYYY-MM-DD') = to_char(sysdate,'YYYY-MM-DD')),
    (select COUNT(measured_weight) as QTD_PECAS from fladc04 where to_char(discharge_time, 'YYYY-MM-DD') = to_char(sysdate,'YYYY-MM-DD')),
    (select COUNT(measured_weight) as ATUAL_HORA_PECAS from fladc04 where to_timestamp(to_char(discharge_time, 'YYYY-MM-DD HH24:MI:SS'), 'YYYY-MM-DD HH24:MI:SS') > to_timestamp(to_char((systimestamp - extract(minute from systimestamp)/24/60 - extract(second from systimestamp)/24/60/60),'YYYY-MM-DD hh24:mi:ss'),'YYYY-MM-DD HH24:MI:SS')),
    (select COUNT(measured_weight) as ULTIMA_HORA_PECAS from fladc04 where to_timestamp(to_char(discharge_time, 'YYYY-MM-DD HH24:MI:SS'), 'YYYY-MM-DD HH24:MI:SS') between to_timestamp(to_char((systimestamp - extract(minute from systimestamp)/24/60 - extract(second from systimestamp)/24/60/60 -1/24+1/24/60/60),'YYYY-MM-DD hh24:mi:ss'),'YYYY-MM-DD HH24:MI:SS') and to_timestamp(to_char((systimestamp - extract(minute from systimestamp)/24/60 - extract(second from systimestamp)/24/60/60),'YYYY-MM-DD hh24:mi:ss'),'YYYY-MM-DD HH24:MI:SS')
)
