#!/usr/bin/env bash
DATE=$(date +%Y-%m-%d -d "yesterday")

hdfs dfs -rm -r profile_hits/$DATE

cd /home/eignatenkov/shad_python/bigdata

hadoop jar /opt/hadoop/hadoop-streaming.jar \
    -D mapreduce.job.reduces=1 \
    -files hbase \
    -input /user/sandello/logs/access.log.${DATE} \
    -output profile_hits/${DATE} \
    -mapper hbase/profile_hits_mapper.py \
    -reducer hbase/profile_hits_reducer.py
