#!/usr/bin/env python
import sys
from log_tools import parse_line


def main():
    for line in sys.stdin:
        line_dict = parse_line(line)
        if line_dict['error'] == '200':
            print '1'


if __name__ == '__main__':
    main()

