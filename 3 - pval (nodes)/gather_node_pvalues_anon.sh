hadoop jar /opt/mapr/hadoop/hadoop-0.20.2/contrib/streaming/hadoop-0.20.2-dev-streaming.jar \
  -D mapred.job.name="Combine node p-values" \
  -numReduceTasks 80 \
  -input MY_FOLDER/py_edge_pvals/part-* \
  -output MY_FOLDER/py_node_pvals \
  -mapper cat \
  -reducer src_pvalues_reducer.py \
  -file src_pvalues_reducer.py 
