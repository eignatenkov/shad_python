#!/usr/bin/env python

import argparse
import datetime
import getpass
import hashlib
import struct
import json

from read_stats import get_total_hits, get_unique_users, get_top_pages, \
    get_sessions_stats, get_new_users, get_lost_users, get_country_stats

from flask import Flask, request, abort, jsonify

app = Flask(__name__)
app.secret_key = "my_secret_key"


def iterate_between_dates(start_date, end_date):
    span = end_date - start_date
    for i in xrange(span.days + 1):
        yield start_date + datetime.timedelta(days=i)


@app.route("/")
def index():
    return "OK!"


@app.route("/api/hw1")
def api_hw1():
    start_date = request.args.get("start_date", None)
    end_date = request.args.get("end_date", None)
    if start_date is None or end_date is None:
        abort(400)
    start_date = datetime.datetime(*map(int, start_date.split("-")))
    end_date = datetime.datetime(*map(int, end_date.split("-")))
    everyday_hits = get_total_hits()
    everyday_users = get_unique_users()
    everyday_toppages = get_top_pages()
    everyday_sessions = get_sessions_stats()
    everyday_new_users = get_new_users()
    everyday_lost_users = get_lost_users()
    everyday_country_stats = get_country_stats()
    result = {}
    for date in iterate_between_dates(start_date, end_date):
        total_hits = everyday_hits.at[date]
        unique_users = everyday_users.at[date]
        new_users = everyday_new_users.at[date]
        lost_users = everyday_lost_users.at[date]
        top_pages = everyday_toppages.at[date].strip(',').split(',')
        session_stats = everyday_sessions.loc[date]
        country_stats = json.loads(everyday_country_stats.loc[date])
        result[date.strftime("%Y-%m-%d")] = {
            "total_hits": total_hits,
            "total_users": unique_users,
            "top_10_pages": top_pages,
            "average_session_time": session_stats['ast'],
            "average_session_length": session_stats['asl'],
            "bounce_rate": session_stats['br'],
            "new_users": new_users,
            "lost_users": lost_users,
            "users_by_country": country_stats
        }

    return jsonify(result)


def login_to_port(login):
    """
    We believe this method works as a perfect hash function
    for all course participants. :)
    """
    hasher = hashlib.new("sha1")
    hasher.update(login)
    values = struct.unpack("IIIII", hasher.digest())
    folder = lambda a, x: a ^ x + 0x9e3779b9 + (a << 6) + (a >> 2)
    return 10000 + reduce(folder, values) % 20000


def main():
    parser = argparse.ArgumentParser(description="HW 1 Example")
    parser.add_argument("--host", type=str, default="127.0.0.1")
    parser.add_argument("--port", type=int, default=login_to_port(getpass.getuser()))
    parser.add_argument("--debug", action="store_true", dest="debug")
    parser.add_argument("--no-debug", action="store_false", dest="debug")
    parser.set_defaults(debug=False)

    args = parser.parse_args()
    app.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == "__main__":
    main()
