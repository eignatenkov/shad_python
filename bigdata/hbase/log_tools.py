import datetime


def get_ip(log_line):
    return log_line.split(' ', 1)[0]


def get_time(log_line):
    string_time = log_line.split('[')[1].split(']')[0][:-6]
    return string_time


def get_day_hour(log_line):
    splits = get_time(log_line).split(':')
    return datetime.datetime.strptime(splits[0], '%d/%b/%Y').strftime('%Y-%m-%d'), splits[1]


def get_error_code(log_line):
    return int(log_line.split('"')[2].split()[0])


def get_page(log_line):
    return log_line.split('"')[1].strip('GET ').split(' ')[0]


def get_visited_profile(log_line):
    candidate = get_page(log_line).split('?')[0].strip('/')
    if candidate.startswith('id'):
        return candidate
    else:
        return None
