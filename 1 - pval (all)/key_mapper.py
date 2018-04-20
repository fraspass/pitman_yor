#!/usr/bin/env python
import sys

## Parser for Red Team data (different format)
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--redteam",action="store_true")
args = parser.parse_args()

### MAP-REDUCE: compute the p-values for each connection associated with a given destination computer

## Sorting:
# - primary sorting on the destination node
# - secondary sorting on the arrival time on the event

## MAPPER:
## - input: entire LANL user-authentication dataset (Kent, 2016)
## - output: string "destination computer \t arrival time \t source computer"

for line in sys.stdin:
    x = line.strip().split(",")
    try:
    	src_computer = x[2 if args.redteam else 3]
        dst_computer = x[3 if args.redteam else 4]
    	time = x[0]
        print dst_computer+"\t"+time+"\t"+src_computer
    except:
        None
