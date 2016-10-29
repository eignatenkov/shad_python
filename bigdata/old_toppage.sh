#!/usr/bin/env bash
PREFIX="/user/sandello/logs/access.log."
for i in {16..1}
  do
    DATE=$(date +%Y-%m-%d -d "$i days ago")
    hdfs dfs -rm -r toppage/$DATE
    hadoop jar /opt/hadoop/hadoop-streaming.jar \
        -D mapreduce.job.reduces=1 \
        -files hadoop_scripts \
        -input /user/sandello/logs/access.log.${DATE} \
        -output toppage/${DATE} \
        -mapper hadoop_scripts/toppage_mapper.py \
        -reducer hadoop_scripts/toppage_reducer.py
    echo "$DATE;$(hdfs dfs -cat toppage/${DATE}/part-00000 | sort -k 2,2nr -k 1,1 | head -10 | awk -F '\t' '{print $1}' | tr '\n' ',')" >> "/home/eignatenkov/shad_python/bigdata/top_pages.csv"
  done
