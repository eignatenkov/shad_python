#!/usr/bin/env bash
PREFIX="/user/sandello/logs/access.log."
for i in {26..21}
  do
    DATE=$(date +%Y-%m-%d -d "$i days ago")
    hdfs dfs -rm -r th/$DATE
    ADDRESS=$PREFIX$DATE
    hadoop jar /opt/hadoop/hadoop-streaming.jar \
    -D mapreduce.job.reduces=1 \
    -files hadoop_scripts \
    -input ${PREFIX}${DATE} \
    -output th/${DATE} \
    -mapper hadoop_scripts/th_mapper.py \
    -reducer hadoop_scripts/th_reducer.py

    echo "$DATE,$(hdfs dfs -cat th/${DATE}/part-00000)" >> "/home/eignatenkov/shad_python/bigdata/total_hits.csv"
  done
