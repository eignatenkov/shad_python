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


def print_rdd(rdd, title):
    value = rdd.collect()[0] if len(rdd.collect()) > 0 else 0
    if title.startswith('60'):
        print "{0}={1};".format(title, value)
    else:
        print "{0}={1};".format(title, value),

if __name__ == "__main__":
    sc = SparkContext(appName="Ignatenkov_badrequests")
    ssc = StreamingContext(sc, 15)
    ssc.checkpoint('badcount_checkpoint')  
    logger = sc._jvm.org.apache.log4j
    logger.LogManager.getLogger("org"). setLevel( logger.Level.ERROR )
    logger.LogManager.getLogger("akka").setLevel( logger.Level.ERROR )
    
    zkQuorum, topic = sys.argv[1:]
    kvs = KafkaUtils.createStream(ssc, zkQuorum,
                                  "spark-streaming-consumer-11833", {topic: 4})
    lines = kvs.map(lambda x: x[1])

    bad_lines = lines.filter(is_bad_line)
    single = bad_lines.count()
    window = bad_lines.countByWindow(60, 15)
    single.foreachRDD(lambda x: print_rdd(x, '15_second_count'))
    window.foreachRDD(lambda x: print_rdd(x, '60_second_count'))

    ssc.start()
    ssc.awaitTermination()
