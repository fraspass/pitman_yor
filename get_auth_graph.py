#! /usr/bin/env python
import sys
# Define the object for the edges
import collections
edges = collections.Counter()
# Define edges as a function that counts the interactions
for line in sys.stdin:
    # Strip and split the dataline
    d = line.strip().split(",")
    try:
        # Obtain the (src,dst) pair
        user = d[3]
        computer = d[4]
        edges[(user,computer)] += 1
    except:
        continue

# Print and obtain a file
for edge in edges:
    print '\t'.join(edge)+'\t'+str(edges[edge])