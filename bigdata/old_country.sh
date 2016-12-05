#!/usr/bin/env bash
PREFIX="/user/sandello/logs/access.log."
for i in {7..5}
  do
    DATE=$(date +%Y-%m-%d -d "$i days ago")
    echo "$(python country_count.py --date ${DATE})" >> country_info.csv
  done
