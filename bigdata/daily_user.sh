#!/usr/bin/env bash
DATE=${1:-$(date +%Y-%m-%d -d "yesterday")}

hdfs dfs -rm -r daily_user/$DATE

cd /home/eignatenkov/shad_python/bigdata

hadoop jar /opt/hadoop/hadoop-streaming.jar \
    -D mapreduce.job.reduces=1 \
    -files hadoop_scripts \
    -input /user/sandello/logs/access.log.${DATE} \
    -output daily_user/${DATE} \
    -mapper hadoop_scripts/tu_mapper.py \
    -reducer hadoop_scripts/daily_user_reducer.py

# hdfs dfs -get daily_user/${DATE}/part-00000 /home/eignatenkov/shad_python/bigdata/daily_user/${DATE}.txt

echo "$(/shared/anaconda/bin/python find_new_users.py --date ${DATE})" >> new_users.csv
echo "$(/shared/anaconda/bin/python find_lost_users.py --date ${DATE})" >> lost_users.csv
echo "$(python country_count.py --date ${DATE})" >> country_info.csv

