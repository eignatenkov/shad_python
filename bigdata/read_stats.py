#!/usr/bin/env python

import pandas as pd


def get_total_hits():
    return pd.Series.from_csv('total_hits.csv', header=None, parse_dates=True)


def get_unique_users():
    return pd.Series.from_csv('unique_users.csv', header=None,
                              parse_dates=True)


def get_top_pages():
    return pd.Series.from_csv('top_pages.csv', header=None, sep=';',
                              parse_dates=True)


def get_sessions_stats():
    sessions = pd.DataFrame.from_csv('session_aggs.csv', header=None,
                                     parse_dates=True)
    sessions.columns = ['ast', 'asl', 'br']
    return sessions


def get_new_users():
    return pd.Series.from_csv('new_users.csv', header=None, parse_dates=True)


def get_lost_users():
    return pd.Series.from_csv('lost_users.csv', header=None, parse_dates=True)
