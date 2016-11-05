#!/usr/bin/env python
import sys
from log_tools import get_error_code, get_ip


def main():
    for line in sys.stdin:
        if get_error_code(line) == 200:
            print "{}\t1".format(get_ip(line))


if __name__ == '__main__':
    main()
