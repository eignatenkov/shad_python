#!/usr/bin/env python
import sys


def main():
    unique_users = set()
    for line in sys.stdin:
        ip = line.strip()
        if ip not in unique_users:
            print ip
        unique_users.add(ip)

if __name__ == '__main__':
    main()
