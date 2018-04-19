#!/usr/bin/env python
import sys
import argparse
from collections import Counter
global alpha,d,k,n,num_categories,alpha_star,ranks,category_counts

### MAP-REDUCE: compute the p-values for each connection associated with a given destination computer

## Sorting:
# - primary sorting on the destination node
# - secondary sorting on the arrival time on the event

## REDUCER:
## - input: string "destination computer \t arrival time \t source computer" from output of the mapper 
## - output: string "source computer \t destination computer \t left_pvalue \t right_pvalue" 
## From left_pvalue and right_pvalue one can compute the mid-p-value

## PARSER to give parameter values from the MapReduce call --> modifications to the code
## are necessary if this is used (the parameter values are obtained from two .txt files)
parser = argparse.ArgumentParser()
parser.add_argument("-a","--alpha",type=float,dest="alpha", metavar="FLOAT",default=1.0)
parser.add_argument("-d","--disc",type=float,dest="d", metavar="FLOAT",default=0.0)
parser.add_argument("-k","--classes",type=int,dest="k", metavar="INT",default=0)
parser.add_argument("--redteam",action="store_true")
args = parser.parse_args()
alpha = args.alpha
d = args.d
k = args.k

#### Description
# - alpha --> prior strength (in-degree of the node in the paper)
# - d --> prior discount parameter
# - k --> dimension of the node set
# - n --> n-th customer
# - num_categories --> number of unique nodes that have connected to the destination node at n
# - alpha_star --> alpha + n
# - ranks --> list of unique nodes that have connected to the given node at n
# - category_counts --> list of number of connections for each element in ranks

### File containing the estimated alpha parameters
degrees = {}
try:
    degree_file = open("alpha.txt")
    for line in degree_file:
        x = line.strip("\n").split("\t")
        degrees[x[1]] = float(x[0])
except:
    None

### File containing the discount parameters
discount = {}
try:
    disc_file = open("d.txt")
    for line in disc_file:
        x = line.strip().split("\t")
        discount[x[1]] = float(x[0])
except:
    None

# Reset function
def reset():
    global alpha,d,k,n,num_categories,alpha_star,ranks,category_counts
    category_counts=Counter()
    ranks=[]
    num_categories=0
    alpha_star=alpha
    n=0
      
# Pitman-Yor p-values
def py_pvalue(x):
    global alpha,d,k,n,num_categories,alpha_star,ranks,category_counts
    # If the link is new
    if x not in ranks:
    	# p-values --> all the nodes not yet observed
        cum_alpha = alpha + d * num_categories
        # If node set is not empty
        if k > 0:
        	# Multiply cum_alpha by the number of unobserved nodes and divide by 
        	# the dimension of the node set
            cum_alpha *= (k - num_categories) / float(k)
        # Divide by alpha_star to get the right p-value
        right_pvalue = cum_alpha/alpha_star
        left_pvalue = 0
        # Increase the category count for the new link
        category_counts[x] = 1
        # Add ranks
        ranks.append(x)
        # Rank of the previous observation (position)
        old_rank=len(ranks) - 1
        # Increase the number of categories by 1
        num_categories += 1
    else:
    	# Frequency of the sampled category
        prev_freq = category_counts[x]
        # Total in the cumulative sum
        total = 0
        # Look down from top rank --> how UNLIKELY (compute p-value from the other side)
        rank = 0 
        # While the category counts are less than the counts for the sampled category
        while prev_freq < category_counts[ranks[rank]]:
        	# Increase the total number (numerator) and discount using d
            total += category_counts[ranks[rank]] - d
            # Increase the rank
            rank += 1
        # If the node set is not empty
        if k > 0:
            # Add alpha*(1/(dimension node set)) times the number of ranks in the while loop
            # and include the discounting parameter
            total += (alpha + d * num_categories) * rank / float(k)
        # Initialise the value for the ties
        tie_total =0
        # Set the value of rank to the total value of the ranks
        lower_rank = rank
        # While the lower_rank is lower than the number of categories and 
        # the frequency of the sampled category is the same as the category count for the rank
        while lower_rank < num_categories and prev_freq == category_counts[ranks[lower_rank]]:
            # Increase the tie_total by the category count (prev_freq) and discount using d
            tie_total += category_counts[ranks[lower_rank]] - d
            # If the sampled x corresponds to lower_rank
            if x == ranks[lower_rank]:
            	# Set current_rank to lower_rank
                current_rank = lower_rank
            # Increase lower_rank
            lower_rank += 1
        # If the node set is not empty
        if k > 0:
        	# Add alpha times the difference between the rank and the ties, divided by 
        	# the dimension of the node set, and discount using d
            tie_total += (alpha + d * num_categories) * (lower_rank - rank) / float(k)
        # cum_alpha is alpha_star - total (ties should not be counted)
        cum_alpha = alpha_star - total
        # Obtain the right p-value (exclude ties)
        right_pvalue = cum_alpha / alpha_star
        # Obtain the left p-value (include the counts)
        left_pvalue = (cum_alpha-tie_total) / alpha_star
        # Increase the category count for x
        category_counts[x] += 1
        # Set the new_rank to current_rank
        new_rank = current_rank
        # Update the ranks
        while new_rank > 0 and category_counts[ranks[new_rank-1]] == prev_freq:
            new_rank -= 1
        if new_rank < current_rank:
            ranks.insert(new_rank,ranks.pop(current_rank))
    # Increase the number of observations
    n += 1
    # Increase alpha_star
    alpha_star += 1
    # Return the left and right p-values
    return [left_pvalue,right_pvalue]

# Empty old key
old_key = ""
for line in sys.stdin:
    # Strip and split the line
    key,time,value = line.strip().split("\t")
    # If a new key is observed
    if key != old_key:
        # Set the value of old_key to the observed key
        old_key = key
        # Compute alpha and d
        try:
            alpha = float(degrees[key])
            d = float(discount[key])
        except:
            None
        # Reset the values used with the previous key
        reset()
    print ",".join([value,key] + map(str, py_pvalue(value)))
