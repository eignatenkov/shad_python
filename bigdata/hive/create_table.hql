use eignatenkov;
ADD JAR /opt/cloudera/parcels/CDH-5.9.0-1.cdh5.9.0.p0.23/lib/hive/lib/hive-contrib.jar;
DROP TABLE parsed_text_log;

CREATE TABLE parsed_text_log (
    ip STRING,
    date STRING,
    url STRING,
    status SMALLINT,
    referer STRING,
    user_agent STRING
)
STORED AS TEXTFILE;

INSERT OVERWRITE TABLE parsed_text_log
SELECT 
    ip,
    date,
    url,
    CAST(status AS smallint),
    referer,
    user_agent
FROM access_log;

