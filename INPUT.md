# Network-wide anomaly detection using Pitman-Yor processes

This reposit contains Python code used to perform network-wide anomaly detection using the two parameter Poisson-Dirichlet or Pitman-Yor process (Pitman and Yor, 1997) in a computer network. 

This code builds up on the Hadoop-MapReduce procedure described in Heard and Rubin-Delanchy (2016). The Dirichlet process described by the authors in the paper is extended to include an extra parameter, which allows for more flexibility when modelling data exhibiting power-law behaviour.

## Methodology

### The Pitman-Yor process

A computer network can be interpreted as a directed graph $\mathbb{G}=(V,E)$, where $V$ is the node set of computers and $E\subseteq V\otimes V$ is the edge set of observed unique connections. 

Let us assume that $x_1,x_2,\dots,x_N$ is a sequence of source computers that have connected to a destination computer $y\in V$. For the given destination computer $y$, we assume that the exchangeable sequence of source computers has the following hierarchical distribution:
\begin{align*}
 x_i\vert G&\overset{iid}{\sim} G,\ i=1,\dots,N \\
 G&\overset{d}{\sim}\mathrm{PY}(\alpha,d,G_0)
\end{align*}

The PPPF implied by the Pitman-Yor process is:
$$ p_{X_{n+1}|X_n,\dots,X_1}(x_{n+1})=\frac{\alpha + dK_n}{\alpha+n}G_0(x_{n+1}) + \sum_{j=1}^{K_n} \frac{N_{jn} - d}{\alpha + n} \delta_{x_j^\star}(x_{n+1}) $$

Therefore, the $p$-value for the $(n+1)$-th observation is: 
$$ p_{n+1} = \sum_{x\in V:\phi_n(x)\leq\phi_n(x_{n+1})} \frac{\phi_n(x)}{\alpha+n}, $$
where:
$$ \phi_n(u) = (\alpha-dK_n)G_0(u) + \sum_{i=1}^n \mathbb I\{x_i=u\} - d . $$

The code also uses mid-$p$-values $q_{n+1}=p_{n+1}+p_{n+1}^\star$, where:
$$ p_{n+1}^\star = \sum_{x\in V:\phi_n(x)<\phi_n(x_{n+1})} \frac{\phi_n(x)}{\alpha+n}. $$

The mid-$p$-values might be preferable since the distribution of the source nodes is discrete. 


### Combining p-values

The $p$-values $p_1,p_2,\dots,p_N$ obtained for each observed connection $x\to y,\ x,y\in V$ having $y$ as destination computer can be combined in this code using 6 different methods, described in Heard and Rubin-Delanchy (2018):

* Edgington's method
\begin{align*}
S_E = \sum_{i=1}^N p_i & & S_E\overset{d}{\rightarrow}\mathbb N\left(\frac{N}{2},\frac{N}{12}\right), 
\end{align*}

* Fisher's method - let $E_x=\{(x,y):y\in V\cap(x,y\in E)\}$, then:
\begin{align*} 
S_F = \sum_{i=1}^N \log(p_i) & & -2S_F\overset{d}{\sim}\chi^2_{2\vert E_x\vert},
\end{align*}

* Pearson's method
\begin{align*}
S_P = -\sum_{i=1}^N \log(1-p_i) & & 2S_P\overset{d}{\sim}\chi^2_{2\vert E_x\vert},
\end{align*}

* George's method 
\begin{align*}
S_G = S_F + S_P = \sum_{i=1}^N \log\left(\frac{p_i}{1-p_i}\right) & &\sqrt{\frac{3(5N+4)}{N(5N+2)}}\frac{S_G}{\pi}\overset{d}{\sim}t_{5N+4}, 
\end{align*}

* Stouffer's method - let $\Phi^{-1}(\cdot)$ denote the inverse of the CDF $\Phi(\cdot)$ of a standard normal distribution, then:
\begin{align*}
S_F = \sum_{i=1}^N \Phi^{-1}(p_i) & & S_S\overset{d}{\sim}\mathbb N\left(0,n\right),
\end{align*}

* Tippett's method (or minimum $p$-value) method 
\begin{align*}
S_T = \min\{p_1,\dots,p_N\} & & S_T\overset{d}{\sim}\mathrm{Beta}(1,N)
\end{align*}

*Note that the distributional results are only valid under normal behaviour of the network.*

# References

* Heard, N.A. and Rubin-Delanchy, P. (2016), "Network-wide anomaly detection via the Dirichlet process", Proceedings of IEEE workshop on Big Data Analytics for Cyber-Security Computing.

* Heard, N.A. and Rubin-Delanchy, P. (2018), "Choosing between methods of combining p-values", Biometrika 105(1), 239–246.

* Pitman, J. and Yor, M. (1997), "The two-parameter Poisson-Dirichlet distribution derived from a stable sub-ordinator", Annals of Probability 25, 855-900.


