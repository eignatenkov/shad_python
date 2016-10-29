#!/usr/bin/env python
import sys
from log_tools import get_error_code, get_page


def main():
    for line in sys.stdin:
        if get_error_code(line) == 200:
            print "{}\t1".format(get_page(line))


if __name__ == '__main__':
    main()
