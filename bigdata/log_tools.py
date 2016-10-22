

def get_ip(log_line):
    return log_line.split(' ', 1)[0]


def get_time(log_line):
    string_time = log_line.split('[')[1].split(']')[0]
    return string_time