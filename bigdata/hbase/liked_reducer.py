#!/usr/bin/env python

import happybase
import logging
import random
import operator
import sys

HOSTS = ["hadoop2-%02d.yandex.ru" % i for i in xrange(11, 14)]
LIKED_TABLE = "bigdatashad_eignatenkov_liked"


def connect(table):
    host = random.choice(HOSTS)
    conn = happybase.Connection(host)

    logging.debug("Connecting to HBase Thrift Server on %s", host)
    conn.open()

    if table not in conn.tables():
        conn.create_table(table, {"f": dict()})

    return happybase.Table(table, conn)


def most_recent(l_dict):
    return '_'.join([i[0] for i in sorted(l_dict.items(),
                                          key=operator.itemgetter(1))[-3:]])


def pu_dict_to_string(pu_dict):
    return {key: str(len(value)) for key, value in pu_dict.iteritems()}


def main():
    liked_table = connect(LIKED_TABLE)
    liked_batch = liked_table.batch()
    current_profile = None
    liked_dict = dict()
    for line in sys.stdin:
        profile, time, user = line.strip().split('\t')
        if profile != current_profile:
            if current_profile:
                liked_batch.put(current_profile, {"f:v": most_recent(liked_dict)})
            current_profile = profile
            liked_dict = dict()
        liked_dict[user] = time
    liked_batch.put(current_profile, {"f:v": most_recent(liked_dict)})
    liked_batch.send()


if __name__ == '__main__':
    main()
