#!/usr/bin/env python
# from __future__ import print_function
import sys
from pyspark import SparkContext
from pyspark.streaming import StreamingContext


def parseLine(line):
 split_values = line.split(' ')
 return (split_values[0], 1)

def print_rdd(rdd, title):
    value = rdd.collect()[0] if len(rdd.collect()) > 0 else 0
    if title.startswith('20'):
        print "{0}={1};".format(title, value)
    else:
        print "{0}={1};".format(title, value),

def get_count(rdd):
    count = rdd.collect()
    return count[0] if len(count) > 0 else 0

if __name__ == "__main__":
    sc = SparkContext(appName="PythonStreamingWC")
    ssc = StreamingContext(sc, 5)
    ssc.checkpoint('linecount_checkpoint')
    logger = sc._jvm.org.apache.log4j
    logger.LogManager.getLogger("org"). setLevel( logger.Level.ERROR )
    logger.LogManager.getLogger("akka").setLevel( logger.Level.ERROR )
    lines = ssc.socketTextStream(sys.argv[1], int(sys.argv[2]))
    objects = lines.count()
    window = lines.countByWindow(20, 5)
    objects.foreachRDD(lambda x: print_rdd(x, '5_second_count'))
    window.foreachRDD(lambda x: print_rdd(x, '20_second_count'))
#    objects.join(window).pprint()

    ssc.start()
    ssc.awaitTermination()
