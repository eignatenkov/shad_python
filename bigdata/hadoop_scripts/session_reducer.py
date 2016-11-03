#!/usr/bin/env python
import sys
import datetime


def main():
    current_ip = None
    for line in sys.stdin:
        ip, time, page = line.strip().split('\t')
        time = datetime.datetime.strptime(time, '%d/%b/%Y:%H:%M:%S')
        if ip != current_ip:
            if current_ip:
                print "{0}\t{1}".format((cs_end - cs_start).seconds, cs_pages)
            current_ip = ip
            cs_start = time
            cs_end = time
            cs_pages = 1

        else:
            if time - cs_end <= datetime.timedelta(minutes=30):
                cs_end = time
                cs_pages+=1
            else:
                print "{0}\t{1}".format((cs_end - cs_start).seconds, cs_pages)
                cs_start = time
                cs_end = time
                cs_pages = 1

    print "{0}\t{1}".format((cs_end - cs_start).seconds, cs_pages)

if __name__ == '__main__':
    main()
