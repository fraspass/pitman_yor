# Network-wide anomaly detection using Pitman-Yor processes

This reposit contains Python code used to perform network-wide anomaly detection in a computer network using the two parameter Poisson-Dirichlet or Pitman-Yor process (Pitman and Yor, 1997). 

This code builds up on the Hadoop-MapReduce procedure described in Heard and Rubin-Delanchy (2016). The Dirichlet process described by the authors in the paper is extended to include an extra parameter, which allows for more flexibility when modelling data exhibiting power-law behaviour.

## References

* Heard, N.A. and Rubin-Delanchy, P. (2016), "Network-wide anomaly detection via the Dirichlet process", Proceedings of IEEE workshop on Big Data Analytics for Cyber-Security Computing. ([Link](https://ieeexplore.ieee.org/document/7745478/))

* Heard, N.A. and Rubin-Delanchy, P. (2018), "Choosing between methods of combining p-values", Biometrika 105(1), 239–246. ([Link](https://academic.oup.com/biomet/article-abstract/105/1/239/4788722?redirectedFrom=fulltext))

* Kent, A.D. (2016), ”Cybersecurity data sources for dynamic network research”, In Dynamic Networks and Cyber-Security. World Scientific. ([Link](https://www.worldscientific.com/doi/abs/10.1142/9781786340757_0002))([Data](https://csr.lanl.gov/data/cyber1/))

* Pitman, J. and Yor, M. (1997), "The two-parameter Poisson-Dirichlet distribution derived from a stable sub-ordinator", Annals of Probability 25, 855-900. ([Link](https://projecteuclid.org/euclid.aop/1024404422))


