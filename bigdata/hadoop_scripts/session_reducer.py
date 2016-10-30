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
                print "{0}\t{1}".format((cs_times[-1] - cs_times[0]).seconds,
                                        len(cs_pages))
            current_ip = ip
            cs_times = [time]
            cs_pages = {page}

        else:
            if time - cs_times[-1] <= datetime.timedelta(minutes=30):
                cs_times.append(time)
                cs_pages.add(page)
            else:
                print "{0}\t{1}".format((cs_times[-1]-cs_times[0]).seconds,
                                        len(cs_pages))
                cs_times = [time]
                cs_pages = {page}

    print "{0}\t{1}".format((cs_times[-1] - cs_times[0]).seconds,
                            len(cs_pages))

if __name__ == '__main__':
    main()
