#! /usr/bin/env python
import sys
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-a","--alpha",type=float,dest="alpha", metavar="FLOAT",default=1.0)
parser.add_argument("--redteam",action="store_true")
args = parser.parse_args()
alpha=args.alpha

### MAP-REDUCE: compute the minimum p-value for each edge

## MAPPER:
# - input: string "destination computer \t source computer \t left_pval \t right_pval"
# - output: string "source computer _ destination computer \t left_pval _ right_pval"

for line in sys.stdin:
    x=line.strip().split(",")
    src_computer = x[1]
    dst_computer = x[0]
    lpval = x[2]
    rpval = x[3]
    print src_computer+"_"+dst_computer+"\t"+lpval+"_"+rpval

