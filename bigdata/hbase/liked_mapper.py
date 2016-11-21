#!/usr/bin/env python
import sys
from datetime import datetime
from log_tools import parse_line, get_visited_profile


def main():
    for line in sys.stdin:
        line_dict = parse_line(line)
        if line_dict['error'] == '200':
            if line_dict['page'].split('?')[-1] == 'like=1':
                bad_date = line_dict['time'].split(':')[0]
                good_date = datetime.strptime(bad_date, '%d/%b/%Y').strftime(
                    '%Y-%m-%d')
                print "{0}_{1}\t{2}\t{3}".format(get_visited_profile(line),
                                                 good_date,
                                                 line_dict['time'],
                                                 line_dict['ip'])


if __name__ == '__main__':
    main()
