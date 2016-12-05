#!/usr/bin/env python

import argparse
import datetime
import getpass
import hashlib
import struct
import json
import happybase
import random

from read_stats import get_total_hits, get_unique_users, get_top_pages, \
    get_sessions_stats, get_new_users, get_lost_users, get_country_stats

from flask import Flask, request, abort, jsonify

app = Flask(__name__)
app.secret_key = "my_secret_key"

HOSTS = ["hadoop2-%02d.yandex.ru" % i for i in xrange(11, 14)]
PH_TABLE = "bigdatashad_eignatenkov_profile_hits"
PU_TABLE = "bigdatashad_eignatenkov_profile_users"
MVP_TABLE = "bigdatashad_eignatenkov_mvp"
LIKED_TABLE = "bigdatashad_eignatenkov_liked"


def connect(table_name):
    host = random.choice(HOSTS)
    conn = happybase.Connection(host)
    conn.open()
    return happybase.Table(table_name, conn)


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
        if date < datetime.datetime(2016,10,7) or date >= datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time()):
            result[date.strftime("%Y-%m-%d")] = {}
        else:
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


@app.route("/api/hw2/profile_hits")
def api_hw2_profile_hits():
    start_date = request.args.get("start_date", None)
    end_date = request.args.get("end_date", None)
    profile_id = request.args.get("profile_id", None)
    if start_date is None or end_date is None or profile_id is None:
        abort(400)
    start_date = datetime.datetime(*map(int, start_date.split("-")))
    end_date = datetime.datetime(*map(int, end_date.split("-")))
    ph_table = connect(PH_TABLE)
    answer = dict()
    for date in iterate_between_dates(start_date, end_date):
        if date < datetime.datetime(2016,10,7) or date >= datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time()):
            pass
        else:
            row_key = "{0}_{1}".format(profile_id, date.strftime("%Y-%m-%d"))
            data = ph_table.row(row_key)
            if len(data) == 0:
                answer[date.strftime("%Y-%m-%d")] = [0]*24
            else:
                answer[date.strftime("%Y-%m-%d")] = [int(data.get('f:{}'.format(i), 0)) for i in range(24)]
    return jsonify(answer)


@app.route("/api/hw2/profile_users")
def api_hw2_profile_users():
    start_date = request.args.get("start_date", None)
    end_date = request.args.get("end_date", None)
    profile_id = request.args.get("profile_id", None)
    if start_date is None or end_date is None or profile_id is None:
        abort(400)
    start_date = datetime.datetime(*map(int, start_date.split("-")))
    end_date = datetime.datetime(*map(int, end_date.split("-")))
    pu_table = connect(PU_TABLE)
    answer = dict()
    for date in iterate_between_dates(start_date, end_date):
        if date < datetime.datetime(2016,10,7) or date >= datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time()):
            pass
        else:
            row_key = "{0}_{1}".format(profile_id, date.strftime("%Y-%m-%d"))
            data = pu_table.row(row_key)
            if len(data) == 0:
                answer[date.strftime("%Y-%m-%d")] = [0]*24
            else:
                answer[date.strftime("%Y-%m-%d")] = [int(data.get('f:{}'.format(i), 0)) for i in range(24)]
    return jsonify(answer)


@app.route("/api/hw2/user_most_visited_profiles")
def api_hw2_user_most_visited_profiles():
    date = request.args.get("date", None)
    user_ip = request.args.get("user_ip", None)
    if date is None or user_ip is None:
        abort(400)
    row = "{0}_{1}".format(user_ip, date)
    mvp_table = connect(MVP_TABLE)
    value = mvp_table.row(row)
    if len(value) == 0:
        answer = []
    else:
        answer = value['f:value'].split('_')
    return jsonify({'profiles': answer})


@app.route("/api/hw2/profile_last_three_liked_users")
def api_hw2_profile_last_three_liked_users():
    profile_id = request.args.get("profile_id", None)
    date = request.args.get("date", None)
    if profile_id is None or date is None:
        abort(400)
    liked_table = connect(LIKED_TABLE)
    answer = list()
    day_number = 0
    while len(answer) < 3 and day_number < 5:
        check_date = datetime.datetime(*map(int, date.split("-"))) - \
                     datetime.timedelta(days=day_number)
        row_id = "{0}_{1}".format(profile_id, check_date.strftime("%Y-%m-%d"))
        value = liked_table.row(row_id)
        if len(value) > 0:
            answer.extend(value['f:v'].split('_'))

    return jsonify({'users': answer[:3]})


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
