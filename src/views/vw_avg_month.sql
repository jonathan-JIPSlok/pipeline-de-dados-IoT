DROP VIEW IF EXISTS vw_avg_month;

CREATE VIEW vw_avg_month AS
SELECT 
    DATE_TRUNC('month', noted_date) AS "mes",
    AVG(CASE WHEN "out/in" = 'In'  THEN temp END) AS "temperatura interna",
    AVG(CASE WHEN "out/in" = 'Out' THEN temp END) AS "temperatura externa"
FROM temperature_readings
GROUP BY DATE_TRUNC('month', noted_date)
HAVING COUNT(CASE WHEN "out/in" = 'In' THEN 1 END) > 0
   AND COUNT(CASE WHEN "out/in" = 'Out' THEN 1 END) > 0;
