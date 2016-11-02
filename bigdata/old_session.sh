#!/usr/bin/env bash
PREFIX="/user/sandello/logs/access.log."
for i in {26..19}
  do
    DATE=$(date +%Y-%m-%d -d "$i days ago")
    hdfs dfs -rm -r session/$DATE
    hadoop jar /opt/hadoop/hadoop-streaming.jar \
        -D stream.num.map.output.key.fields=2 \
        -D mapreduce.job.output.key.comparator.class=org.apache.hadoop.mapreduce.lib.partition.KeyFieldBasedComparator \
        -D mapred.text.key.comparator.options='-k 1,1 -k 2,2' \
        -D mapreduce.job.reduces=1 \
        -D mapreduce.job.maps=4 \
        -files hadoop_scripts \
        -input /user/sandello/logs/access.log.${DATE} \
        -output session/${DATE} \
        -mapper hadoop_scripts/session_mapper.py \
        -reducer hadoop_scripts/session_reducer.py
    echo "$DATE,$(hdfs dfs -cat session/${DATE}/part-00000 | python hadoop_scripts/session_aggs.py)" \
    >> "/home/eignatenkov/shad_python/bigdata/session_aggs.csv"
  done
