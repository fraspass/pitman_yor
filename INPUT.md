## Network-wide anomaly detection using the Pitman-Yor process

This reposit contains Python code used to perform network-wide anomaly detection using the Pitman-Yor process in a computer network. 

A computer network can be interpreted as a directed graph $\mathbb{G}=(V,E)$, where $V$ is the node set of computers and $E\subseteq V\otimes V$ is the edge set of observed unique connections. 

Let us assume that $x_1,x_2,\dots,x_N$ is a sequence of source computers that have connected to a destination computer $y\in V$. The probability that the co

The PPPF implied by the Pitman-Yor process is:

$$
p_{X_{n+1}|X_n,\dots,X_1}(x_{n+1})=\frac{\alpha + dK_n}{\alpha+n}G_0(x_{x+1})
$$

