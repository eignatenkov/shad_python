#!/usr/bin/env python
import sys
import datetime
from log_tools import get_error_code, get_page, get_ip, get_time


def main():
    for line in sys.stdin:
        if get_error_code(line) == 200:
            try:
                time = datetime.datetime.strptime(get_time(line), '%d/%b/%Y:%H:%M:%S')
                print "{0}\t{1}\t{2}".format(get_ip(line),
                                             get_time(line),
                                             get_page(line))
            except ValueError:
                pass


if __name__ == '__main__':
    main()
