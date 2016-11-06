#!/usr/bin/env python
import sys
from log_tools import get_error_code, get_visited_profile, get_day_hour


def main():
    for line in sys.stdin:
        if get_error_code(line) == 200:
            day, hour = get_day_hour(line)
            profile = get_visited_profile(line)
            if profile:
                print "{0}_{1}\t{2}".format(profile, day, hour)


if __name__ == '__main__':
    main()
