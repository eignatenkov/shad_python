#!/shared/anaconda/bin/python
import datetime
import argparse
import subprocess
from api import iterate_between_dates


def count_new_users(date=datetime.date.today()-datetime.timedelta(days=1)):
    old_users = set()
    start_date = max(date - datetime.timedelta(days=13), datetime.date(2016,10,7))
    end_date = date - datetime.timedelta(days=1)
    for day in iterate_between_dates(start_date, end_date):
        h_file = "daily_user/{}/part-00000".format(day.strftime("%Y-%m-%d"))
        cat = subprocess.Popen(["hdfs", "dfs", "-cat", h_file],
                               stdout=subprocess.PIPE)
        for line in cat.stdout:
            old_users.add(line.strip())
    new_users = set()
    h_file = "daily_user/{}/part-00000".format(date.strftime("%Y-%m-%d"))
    cat = subprocess.Popen(["hdfs", "dfs", "-cat", h_file],
                           stdout=subprocess.PIPE)
    for line in cat.stdout:
        if line.strip() not in old_users:
            new_users.add(line.strip())
    print "{0},{1}".format(date.strftime("%Y-%m-%d"), len(new_users))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", type=str)
    args = parser.parse_args()
    if args.date:
        count_new_users(date=datetime.datetime.strptime(args.date, "%Y-%m-%d").date())
    else:
        count_new_users()
