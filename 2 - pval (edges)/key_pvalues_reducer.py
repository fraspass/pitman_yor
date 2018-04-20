#! /usr/bin/env python
import sys
from numpy import log,sqrt,pi,inf
from scipy.stats import norm,chi2,beta,t
import numpy as np 
np.seterr(divide='ignore')

### MAP-REDUCE: compute the minimum p-value for each edge

## REDUCER:
# - input: string "destination computer _ source computer \t left_pvalue _ right_pvalue"
# - output: string "source computer \t pvalue \t mid_pvalue" obtained using Edgington, Fisher, Pearson, \ 
#           George, Stouffer and Tippet methods

old_key = ""
for line in sys.stdin:
    ## Obtain the edge and the pvalues
    key, pvals = line.strip().split("\t")
    if key != old_key:
        if old_key != "":
            ## Edgington p-value (normal approximation - extremely good even for n=4)
            edgington_pval = norm.logcdf(sqrt(12.0/n)*(sum_pvals_edg-.5*n))
            mid_edgington_pval = norm.logcdf(sqrt(12.0/n)*(sum_mid_pvals_edg-.5*n))
            ## Fisher p-value
            fisher_pval = chi2.logsf(-2*sum_pvals_fisher,2*n)
            mid_fisher_pval = chi2.logsf(-2*sum_mid_pvals_fisher,2*n)
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
            tippett_pval = beta.logcdf(tippett_min,1,n)
            tippett_mid_pval = beta.logcdf(tippett_mid_min,1,n)
            ## Print to console
            print src+"\t"+dst+"\t"+"\t".join(map(str,[n, edgington_pval,mid_edgington_pval, \
                fisher_pval,mid_fisher_pval, pearson_pval, mid_pearson_pval, george_pval, mid_george_pval, \
                stouffer_pval, mid_stouffer_pval, tippett_pval, tippett_mid_pval]))
        ## Update new key
        old_key = key
        n = 0
        ## Reset the sums of p-values
        sum_pvals_edg = sum_mid_pvals_edg = 0
        sum_pvals_fisher = sum_mid_pvals_fisher = 0
        sum_pvals_pearson = sum_mid_pvals_pearson = 0
        sum_pvals_stouffer = sum_mid_pvals_stouffer = 0
        tippett_min = tippett_mid_min = 1
    # Compute source, destination and ovalues
    dst, src = key.strip().split("_")
    pvals = map(float,pvals.split("_"))
    ## Update when same key is used
    n += 1
    ## Compute pvalue and mid-pvalue
    pval = pvals[1]
    mid_pval = .5*sum(pvals)
    ## Edgington p-values
    sum_pvals_edg += pval
    sum_mid_pvals_edg += mid_pval
    ## Fisher p-values
    sum_pvals_fisher += log(pval)
    sum_mid_pvals_fisher += log(mid_pval)
    # Pearson p-values
    sum_pvals_pearson -= log(1-pval)
    sum_mid_pvals_pearson -= log(1-mid_pval)
    ## Stouffer p-values
    sum_pvals_stouffer += norm.ppf(pval)
    sum_mid_pvals_stouffer += norm.ppf(mid_pval)
    ## Tippett p-values 
    tippett_min = pval if pval < tippett_min else tippett_min
    tippett_mid_min = mid_pval if mid_pval < tippett_mid_min else tippett_mid_min
    

if old_key != "":
   ## Edgington p-value (normal approximation - extremely good even for n=4)
    edgington_pval = norm.logcdf(sqrt(12.0/n)*(sum_pvals_edg-.5*n))
    mid_edgington_pval = norm.logcdf(sqrt(12.0/n)*(sum_mid_pvals_edg-.5*n))
    ## Fisher p-value
    fisher_pval = chi2.logsf(-2*sum_pvals_fisher,2*n)
    mid_fisher_pval = chi2.logsf(-2*sum_mid_pvals_fisher,2*n)
    ## Pearson p-value
    pearson_pval = chi2.logcdf(2*sum_pvals_pearson,2*n)
    mid_pearson_pval = chi2.logcdf(2*sum_mid_pvals_pearson,2*n)
    ## Mudholkar and George p-value (scaled Student's t approximation)
    george_pval = t.logcdf(sqrt(3.0/n*(5.0*n+4.0)/(5.0*n+2.0))/pi*(sum_pvals_pearson + sum_pvals_fisher),5*n+4)
    mid_george_pval = t.logcdf(sqrt(3.0/n*(5.0*n+4.0)/(5.0*n+2.0))/pi*(sum_mid_pvals_fisher + sum_mid_pvals_pearson),5*n+4)        
    ## Stouffer's p-value
    stouffer_pval = norm.logcdf(sum_pvals_stouffer/sqrt(n))
    mid_stouffer_pval = norm.logcdf(sum_mid_pvals_stouffer/sqrt(n))
    ## Tippett's p-value
    tippett_pval = beta.logcdf(tippett_min,1,n)
    tippett_mid_pval = beta.logcdf(tippett_mid_min,1,n)
    ## Print to console
    print src+"\t"+dst+"\t"+"\t".join(map(str,[n, edgington_pval,mid_edgington_pval, \
        fisher_pval, mid_fisher_pval, pearson_pval, mid_pearson_pval, george_pval, mid_george_pval, \
        stouffer_pval, mid_stouffer_pval, tippett_pval, tippett_mid_pval]))
        
