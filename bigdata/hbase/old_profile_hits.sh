#!/usr/bin/env bash
PREFIX="/user/sandello/logs/access.log."
cd ..
for i in {10..1}
  do
    DATE=$(date +%Y-%m-%d -d "$i days ago")
    hdfs dfs -rm -r profile_hits/$DATE
    hadoop jar /opt/hadoop/hadoop-streaming.jar \
        -files hbase \
        -input ${PREFIX}${DATE} \
        -output profile_hits/${DATE} \
        -mapper hbase/profile_hits_mapper.py \
        -reducer hbase/profile_hits_reducer.py
  done

