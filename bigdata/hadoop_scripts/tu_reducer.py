#!/usr/bin/env python
import sys


def main():
    unique_users = set()
    for line in sys.stdin:
        unique_users.add(line.strip())
    print len(unique_users)
