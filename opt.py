#!/usr/bin/env python
import math
import pandas as pd
from scipy.optimize import root
from numpy import count_nonzero

## Parser for hyperparameter to return to file 
import argparse
parser = argparse.ArgumentParser()
# Hyperparameter to return. Options -alpha, -d, -both, -K, -H, or -all
parser.add_argument("-r","--ret",type=str,dest="ret",default="both")
# Decision in case of problems in the optimisation of phi: 
# - -deg returns the indegree for alpha (Heard, Rubin-Delanchy)
# - -logdeg returns the indegree divided by log(N) (DEFAULT)
parser.add_argument("-e","--err",type=str,dest="err",default="logdeg")
args = parser.parse_args()

## Allow only for specific values of -r
options_r = ["alpha","d","both","K","N","H","all"]
ret = "both" if args.ret not in options_r else args.ret

## Allow only for specific values of -e
options_e = ["deg","logdeg"]
err = "logdeg" if args.err not in options_e else args.err

## Import the LANL authentication graph (already preprocessed: edge list with weights given by the number
## of observations on the edge)
lanl_graph = pd.read_csv("lanl_graph.txt", sep="\t", names=["src","dst","n"])

## Define a function to get the hyperparameter values from a set of weights / number of connections
def get_hyperparameters(x):
	# Compute N, K and H
	N = sum(x)
	K = len(x)
	H = K - count_nonzero([i-1 for i in x])
	# Compute d
	d = H/float(K)
	# Define a temporary psi (log-transformation)
	def psi(alpha): 
		return math.lgamma(1+alpha) - math.lgamma(d+alpha) + d*math.log(N) - math.log(H) 
	# Compute alpha
	if H != 0:
		alpha_out = root(psi, K/math.log(N) if N != 1 else K)
		# If optimisation for alpha is unsuccessful, return the appropriate values according to -err, 
		# otherwise use the optimised value
		alpha = alpha_out.x[0] if alpha_out.success == True and alpha_out.x[0] > 0 else K/math.log(N) if N != 1 and \
			err == "logdeg" else K 
	else: 
		alpha = K/math.log(N) if N != 1 and err == "logdeg" else K 
	# Return the parameter values according to -ret
	if ret == "alpha": 
		return alpha 
	else: 
		if ret == "d":
			return d 
		else: 
			if ret == "both": 
				return [alpha,d] 
			else: 
				if ret == "K": 
					return K 
				else: 
					if ret == "H": 
						return H 
					else: 
						if ret == "N": 
							return N 
						else: 
							if ret == "all": 
								return [alpha,d,K,H,N]

## Apply the function on the LANL graph and obtain the parameter values
param_array = (lanl_graph.groupby("dst")["n"].agg([get_hyperparameters]))["get_hyperparameters"]

## Print the output
for computer in param_array.index:
	u = param_array[computer]
	if ret == "both" or ret == "all": 
		print "\t".join(map(str,u))+"\t"+computer
	else:
		print str(u)+"\t"+computer
