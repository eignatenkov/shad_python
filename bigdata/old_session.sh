#!/usr/bin/env bash
PREFIX="/user/sandello/logs/access.log."
for i in {16..1}
  do
    DATE=$(date +%Y-%m-%d -d "$i days ago")
    echo "$DATE,$(hdfs dfs -cat /user/sandello/logs/access.log.${DATE} | python \
          hadoop_scripts/session_mapper.py | sort -k 1,1 -k 2,2 | python \
          hadoop_scripts/session_reducer.py | python hadoop_scripts/session_aggs.py)" \
          >> "/home/eignatenkov/shad_python/bigdata/session_aggs.csv"
    echo "$DATE done"
  done
