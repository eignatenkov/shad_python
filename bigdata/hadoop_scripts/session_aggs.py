import sys


def main():
    session_counter = 0
    skeleton_counter = 0
    total_time = 0
    total_length = 0
    for line in sys.stdin:
        session_counter += 1
        time, length = line.strip().split('\t')
        time = int(time)
        length = int(length)
        if length == 1:
            skeleton_counter += 1
        total_time += time
        total_length += length
    print '{0}, {1}, {2}'.format(float(total_time)/session_counter,
                                 float(total_length)/session_counter,
                                 float(skeleton_counter)/session_counter)

if __name__ == '__main__':
    main()
