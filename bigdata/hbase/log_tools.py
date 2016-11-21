import datetime
import re


def parse_line(log_line):
    record_re = re.compile('([\d\.:]+) - - \[(\S+ [^"]+)\] "(\w+) ([^"]+) (HTTP/[\d\.]+)" (\d+) \d+ "([^"]+)" "([^"]+)"')
    match = record_re.search(log_line)
    if not match:
        raise ValueError
    return {
        "ip": match.group(1),
        "time": match.group(2)[:-6],
        "page": match.group(4),
        "error": match.group(6)
    }


def get_ip(log_line):
    return log_line.split(' ', 1)[0]


def get_time(log_line):
    string_time = log_line.split('[')[1].split(']')[0][:-6]
    return string_time


def get_day_hour(log_line):
    splits = get_time(log_line).split(':')
    return datetime.datetime.strptime(splits[0], '%d/%b/%Y').strftime('%Y-%m-%d'), splits[1]


def get_error_code(log_line):
    try:
        code = int(log_line.split('"')[2].split()[0])
        return code
    except:
        return 500


def get_page(log_line):
    return log_line.split('"')[1].strip('GET ').split(' ')[0]


def get_visited_profile(log_line):
    candidate = get_page(log_line).split('?')[0].strip('/')
    if candidate.startswith('id'):
        return candidate
    else:
        return None


def have_like(log_line):
    return 'like=1' in get_page(log_line)
