## Network-wide anomaly detection using the Pitman-Yor process

This reposit contains Python code used to perform network-wide anomaly detection using the Pitman-Yor process in a computer network. 

A computer network can be interpreted as a directed graph $\mathbb{G}=(V,E)$, where $V$ is the node set of computers and $E\subseteq V\otimes V$ is the edge set of observed unique connections. 

Let us assume that $x_1,x_2,\dots,x_N$ is a sequence of source computers that have connected to a destination computer $y\in V$. For the given destination computer $y$, we assume that the exchangeable sequence of source computers has the following hierarchical distribution:
\begin{align*}
 x_i\vert G&\overset{iid}{\sim} G,\ i=1,\dots,N \\
 G&\overset{d}{\sim}\mathrm{PY}(\alpha,d,G_0)
\end{align*}

The PPPF implied by the Pitman-Yor process is:

$$
p_{X_{n+1}|X_n,\dots,X_1}(x_{n+1})=\frac{\alpha + dK_n}{\alpha+n}G_0(x_{n+1}) + \sum_{j=1}^{K_n} \frac{N_{jn}-d}{\alpha + n}
$$

