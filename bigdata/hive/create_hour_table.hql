use eignatenkov;
ADD JAR /opt/cloudera/parcels/CDH-5.9.0-1.cdh5.9.0.p0.23/lib/hive/lib/hive-contrib.jar;
DROP TABLE hour;

CREATE TABLE hour (
    hour SMALLINT
)
STORED AS TEXTFILE;

INSERT OVERWRITE TABLE hour
SELECT 
    hour(date)
FROM parsed_log;

