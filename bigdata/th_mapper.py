#!/usr/bin/env python
import sys


def get_error_code(log_line):
    return int(log_line.split('"')[2].split()[0])


def main():
    for line in sys.stdin:
        if get_error_code(line) == 200:
            print '1'


if __name__ == '__main__':
    main()

