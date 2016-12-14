#!/usr/bin/env python

from __future__ import print_function

import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

import re
import sys

def updateFunc(new_values, last_sum):
    return sum(new_values) + (last_sum or 0)

def filterUser(userIp):
    if userIp.startswith('8'):
        return True
    else:
        return False

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

    logger = sc._jvm.org.apache.log4j
    logger.LogManager.getLogger("org"). setLevel( logger.Level.ERROR )
    logger.LogManager.getLogger("akka").setLevel( logger.Level.ERROR )

    zkQuorum, topic = sys.argv[1:]
    kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer-11833", {topic: 4})
    lines = kvs.map(lambda x: x[1])
    # 1
    # counts = lines.flatMap(lambda line: readUserIp(line)) \
    #     .map(lambda word: (word, 1)) \
    #     .reduceByKey(lambda a, b: a+b)
    # counts.pprint()
    #counts.saveAsTextFiles('eight/eightUsers')

    # #2
    # counts = lines.flatMap(lambda line: readUserIp(line)) \
    #      .map(lambda word: (word, 1)) \
    #      .reduceByKeyAndWindow(lambda a, b: a+b, 10, 2)
    # counts.pprint()

    #3
    # counts = lines.flatMap(lambda line : readUserIp(line)) \
    #       .filter(lambda user: filterUser(user)) \
    #       .map(lambda user: (user, 1)) \
    #       .reduceByKey(lambda a, b: a+b);
    # counts.pprint()
    # counts.saveAsTextFiles('eight/eightUsers')

    #4
    # windowedCount1 = counts.window(10)
    # windowedCount2 = counts.window(60)
    # joinedStream = windowedCount1.join(windowedCount2)
    # joinedStream.pprint()

    # 5
    sortedCounts = lines.flatMap(lambda line: readUserIp(line)) \
                       .map(lambda user: (user, 1)) \
                       .updateStateByKey(updateFunc) \
                       .map(lambda (user,count): (count, user)) \
                       .transform(lambda rdd : rdd.sortByKey(False)) \
                       .foreachRDD(printTopUsers)
    # sortedCounts.pprint()

    ssc.start()
    ssc.awaitTermination()
