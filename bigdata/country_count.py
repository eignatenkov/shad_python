#!/usr/bin/env python
import datetime
import argparse
from collections import Counter
from bisect import bisect_left
import json


def ip2num(ip):
    byte_0, byte_1, byte_2, byte_3 = map(int, ip.split("."))
    return byte_0 << 24 | byte_1 << 16 | byte_2 << 8 | byte_3 << 0


def get_country_count(date=datetime.date.today()-datetime.timedelta(days=1)):
    borders = []
    countries = []
    ccount = Counter()

    with open('IP2LOCATION-LITE-DB1.csv') as f:
        for line in f:
            info = line.split(',')
            borders.append(int(info[1].strip('"')))
            countries.append(info[3].strip('"\n\r'))

    with open("daily_user/{}.txt".format(date.strftime("%Y-%m-%d"))) as f:
        for line in f:
            ip = ip2num(line.strip())
            ccount[countries[bisect_left(borders, ip)]] += 1

    print "{0};{1}".format(date.strftime("%Y-%m-%d"),json.dumps(ccount))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", type=str)
    args = parser.parse_args()
    if args.date:
        get_country_count(date=datetime.datetime.strptime(args.date, "%Y-%m-%d").date())
    else:
        get_country_count()
