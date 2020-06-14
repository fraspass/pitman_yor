#!/usr/bin/env python
import sys
import math
import numpy as np
from scipy.optimize import root
from numpy import count_nonzero
from collections import Counter

## Parser for hyperparameter to return to file 
import argparse
parser = argparse.ArgumentParser()
# Decision in case of problems in the optimisation of phi: 
parser.add_argument("-t","--tmin",type=float,dest="tmin",default=0.0)
parser.add_argument("-z","--zeta",type=int,dest="zeta", metavar="INT",default=16230)
parser.add_argument("-train","--training",type=int,dest="train", metavar="INT",default=58)
args = parser.parse_args()

## Starting time
tmin = args.tmin
train = args.train
zeta = args.zeta

# Construct the source computer list (dictionary) + arrival times
dest_comp = {}
for line in sys.stdin:
	# Strip and split the dataline
	d = line.strip().split(",")
	try:
		# Obtain the (src,dst) pair
		user = d[3]
		computer = d[4]
		if (float(d[0])-tmin) < (train*86400.0):
			if computer not in dest_comp:
				dest_comp[computer] = [user]
			else:
				dest_comp[computer] += [user]
	except:
		continue

## Define a function to get the hyperparameter values from a set of weights / number of connections
def get_hyperparameters(x):
	# Compute N, K and H
	N = sum(x)
	K = len(x)
	K_star = float(np.log(1-K/float(zeta))/np.log(1-1.0/zeta))
	H = K - count_nonzero([i-1 for i in x])
	H_star = H*(float(zeta)/float(zeta-1))**(K_star-1) if H != 0 else 0
	alpha_diri = K_star / math.log(N) if N != 1 else K_star
	alpha_diri_obs = K / math.log(N) if N != 1 else K
	# Define a temporary psi_star_joint for the joint optimisation (log-transformation)
	def psi_star_joint(para): 
		alpha = para[0]
		d = para[1] 
		result = np.array([(math.lgamma(1+alpha) - math.lgamma(d+alpha) + d*math.log(N) - math.log(d) - math.log(K_star+alpha/d)) if alpha > 0 and d > 0 and d < 1 else -100,
						((H_star-alpha)/K_star-d) if alpha > 0 and d > 0 and d < 1 else -100])
		return result
	def psi_star_joint_observed(para): 
		alpha = para[0]
		d = para[1] 
		result = np.array([(math.lgamma(1+alpha) - math.lgamma(d+alpha) + d*math.log(N) - math.log(d) - math.log(K+alpha/d)) if alpha > 0 and d > 0 and d < 1 else -100,
						((H-alpha)/K-d) if alpha > 0 and d > 0 and d < 1 else -100])
		return result
	# Compute alpha
	if H != 0:
		para_out = root(psi_star_joint, np.array([K_star/math.log(N),H_star/K_star]) if N != 1 else [K_star,0.0])
		para_out_obs = root(psi_star_joint_observed, np.array([K/math.log(N),H/K]) if N != 1 else [K,0.0])
		# If optimisation for alpha is unsuccessful, return the appropriate values according to -err, 
		# Otherwise use the optimised value
		if para_out.success and para_out.x[0] > 0 and para_out.x[1] > 0 and para_out.x[1] < 1:
			alpha = para_out.x[0] 
			d = para_out.x[1]
		else:
			d = H_star / K_star
			# Define a temporary psi_star function for the optimisation of alpha only
			def psi_star(alpha): 
				result = (math.lgamma(1+alpha) - math.lgamma(d+alpha) + d*math.log(N) - math.log(d) - math.log(K_star+alpha/d)) if alpha > 0 else -100
				return result
			alpha_out = root(psi_star, K_star/math.log(N) if N != 1 else K_star)
			alpha = alpha_out.x[0] if alpha_out.success else K_star/math.log(N) if N != 1 else K_star
		## Repeat for the observed values
		if para_out_obs.success and para_out_obs.x[0] > 0 and para_out_obs.x[1] > 0 and para_out_obs.x[1] < 1:
			alpha_obs = para_out_obs.x[0] 
			d_obs = para_out_obs.x[1]
		else:
			d_obs = H / K
			# Define a temporary psi_star function for the optimisation of alpha only
			def psi_star_observed(alpha): 
				result = (math.lgamma(1+alpha) - math.lgamma(d+alpha) + d*math.log(N) - math.log(d) - math.log(K+alpha/d)) if alpha > 0 else -100
				return result
			alpha_out_obs = root(psi_star_observed, K/math.log(N) if N != 1 else K)
			alpha_obs = alpha_out_obs.x[0] if alpha_out_obs.success else K/math.log(N) if N != 1 else K
	else:
		d = 0
		d_obs = 0
		alpha = K_star/math.log(N) if N != 1 else K_star
		alpha_obs = K/math.log(N) if N != 1 else K
	# Return the parameter values
	return [N,K,K_star,H,H_star,alpha,d,alpha_obs,d_obs,alpha_diri,alpha_diri_obs]

## Apply the function on the LANL graph and obtain the parameter values
param_array = {}
for computer in dest_comp.keys():
	param_array[computer] = get_hyperparameters(Counter(dest_comp[computer]).values())

## Calculate the mean for popular nodes
py_sum_alpha = []
py_sum_d = []
for computer in param_array.keys():
	if param_array[computer][2] > 100:
		py_sum_alpha += [param_array[computer][0]]
		py_sum_d += [param_array[computer][1]]

## Calculate the mean
py_mean_alpha = np.median(py_sum_alpha)
py_mean_d = np.median(py_sum_d)

## Modify the results to take into account uncommon destination computers
for computer in param_array.keys():
	if param_array[computer][2] <= 100:
		string_comp = param_array[computer]
		string_comp[0] = py_mean_alpha
		string_comp[1] = py_mean_d
		param_array[computer] = string_comp

## Print the output
for computer in param_array.keys():
	u = param_array[computer] 
	print computer + "\t" + "\t".join([str(x) for x in u])