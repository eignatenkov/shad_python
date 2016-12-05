#!/usr/bin/env bash
PREFIX="/user/sandello/logs/access.log."
cd /home/eignatenkov/shad_python/bigdata
for i in {14..1}
  do
    DATE=$(date +%Y-%m-%d -d "$i days ago")
    hdfs dfs -rm -r liked/$DATE
    hadoop jar /opt/hadoop/hadoop-streaming.jar \
        -D stream.num.map.output.key.fields=2 \
        -D mapreduce.job.output.key.comparator.class=org.apache.hadoop.mapreduce.lib.partition.KeyFieldBasedComparator \
        -D mapreduce.partition.keypartitioner.options='-k1,1' \
        -D mapreduce.partition.keycomparator.options='-k1 -k2' \
        -files hbase \
        -input ${PREFIX}${DATE} \
        -output liked/${DATE} \
        -mapper hbase/liked_mapper.py \
        -reducer hbase/liked_reducer.py \
        -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner
  done

