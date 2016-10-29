#!/usr/bin/env python

import pandas as pd


def get_total_hits():
    return pd.Series.from_csv('total_hits.csv', header=None, parse_dates=True)


def get_unique_users():
    return pd.Series.from_csv('unique_users.csv', header=None, parse_dates=True)