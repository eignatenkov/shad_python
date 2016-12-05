#!/usr/bin/env bash
PREFIX="/user/sandello/logs/access.log."
for i in {7..5}
  do
    DATE=$(date +%Y-%m-%d -d "$i days ago")
    hdfs dfs -rm -r daily_user/$DATE

    hadoop jar /opt/hadoop/hadoop-streaming.jar \
        -D mapreduce.job.reduces=1 \
        -files hadoop_scripts \
        -input /user/sandello/logs/access.log.${DATE} \
        -output daily_user/${DATE} \
        -mapper hadoop_scripts/tu_mapper.py \
        -reducer hadoop_scripts/daily_user_reducer.py

  done
