#!/usr/bin/env bash
DATE=${1:-$(date +%Y-%m-%d -d "yesterday")}

hdfs dfs -rm -r session/$DATE

cd /home/eignatenkov/shad_python/bigdata

hadoop jar /opt/hadoop/hadoop-streaming.jar \
    -D stream.num.map.output.key.fields=2 \
    -D mapreduce.job.output.key.comparator.class=org.apache.hadoop.mapreduce.lib.partition.KeyFieldBasedComparator \
    -D mapreduce.partition.keypartitioner.options='-k1,1' \
    -D mapreduce.partition.keycomparator.options='-k1 -k2' \
    -files hadoop_scripts \
    -input /user/sandello/logs/access.log.${DATE} \
    -output session/${DATE} \
    -mapper hadoop_scripts/session_mapper.py \
    -reducer hadoop_scripts/session_reducer.py \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner

echo "$DATE,$(hdfs dfs -cat session/${DATE}/* | python hadoop_scripts/session_aggs.py)" \
>> "/home/eignatenkov/shad_python/bigdata/session_aggs.csv"
