#!/usr/bin/env python

import happybase
import logging
import random
import sys

HOSTS = ["hadoop2-%02d.yandex.ru" % i for i in xrange(11, 14)]
TABLE = "bigdatashad_eignatenkov_test_hbase"


def connect():
    host = random.choice(HOSTS)
    conn = happybase.Connection(host)

    logging.debug("Connecting to HBase Thrift Server on %s", host)
    conn.open()

    if TABLE not in conn.tables():
        # Create a table with column family `cf` with default settings.
        conn.create_table(TABLE, {"cf": dict()})
        logging.debug("Created table %s", TABLE)
    else:
        logging.debug("Using table %s", TABLE)
    return happybase.Table(TABLE, conn)


def main():
    table = connect()
    b = table.batch()
    current_user = None
    current_count = 0
    for line in sys.stdin:
        ip, count = line.strip().split('\t')
        if ip != current_user:
            if current_user:
                b.put(current_user, {"cf:value": current_count})
            current_user = ip
            current_count = 1
        else:
            current_count += 1
    b.put(current_user, {"cf:value": current_count})
    b.send()


if __name__ == '__main__':
    main()

