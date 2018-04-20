#! /usr/bin/env python
import sys

## Example of input:
# 1,C608$@DOM1,C608$@DOM1,C608,C467,Kerberos,Network,LogOn,Success

# Count connections on each edge
import collections
edges = collections.Counter()

# Read from input
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

# Print to console
for edge in edges:
    print '\t'.join(edge)+'\t'+str(edges[edge])