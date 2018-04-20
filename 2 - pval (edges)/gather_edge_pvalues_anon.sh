$HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/contrib/streaming/hadoop-0.20.2-dev-streaming.jar \
  -D mapred.job.name="Combine edge p-values" \
  -numReduceTasks 80 \
  -input MY_FOLDER/pitman_yor/part-* \
  -output MY_FOLDER/py_edge_pvals \
  -mapper key_pvalues_mapper.py \
  -reducer key_pvalues_reducer.py \
  -file key_pvalues_mapper.py key_pvalues_reducer.py 
