#!/usr/bin/env python

import happybase
import logging
import random
import sys
from collections import Counter, defaultdict

HOSTS = ["hadoop2-%02d.yandex.ru" % i for i in xrange(11, 14)]
PH_TABLE = "bigdatashad_eignatenkov_profile_hits"
PU_TABLE = "bigdatashad_eignatenkov_profile_users"


def connect(table):
    host = random.choice(HOSTS)
    conn = happybase.Connection(host)

    logging.debug("Connecting to HBase Thrift Server on %s", host)
    conn.open()

    if table not in conn.tables():
        conn.create_table(table, {"f": dict()})

    return happybase.Table(table, conn)


def counter_to_string(counter):
    return {key: str(value) for key, value in counter.iteritems()}


def pu_dict_to_string(pu_dict):
    return {key: str(len(value)) for key, value in pu_dict.iteritems()}


def main():
    ph_table = connect(PH_TABLE)
    pu_table = connect(PU_TABLE)
    ph_batch = ph_table.batch()
    pu_batch = pu_table.batch()
    current_profile = None
    hour_counts = Counter()
    hour_user_counts = defaultdict(set)
    for line in sys.stdin:
        profile, hour, user = line.strip().split('\t')
        if profile != current_profile:
            if current_profile:
                ph_batch.put(current_profile, counter_to_string(hour_counts))
                pu_batch.put(current_profile, pu_dict_to_string(hour_user_counts))
            current_profile = profile
            hour_counts = Counter()
            hour_user_counts = defaultdict(set)
        hour_counts['f:{}'.format(hour)] += 1
        hour_user_counts['f:{}'.format(hour)].add(user)

    ph_batch.put(current_profile, counter_to_string(hour_counts))
    pu_batch.put(current_profile, pu_dict_to_string(hour_user_counts))
    ph_batch.send()
    pu_batch.send()


if __name__ == '__main__':
    main()

