DROP VIEW IF EXISTS temp_in_out_diff;

CREATE VIEW temp_in_out_diff AS
SELECT 
    DATE_TRUNC('day', noted_date) AS dia,
    AVG(CASE WHEN "out/in" = 'In'  THEN temp END) AS "temperatura interna",
    AVG(CASE WHEN "out/in" = 'Out' THEN temp END) AS "temperatura externa",
    (AVG(CASE WHEN "out/in" = 'Out' THEN temp END) -
     AVG(CASE WHEN "out/in" = 'In'  THEN temp END)) AS "diferenca temperatura"
FROM temperature_readings
GROUP BY DATE_TRUNC('day', noted_date)
HAVING COUNT(CASE WHEN "out/in" = 'In' THEN 1 END) > 0
   AND COUNT(CASE WHEN "out/in" = 'Out' THEN 1 END) > 0;
