#!/usr/bin/env python

from __future__ import print_function
import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

def is_bad_line(log_line):
    try:
        code = int(log_line.split('"')[2].split()[0])
        return code != 200
    except:
        return True

def update_total(new, runningCount):
    if runningCount is None:
        runningCount = 0
    return sum(new, runningCount)


def print_counts(rdd):
    values = rdd.collectAsMap().get('count')
#    print(values)
    if values:
        print("15_second_count={0}; 60_second_count={1}; total_count={2};".format(values[0][0], values[0][1], values[1]))


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
    count_bl = bad_lines.count().map(lambda x: ('count', x))
    count_wl = bad_lines.countByWindow(60,15).map(lambda x: ('count', x))
    total_count = count_bl.updateStateByKey(update_total)
    joinedStream = count_bl.join(count_wl).join(total_count)

    joinedStream.foreachRDD(print_counts)
    #joinedStream.pprint()

    ssc.start()
    ssc.awaitTermination()
