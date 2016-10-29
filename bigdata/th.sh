#!/usr/bin/env bash
DATE=$(date +%Y-%m-%d -d "yesterday")

hdfs dfs -rm -r th/$DATE

hadoop jar /opt/hadoop/hadoop-streaming.jar \
    -D mapreduce.job.reduces=1 \
    -files hadoop_scripts \
    -input /user/sandello/logs/access.log.${DATE} \
    -output th/${DATE} \
    -mapper hadoop_scripts/th_mapper.py \
    -reducer hadoop_scripts/th_reducer.py
