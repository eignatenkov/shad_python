#!/usr/bin/env python
import sys
from log_tools import get_error_code, get_visited_profile, get_day_hour, get_ip


def main():
    for line in sys.stdin:
        if get_error_code(line) == 200:
            day, hour = get_day_hour(line)
            profile = get_visited_profile(line)
            user = get_ip(line)
            if profile:
                print "{0}_{1}\t{2}\t{3}".format(profile, day, hour, user)


if __name__ == '__main__':
    main()
