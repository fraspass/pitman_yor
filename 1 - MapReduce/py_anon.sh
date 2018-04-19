$HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/contrib/streaming/hadoop-0.20.2-dev-streaming.jar \
  -D mapred.job.name="Pitman-Yor process anomaly detection" \
  -D stream.num.map.output.key.fields=2 \
  -D mapred.text.key.partitioner.options=-k1,1 \
  -D mapred.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator \
  -D mapred.text.key.comparator.options="-k1,1 -k2,2n" \
  -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
  -numReduceTasks 80 \
  -input MY_FOLDER/lanl_data/ \
  -output MY_FOLDER/pitman_yor \
  -mapper "python key_mapper.py" \
  -reducer "python py_pvalues_reducer.py -k 16230" \
  -file key_mapper.py py_pvalues_reducer.py alpha.txt d.txt

