#!/usr/bin/env python
import sys
from log_tools import get_error_code


def main():
    for line in sys.stdin:
        if get_error_code(line) == 200:
            print 1


if __name__ == '__main__':
    main()

