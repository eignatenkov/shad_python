#!/usr/bin/env bash
DATE=$(date +%Y-%m-%d -d "yesterday")

hdfs dfs -rm -r tu_hbase/$DATE

cd /home/eignatenkov/shad_python/bigdata

hadoop jar /opt/hadoop/hadoop-streaming.jar \
    -files hbase \
    -input /user/sandello/logs/access.log.${DATE} \
    -output tu_hbase/${DATE} \
    -mapper hbase/tu_hbase_mapper.py \
    -reducer hbase/tu_hbase_reducer.py
