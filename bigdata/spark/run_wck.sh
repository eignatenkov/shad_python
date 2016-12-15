#!/bin/bash

spark-submit \
      --jars /opt/cloudera/parcels/CDH/jars/spark-streaming-kafka_2.10-1.6.0-cdh5.9.0.jar \
      --conf spark.eventLog.enabled=false \
      --master yarn-client \
      --num-executors 2 \
      --executor-cores 1 \
      --executor-memory 2048m \
      wordCountKafka.py hadoop2-10:2181 bigdatashad-2016
