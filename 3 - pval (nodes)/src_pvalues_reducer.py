#! /usr/bin/env python
import sys

from numpy import log,sqrt,exp,pi,inf
from scipy.stats import norm,chi2,beta,t
import numpy as np 
np.seterr(divide='ignore')

##### MAPPER --> identity

##### REDUCER 
# - input: sequence of source nodes with corresponding (log-transformed) minimum p-value and minimum mid-p-value 
#          obtained using different combiners on each edge (separator: "\t")
# - output: source node, outdegree and combined (log-transformed) p-values using Edgington, Fisher, Pearson, George, 
#           Stouffer and Tippett methods (see Heard and Rubin-Delanchy, Biometrika (2018) for a description of the methods)

### Example of input: 
## C15244   C10093  2   -4.93221659052  -4.93221659052   ...  -7.11943339313  -7.81247938472
## String of the type src - dst - # obs on edge - edg pvals - fish pvals - pears pvals - george pvals - stouf pvals - min pvals
## where for each method the standard p-value and the mid-p-value have been computed

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-p","--ptype",type=str,dest="ptype", \
    help="Specifies which p-value from previous analysis should be used.", default="tippett")
args = parser.parse_args()
ptype = args.ptype

#### Options for ptype (p-value from previous analysis which is used)
# - "edgington" for Edgington's log-p-value and log-mid-p-value
# - "fisher" for Fisher's log-p-value and log-mid-p-value 
# - "pearson" for Pearson's log-p-value and log-mid-p-value 
# - "george" for George's log-p-value and log-mid-p-value 
# - "stouffer" for Stouffer's log-p-value and log-mid-p-value
# - *** DEFAULT *** "tippett" OR "min" OR "minimum" for Tippett's log-p-value and log-mid-p-value (minimum p-value method)

## Only allow for 4 different p-value types, otherwise set to default
ptype_opts = ["edgington","fisher","pearson","george","stouffer","tippett","min","minimum"]
ptype = "tippett" if ptype not in ptype_opts else ptype
ptype = "tippett" if ptype == "min" or ptype == "minimum" else ptype

## Select indices
if ptype == "edgington": v = [3,4]
if ptype == "fisher": v = [5,6]
if ptype == "pearson": v = [7,8]
if ptype == "george": v = [9,10]
if ptype == "stouffer": v = [11,12]
if ptype == "tippett": v = [13,14]

