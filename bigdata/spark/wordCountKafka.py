#!/usr/bin/env python

from __future__ import print_function

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

import re
import sys


def readUserIp(line):
    log_format = re.compile(r"(?P<userIp>[\d\.]+)\s")
    match = log_format.match(line)
    if not match:
        return None
    request = match.group('userIp').split()
    return request


def printTopUsers(rdd):
    top10Rdd = rdd.take(5)
    print("Top 5 users:")
    for r in top10Rdd:
        print("User %s total hits = %s" % (r[1], r[0]))
    print("--------------------------------------------")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: kafka_wordcount.py <zk> <topic>", file=sys.stderr)
        exit(-1)

    sc = SparkContext(appName="PythonStreamingKafkaWordCount")
    ssc = StreamingContext(sc, 10)
    ssc.checkpoint("checkpointKafka")

    zkQuorum, topic = sys.argv[1:]
    kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer-11833", {topic: 4})
    lines = kvs.map(lambda x: x[1])
    counts = lines.flatMap(lambda line: readUserIp(line)) \
        .map(lambda word: (word, 1)) \
        .reduceByKey(lambda a, b: a+b)
    counts.pprint()

    ssc.start()
    ssc.awaitTermination()
