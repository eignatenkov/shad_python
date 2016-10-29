#!/usr/bin/env python
import sys


def main():
    current_page = None
    counter = 0
    for line in sys.stdin:
        key, value = line.strip().split('\t')
        if key == current_page:
            counter += int(value)
        else:
            print "{0}\t{1}".format(current_page, counter)
            current_page = key
            counter = 1
    print "{0}\t{1}".format(current_page, counter)

if __name__ == '__main__':
    main()

