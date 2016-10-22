hdfs dfs -rm -r out_test
# step 1
hadoop jar /opt/hadoop/hadoop-streaming.jar \
    -files strip_browser.py,count_browser.py -input logs/access.log.2016-10-08 -output out_test \
    -mapper strip_browser.py \
    -reducer count_browser.py
