#!/usr/bin/env bash
PREFIX="/user/sandello/logs/access.log."
for i in {4..1}
  do
    DATE=$(date +%Y-%m-%d -d "$i days ago")
    echo "$(/shared/anaconda/bin/python find_new_users.py --date ${DATE})" >> new_users.csv
    echo "$(/shared/anaconda/bin/python find_lost_users.py --date ${DATE})" >> lost_users.csv
  done
