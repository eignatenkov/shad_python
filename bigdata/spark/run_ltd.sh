#!/usr/bin/env bash
DATE=${1:-$(date +%Y-%m-%d -d "yesterday")}
cd /home/eignatenkov/shad_python/bigdata/spark
spark-submit --master yarn-client \
     --num-executors 6 \
     --driver-memory 2g \
     --executor-memory 8g \
     --executor-cores 4 \
     --conf "spark.yarn.executor.memoryOverhead=1024" \
     liked_three_days.py --date ${DATE}