## Initialise the key
old_key = ""
## Read from stdin
for line in sys.stdin:
    x = line.strip().split("\t")
    key = x[0]
    log_pval = float(x[v[0]])
    log_mid_pval = float(x[v[1]])
    if key != old_key:
        if old_key != "":
            ## Edgington p-value (normal approximation - extremely good even for n=4)
            edgington_pval = norm.logcdf(sqrt(12.0/n)*(sum_pvals_edg-.5*n))
            mid_edgington_pval = norm.logcdf(sqrt(12.0/n)*(sum_mid_pvals_edg-.5*n))
            ## Fisher p-value
            fisher_pval = chi2.logsf(-2*sum_pvals_fisher,2*n)
            mid_fisher_pval = chi2.logsf(-2*sum_mid_pvals_fisher,2*n)
            # fish_std = (sum_mid_pvals_fisher+n)/sqrt(n)
            ## Pearson p-value *** CHANGE OF SIGN wrt Biometrika paper ***
            pearson_pval = chi2.logcdf(2*sum_pvals_pearson,2*n)
            mid_pearson_pval = chi2.logcdf(2*sum_mid_pvals_pearson,2*n)
            ## Mudholkar and George p-value (scaled Student's t approximation)
            george_pval = t.logcdf(sqrt(3.0/n*(5.0*n+4.0)/(5.0*n+2.0))/pi*(sum_pvals_pearson + sum_pvals_fisher),5*n+4)
            mid_george_pval = t.logcdf(sqrt(3.0/n*(5.0*n+4.0)/(5.0*n+2.0))/pi*(sum_mid_pvals_fisher + sum_mid_pvals_pearson),5*n+4)
            ## Stouffer's p-value
            stouffer_pval = norm.logcdf(sum_pvals_stouffer/sqrt(n))
            mid_stouffer_pval = norm.logcdf(sum_mid_pvals_stouffer/sqrt(n))
            ## Tippett's p-value
            tippett_pval = beta.logcdf(exp(tippett_min),1,n)
            tippett_mid_pval = beta.logcdf(exp(tippett_mid_min),1,n)
            ## Print to console
            print old_key+"\t"+ptype+"\t"+"\t".join(map(str,[n, edgington_pval,mid_edgington_pval, \
                fisher_pval,mid_fisher_pval,pearson_pval,mid_pearson_pval, george_pval, mid_george_pval, \
                stouffer_pval, mid_stouffer_pval, tippett_pval, tippett_mid_pval])) 
        ## Reset 
        old_key = key
        n = 0
        ## Reset the sums of p-values
        sum_pvals_edg = sum_mid_pvals_edg = 0
        sum_pvals_fisher = sum_mid_pvals_fisher = 0
        sum_pvals_pearson = sum_mid_pvals_pearson = 0
        sum_pvals_stouffer = sum_mid_pvals_stouffer = 0
        tippett_min = tippett_mid_min = 1
    # Increase n
    n += 1
    # Edgington p-values
    sum_pvals_edg += exp(log_pval)
    sum_mid_pvals_edg += exp(log_mid_pval)
    # Fisher p-values
    sum_pvals_fisher += log_pval
    sum_mid_pvals_fisher += log_mid_pval
    # Pearson p-values
    sum_pvals_pearson -= log(1-exp(log_pval))
    sum_mid_pvals_pearson -= log(1-exp(log_mid_pval))
    # Stouffer p-values
    sum_pvals_stouffer += norm.ppf(exp(log_pval))
    sum_mid_pvals_stouffer += norm.ppf(exp(log_mid_pval))
    # Tippett p-values 
    tippett_min = log_pval if log_pval < tippett_min else tippett_min
    tippett_mid_min = log_mid_pval if log_mid_pval < tippett_mid_min else tippett_mid_min

## Print and calculate combined p-values for last node
if old_key != "":
    ## Edgington p-value (normal approximation - extremely good even for n=4)
    edgington_pval = norm.logcdf(sqrt(12.0/n)*(sum_pvals_edg-.5*n))
    mid_edgington_pval = norm.logcdf(sqrt(12.0/n)*(sum_mid_pvals_edg-.5*n))
    ## Fisher p-value
    fisher_pval = chi2.logsf(-2*sum_pvals_fisher,2*n)
    mid_fisher_pval = chi2.logsf(-2*sum_mid_pvals_fisher,2*n)
    # fish_std = (sum_mid_pvals_fisher+n)/sqrt(n)
    ## Pearson p-value
    pearson_pval = chi2.logcdf(2*sum_pvals_pearson,2*n)
    mid_pearson_pval = chi2.logcdf(2*sum_mid_pvals_pearson,2*n)
    ## Mudholkar and George p-value (scaled Student's t approximation)
    george_pval = t.logcdf(sqrt(3.0/n*(5.0*n+4.0)/(5.0*n+2.0))/pi*(sum_pvals_fisher + sum_pvals_pearson),5*n+4)
    mid_george_pval = t.logcdf(sqrt(3.0/n*(5.0*n+4.0)/(5.0*n+2.0))/pi*(sum_mid_pvals_fisher + sum_mid_pvals_pearson),5*n+4)
    ## Stouffer's p-value
    stouffer_pval = norm.logcdf(sum_pvals_stouffer/sqrt(n))
    mid_stouffer_pval = norm.logcdf(sum_mid_pvals_stouffer/sqrt(n))
    ## Tippett's p-value
    tippett_pval = beta.logcdf(exp(tippett_min),1,n)
    tippett_mid_pval = beta.logcdf(exp(tippett_mid_min),1,n)
    ## Print to console
    print old_key+"\t"+ptype+"\t"+"\t".join(map(str,[n, edgington_pval,mid_edgington_pval, \
        fisher_pval,mid_fisher_pval,pearson_pval,mid_pearson_pval, george_pval, mid_george_pval, \
        stouffer_pval, mid_stouffer_pval, tippett_pval, tippett_mid_pval]))
