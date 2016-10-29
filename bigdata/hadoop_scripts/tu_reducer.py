#!/usr/bin/env python
import sys


def main():
    unique_users = set()
    for line in sys.stdin:
        ip = line.strip()
        unique_users.add(ip)
    print len(unique_users)

if __name__ == '__main__':
    main()

