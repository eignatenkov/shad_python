#!/usr/bin/env python
import sys


def main():
    current_key = None
    for line in sys.stdin:
        ip = line.strip()
        if current_key != ip:
            print ip
            current_key = ip
