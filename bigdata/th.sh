#!/usr/bin/env bash
DATE=${1:-$(date +%Y-%m-%d -d "yesterday")}
hdfs dfs -rm -r th/$DATE

cd /home/eignatenkov/shad_python/bigdata

hadoop jar /opt/hadoop/hadoop-streaming.jar \
    -D mapreduce.job.reduces=1 \
    -files hadoop_scripts \
    -input /user/sandello/logs/access.log.${DATE} \
    -output th/${DATE} \
    -mapper hadoop_scripts/th_mapper.py \
    -reducer hadoop_scripts/th_reducer.py

echo "$DATE,$(hdfs dfs -cat th/${DATE}/part-00000)" >> "/home/eignatenkov/shad_python/bigdata/total_hits.csv"
