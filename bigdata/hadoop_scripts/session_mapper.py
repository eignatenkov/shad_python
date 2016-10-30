#!/usr/bin/env python
import sys
from log_tools import get_error_code, get_page, get_ip, get_time


def main():
    for line in sys.stdin:
        if get_error_code(line) == 200:
            print "{0}\t{1}\t{2}".format(get_ip(line),
                                         get_time(line),
                                         get_page(line))


if __name__ == '__main__':
    main()
