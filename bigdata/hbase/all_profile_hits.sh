#!/usr/bin/env bash

hdfs dfs -rm -r profile_hits/all

cd /home/eignatenkov/shad_python/bigdata

hadoop jar /opt/hadoop/hadoop-streaming.jar \
    -files hbase \
    -input /user/sandello/logs \
    -output profile_hits/all \
    -mapper hbase/profile_hits_mapper.py \
    -reducer hbase/profile_hits_reducer.py
