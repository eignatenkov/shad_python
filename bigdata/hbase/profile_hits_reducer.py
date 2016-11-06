#!/usr/bin/env python

import happybase
import logging
import random
import sys
from collections import Counter

HOSTS = ["hadoop2-%02d.yandex.ru" % i for i in xrange(11, 14)]
TABLE = "bigdatashad_eignatenkov_profile_hits"


def connect():
    host = random.choice(HOSTS)
    conn = happybase.Connection(host)

    logging.debug("Connecting to HBase Thrift Server on %s", host)
    conn.open()

    if TABLE not in conn.tables():
        conn.create_table(TABLE, {"f": dict()})

    return happybase.Table(TABLE, conn)


def counter_to_string(counter):
    return {key:str(value) for key, value in counter.iteritems()}


def main():
    table = connect()
    b = table.batch()
    current_profile = None
    hour_counts = Counter()
    for line in sys.stdin:
        profile, hour = line.strip().split('\t')
        if profile != current_profile:
            if current_profile:
                b.put(current_profile, counter_to_string(hour_counts))
            current_profile = profile
            hour_counts = Counter()
            hour_counts['f:{}'.format(hour)] += 1
        else:
            hour_counts['f:{}'.format(hour)] += 1
    b.put(current_profile, counter_to_string(hour_counts))
    b.send()


if __name__ == '__main__':
    main()

