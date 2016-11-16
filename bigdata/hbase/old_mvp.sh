#!/usr/bin/env bash
PREFIX="/user/sandello/logs/access.log."
cd ..
for i in {40..1}
  do
    DATE=$(date +%Y-%m-%d -d "$i days ago")
    hdfs dfs -rm -r user_mvp/$DATE
    hadoop jar /opt/hadoop/hadoop-streaming.jar \
        -files hbase \
        -input ${PREFIX}${DATE} \
        -output user_mvp/${DATE} \
        -mapper hbase/user_mvp_mapper.py \
        -reducer hbase/user_mvp_reducer.py
  done

