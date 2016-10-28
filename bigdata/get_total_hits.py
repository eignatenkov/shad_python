#!/usr/bin/env python

import pandas as pd


def get_total_hits():
    return pd.DataFrame.from_csv('total_hits.csv', header=None, parse_dates=True)
