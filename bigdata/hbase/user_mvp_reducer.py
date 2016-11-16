#!/usr/bin/env python

import happybase
import logging
import random
import sys
from collections import Counter, defaultdict

HOSTS = ["hadoop2-%02d.yandex.ru" % i for i in xrange(11, 14)]
MVP_TABLE = "bigdatashad_eignatenkov_mvp"


def connect(table):
    host = random.choice(HOSTS)
    conn = happybase.Connection(host)

    logging.debug("Connecting to HBase Thrift Server on %s", host)
    conn.open()

    if table not in conn.tables():
        conn.create_table(table, {"f": dict()})

    return happybase.Table(table, conn)


def sorted_counter_keys(counter):
    return '_'.join(l[0] for l in sorted(counter.items(), key=lambda el: (-el[1], el[0])))


def main():
    mvp_table = connect(MVP_TABLE)
    mvp_batch = mvp_table.batch()
    current_row_key = None
    profile_counts = Counter()
    for line in sys.stdin:
        row_key, profile = line.strip().split('\t')
        if row_key != current_row_key:
            if current_row_key:
                mvp_batch.put(current_row_key, {'f:value': sorted_counter_keys(profile_counts)})
            current_row_key = row_key
            profile_counts = Counter()
        profile_counts[profile] += 1

    mvp_batch.put(current_row_key, {'f:value': sorted_counter_keys(profile_counts)})
    mvp_batch.send()


if __name__ == '__main__':
    main()

