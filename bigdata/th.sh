#!/usr/bin/env bash
hdfs dfs -rm -r th/2016-10-27

hadoop jar /opt/hadoop/hadoop-streaming.jar \
    -files th_mapper.py,th_reducer.py -input /user/sandello/logs/access.log.2016-10-27 -output th/2016-10-27 \
    -mapper th_mapper.py \
    -reducer th_reducer.py
