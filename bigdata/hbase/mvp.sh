#!/usr/bin/env bash
DATE=$(date +%Y-%m-%d -d "yesterday")

hdfs dfs -rm -r user_mvp/$DATE

cd /home/eignatenkov/shad_python/bigdata

hadoop jar /opt/hadoop/hadoop-streaming.jar \
    -files hbase \
    -input /user/sandello/logs/access.log.${DATE} \
    -output user_mvp/${DATE} \
    -mapper hbase/user_mvp_mapper.py \
    -reducer hbase/user_mvp_reducer.py
