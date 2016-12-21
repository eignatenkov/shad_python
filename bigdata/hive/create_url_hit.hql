use eignatenkov;
ADD JAR /opt/cloudera/parcels/CDH-5.9.0-1.cdh5.9.0.p0.23/lib/hive/lib/hive-contrib.jar;

CREATE TABLE urls_stat 
STORED AS TEXTFILE
AS
SELECT url, count(distinct ip) AS users, count(1) AS hits
FROM access_log
WHERE status='200'
GROUP BY url
ORDER BY hits DESC; 

