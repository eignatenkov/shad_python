#!/usr/bin/env bash
DATE=$(date +%Y-%m-%d -d "yesterday")

hdfs dfs -rm -r liked/$DATE

cd /home/eignatenkov/shad_python/bigdata

hadoop jar /opt/hadoop/hadoop-streaming.jar \
    -D stream.num.map.output.key.fields=2 \
    -D mapreduce.job.output.key.comparator.class=org.apache.hadoop.mapreduce.lib.partition.KeyFieldBasedComparator \
    -D mapreduce.partition.keypartitioner.options='-k1,1' \
    -D mapreduce.partition.keycomparator.options='-k1 -k2' \
    -files hbase \
    -input /user/sandello/logs/access.log.${DATE} \
    -output liked/${DATE} \
    -mapper hbase/liked_mapper.py \
    -reducer hbase/liked_reducer.py \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner
