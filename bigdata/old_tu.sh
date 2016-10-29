#!/usr/bin/env bash
PREFIX="/user/sandello/logs/access.log."
for i in {16..1}
  do
    DATE=$(date +%Y-%m-%d -d "$i days ago")
    hdfs dfs -rm -r tu/$DATE
    hadoop jar /opt/hadoop/hadoop-streaming.jar \
        -D mapreduce.job.reduces=1 \
        -files hadoop_scripts \
        -input /user/sandello/logs/access.log.${DATE} \
        -output tu/${DATE} \
        -mapper hadoop_scripts/tu_mapper.py \
        -reducer hadoop_scripts/tu_reducer.py
    echo "$DATE,$(hdfs dfs -cat tu/${DATE}/part-00000)" >> "/home/eignatenkov/shad_python/bigdata/unique_users.csv"
  done