#!/usr/bin/env python

import re
import datetime
import argparse
from pyspark import SparkContext
from pyspark import SparkConf


def get_liked_profile(log_line):
    record_re = re.compile('([\d\.:]+) - - \[(\S+ [^"]+)\] "(\w+) ([^"]+) (HTTP/[\d\.]+)" (\d+) \d+ "([^"]+)" "([^"]+)"')
    match = record_re.search(log_line)
    if match.group(6) == '200':
       if 'like=1' in match.group(4):
            return [match.group(4).split('?')[0]]
    return []


if __name__ == "__main__":
    conf = SparkConf().setAppName("eignatenkov_liked").set("spark.ui.port", "4050")
    sc = SparkContext(conf=conf)

    parser = argparse.ArgumentParser()
    parser.add_argument("--date", type=str)
    args = parser.parse_args()

    def process_day(day):
        log = sc.textFile('/user/sandello/logs/access.log.{}'.format(
            day.strftime("%Y-%m-%d")))
        liked_log = log.flatMap(get_liked_profile)
        return liked_log.distinct().map(lambda x: (x, 1))

    if args.date:
        y_day = datetime.datetime.strptime(args.date, "%Y-%m-%d")
    else:
        y_day = datetime.datetime.today() - datetime.timedelta(days=1)
    yy_day = y_day - datetime.timedelta(days=1)
    yyy_day = yy_day - datetime.timedelta(days=1)

    result = process_day(y_day).union(process_day(yy_day)).union(process_day(yyy_day)).reduceByKey(lambda a, b: a + b).filter(lambda (k, v): v == 3).count()

    with open("/home/eignatenkov/shad_python/bigdata/liked_three_days.csv", 'a') as file:
        file.write('{0};{1}\n'.format(y_day.strftime("%Y-%m-%d"), result))

    sc.stop()
