#!/usr/bin/env python

import sys
from operator import add

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils


def updateFunc(new_values, last_sum):
    return sum(new_values) + (last_sum or 0)


def is_bad_line(log_line):
    try:
        code = int(log_line.split('"')[2].split()[0])
        return code != 200
    except:
        return True


def print_count(rdd):
    print("15_second_count={}".format(rdd.count()))

def print_mincount(rdd):
    print("60_second_count={}".format(rdd.countByWindow(60,60)))

if __name__ == "__main__":
    sc = SparkContext(appName="Ignatenkov_badrequests")
    ssc = StreamingContext(sc, 15)

    logger = sc._jvm.org.apache.log4j
    logger.LogManager.getLogger("org"). setLevel( logger.Level.ERROR )
    logger.LogManager.getLogger("akka").setLevel( logger.Level.ERROR )
    
    zkQuorum, topic = sys.argv[1:]
    kvs = KafkaUtils.createStream(ssc, zkQuorum,
                                  "spark-streaming-consumer-11833", {topic: 4})
    lines = kvs.map(lambda x: x[1])

    bad_lines = lines.filter(is_bad_line)
    bad_lines.foreachRDD(print_count)

    bad_lines.foreachRDD(print_mincount)
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
    # sortedCounts = lines.flatMap(lambda line: readUserIp(line)) \
    #     .map(lambda user: (user, 1)) \
    #     .updateStateByKey(updateFunc) \
    #     .map(lambda (user, count): (count, user)) \
    #     .transform(lambda rdd: rdd.sortByKey(False)) \
    #     .foreachRDD(printTopUsers)
    # # sortedCounts.pprint()

    ssc.start()
    ssc.awaitTermination()
