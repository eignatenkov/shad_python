#!/bin/bash

spark-submit \
      --conf spark.eventLog.enabled=false \
      --master yarn-client \
      --num-executors 2 \
      --executor-cores 1 \
      --executor-memory 2048m \
      kafka_bad_requests.py hadoop2-10:2181 bigdatashad-2016
