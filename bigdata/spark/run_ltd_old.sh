#!/usr/bin/env bash
PREFIX="/user/sandello/logs/access.log."
for i in {2..1}
  do
    DATE=$(date +%Y-%m-%d -d "$i days ago")
    spark-submit --master yarn-client \
     --num-executors 6 \
     --driver-memory 2g \
     --executor-memory 8g \
     --executor-cores 4 \
     --conf "spark.yarn.executor.memoryOverhead=1024" \
     liked_three_days.py --date ${DATE}
  done