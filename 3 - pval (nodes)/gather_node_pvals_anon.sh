#!/bin/sh

## ARGUMENT: type of p-value combiner from previous step that should be used in this analysis
## Options are: edgington, fisher, pearson, george, stouffer, tippett, min and minimum
ptype=$(printf %s "$1")

## Determine the correct combiner
if [ "$ptype" == "" ]
then ptype=tippett
fi

## Hadoop call
hadoop jar /opt/mapr/hadoop/hadoop-0.20.2/contrib/streaming/hadoop-0.20.2-dev-streaming.jar \
  -D mapred.job.name="Combine node p-values" \
  -numReduceTasks 80 \
  -input MY_FOLDER/py_edge_pvals/part-* \
  -output MY_FOLDER/py_node_pvals_$(printf %s "$ptype") \
  -mapper cat \
  -reducer "src_pvalues_reducer.py -p $(printf %s "$ptype")" \
  -file src_pvalues_reducer.py 
