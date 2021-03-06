# Modelling dynamic network evolution as a Pitman-Yor process

The model and datasets are described in *Sanna Passino, F. and Heard, N. A., "Modelling dynamic network evolution as a Pitman-Yor process", Foundations of Data Science, 2019, 1(3):293-306* ([link to the journal publication](https://www.aimsciences.org/article/doi/10.3934/fods.2019013)). 

This repository contains Python code used to perform network-wide anomaly detection in a computer network using the two parameter Poisson-Dirichlet or Pitman-Yor process (Pitman and Yor, 1997). 

This code builds up on the Hadoop-MapReduce procedure described in Heard and Rubin-Delanchy (2016). The Dirichlet process described by the authors in the paper is extended to include an extra parameter, which allows for more flexibility when modelling data exhibiting power-law behaviour.

## Methodology

### The Pitman-Yor process

A computer network can be interpreted as a directed graph $\mathbb{G}=(V,E)$, where $V$ is the node set of computers and $E\subseteq V\otimes V$ is the edge set of observed unique connections. 

Let us assume that $x_1,x_2,\dots,x_N$ is a sequence of source computers that have connected to a destination computer $y\in V$. For the given destination computer $y$, we assume that the exchangeable sequence of source computers has the following hierarchical distribution:
\begin{align*}
 x_i\vert G &\overset{iid}{\sim} G,\ i=1,\dots,N \\
 G &\overset{d}{\sim} \mathrm{PY}(\alpha,d,G_0)
\end{align*}

The PPPF implied by the Pitman-Yor process is:
$$ p_{X_{n+1}|X_n,\dots,X_1}(x_{n+1})=\frac{\alpha + dK_n}{\alpha+n}G_0(x_{n+1}) + \sum_{j=1}^{K_n} \frac{N_{jn} - d}{\alpha + n} \delta_{x_j^\star}(x_{n+1}) $$

where $K_n$ is the number of unique source computers that have connected to $y$ up to time $n$, and $N_{jn},\ j=1,\dots,K_n$ is the number of times the source computer $x_j^\star,\ j=1,\dots,K_n$ has connected to $y$ in the fist $n$ observed connections to the destination computer. 

Therefore, the $p$-value for the $(n+1)$-th observation is: 
$$ p_{n+1} = \sum_{x\in V:\phi_n(x)\leq\phi_n(x_{n+1})} \frac{\phi_n(x)}{\alpha+n}, $$
where:
$$ \phi_n(u) = (\alpha-dK_n)G_0(u) + \sum_{i=1}^n \mathbb I\{x_i=u\} - d. $$

The code also uses mid-$p$-values $q_{n+1}=(p_{n+1}+p_{n+1}^\star)/2$, where:
$$ p_{n+1}^\star = \sum_{x\in V:\phi_n(x)<\phi_n(x_{n+1})} \frac{\phi_n(x)}{\alpha+n} . $$

The mid-$p$-values might be preferable since the distribution of the source nodes is discrete. 

### Combining p-values

A sequence of $p$-values $p_1,p_2,\dots,p_N$ can be combined in this code using 6 different methods, described in Heard and Rubin-Delanchy (2018):

* Edgington's method:
\begin{align*}
S_E = \sum_{i=1}^N p_i & & S_E\overset{d}{\rightarrow}\mathbb N\left(\frac{N}{2},\frac{N}{12}\right) , 
\end{align*}

* Fisher's method - let $E_x=\{(x,y):y\in V\cap(x,y\in E)\}$, then:
\begin{align*} 
S_F = \sum_{i=1}^N \log(p_i) & & -2S_F\overset{d}{\sim}\chi^2_{2\vert E_x\vert} ,
\end{align*}

* Pearson's method:
\begin{align*}
S_P = -\sum_{i=1}^N \log(1-p_i) & & 2S_P\overset{d}{\sim}\chi^2_{2\vert E_x\vert} ,
\end{align*}

* George's method: 
\begin{align*}
S_G = S_F + S_P = \sum_{i=1}^N \log\left(\frac{p_i}{1-p_i}\right) & &\sqrt{\frac{3(5N+4)}{N(5N+2)}}\frac{S_G}{\pi}\overset{d}{\rightarrow}t_{5N+4} , 
\end{align*}

* Stouffer's method - let $\Phi^{-1}(\cdot)$ denote the inverse of the CDF $\Phi(\cdot)$ of a standard normal distribution, then:
\begin{align*}
S_F = \sum_{i=1}^N \Phi^{-1}(p_i) & & S_S\overset{d}{\sim}\mathbb N\left(0,n\right) ,
\end{align*}

* Tippett's method (or minimum $p$-value) method: 
\begin{align*}
S_T = \min\{p_1,\dots,p_N\} & & S_T\overset{d}{\sim}\mathrm{Beta}(1,N)
\end{align*}

*Note that the distributional results are only valid under normal behaviour of the network.*

### Anomaly detection

In the code, the $p$-values and mid-$p$-values are combined in two different stages. Suppose that for a given destination computer $y\in V$, the $p$-values (and mid-$p$-values) $p_1,\dots,p_N$ corresponding to each observed connection are computed using the PY posterior predictive probability.

* for all the connections on a given edge $x\to y$, it is possible to combine the $p$-values and obtain a grouped $p$-value $p_{xy}$ for each edge,

* given the $p$-values $p_{xy}$ for each edge, it is possible to combine the $p$-values $p_{xy_1},\dots,p_{xy_x}$ for a given source computer $x$, in order to obtain a $p$-value for each source computer.

The $p$-values computed at the second stage give an anomaly score for the source node $x$, which can be used for anomaly detection. 

## Usage

### Data preprocessing

An example of a data line in the LANL authentication dataset (Kent, 2016) is:

```
1,C608@DOM1,C608@DOM1,C608,C467,Kerberos,Network,LogOn,Success
```

The following command returns the edge list `lanl_graph.txt` with tab sepearated source and destination, and weights given by the number of observed connections on each edge:

```
hadoop fs -text MY_FOLDER/auth.txt.gz | ./get_auth_graph.py > lanl_graph.txt
```

Given the LANL edge list, it is possible to obtain method of moments estimates of the hyperparameters $ \alpha $ and $ d $ using the code in `py_parameters.py`:

```
cat lanl_graph.txt | ./py_parameters.py
```

### Hadoop procedures

The first of the three Hadoop MapReduce procedures can be most simply run using the command:
```
./py_anon.sh &
```

where the anonymised file `py_anon.sh` in `1 - pvals (all)` is appropriately modified to give the correct -input and -output. Similar procedures can be carried out for the two remaining MapReduce procedures, using the `.sh` files in the folders `2 - pvals (edges)` and `3 - pvals (nodes)`. 

## References

* Sanna Passino, F. and Heard, N.A. (2019), "Modelling dynamic network evolution as a Pitman-Yor process", Foundations of Data Science, 2019, 1(3):293-306. ([Link](https://www.aimsciences.org/article/doi/10.3934/fods.2019013))

* Heard, N.A. and Rubin-Delanchy, P. (2016), "Network-wide anomaly detection via the Dirichlet process", Proceedings of IEEE workshop on Big Data Analytics for Cyber-Security Computing. ([Link](https://ieeexplore.ieee.org/document/7745478/))

* Heard, N.A. and Rubin-Delanchy, P. (2018), "Choosing between methods of combining p-values", Biometrika 105(1), 239–246. ([Link](https://academic.oup.com/biomet/article-abstract/105/1/239/4788722?redirectedFrom=fulltext))

* Kent, A.D. (2016), ”Cybersecurity data sources for dynamic network research”, In Dynamic Networks and Cyber-Security. World Scientific. ([Link](https://www.worldscientific.com/doi/abs/10.1142/9781786340757_0002))([Data](https://csr.lanl.gov/data/cyber1/))

* Pitman, J. and Yor, M. (1997), "The two-parameter Poisson-Dirichlet distribution derived from a stable sub-ordinator", Annals of Probability 25, 855-900. ([Link](https://projecteuclid.org/euclid.aop/1024404422))


