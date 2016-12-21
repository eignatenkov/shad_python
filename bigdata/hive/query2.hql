use eignatenkov;
ADD JAR /opt/cloudera/parcels/CDH-5.9.0-1.cdh5.9.0.p0.23/lib/hive/lib/hive-contrib.jar;
select from_unixtime(unix_timestamp(date ,'dd/MMM/yyyy:HH:mm:ss'), 'HH') as hour, count(*) as count_hits from access_log where status=200 group by from_unixtime(unix_timestamp(date ,'dd/MMM/yyyy:HH:mm:ss'), 'HH') sort by count_hits desc limit 10;

