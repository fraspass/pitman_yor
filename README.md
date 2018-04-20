# Network-wide anomaly detection using Pitman-Yor processes

This reposit contains Python code used to perform network-wide anomaly detection using the two parameter Poisson-Dirichlet or Pitman-Yor process (Pitman and Yor, 1997) in a computer network. 

This code builds up on the Hadoop-MapReduce procedure described in Heard and Rubin-Delanchy (2016). The Dirichlet process described by the authors in the paper is extended to include an extra parameter, which allows for more flexibility when modelling data exhibiting power-law behaviour.

## Methodology

### The Pitman-Yor process

A computer network can be interpreted as a directed graph <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/73dde20bcffb31b6177c5d21c5a96f6d.svg?invert_in_darkmode" align=middle width=78.37896pt height=24.6576pt/>, where <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/a9a3a4a202d80326bda413b5562d5cd1.svg?invert_in_darkmode" align=middle width=13.242075pt height=22.46574pt/> is the node set of computers and <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/94db391751ae0befe931ce025807b400.svg?invert_in_darkmode" align=middle width=81.575175pt height=22.46574pt/> is the edge set of observed unique connections. 

Let us assume that <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/93e8f48a97001313f47040c9f354a850.svg?invert_in_darkmode" align=middle width=98.415405pt height=14.15535pt/> is a sequence of source computers that have connected to a destination computer <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/3a49e7753441741b7224c79f23973f59.svg?invert_in_darkmode" align=middle width=41.982435pt height=22.46574pt/>. For the given destination computer <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/deceeaf6940a8c7a5a02373728002b0f.svg?invert_in_darkmode" align=middle width=8.6493pt height=14.15535pt/>, we assume that the exchangeable sequence of source computers has the following hierarchical distribution:
<p align="center"><img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/8200749748ae36b2058d9caafc3d8805.svg?invert_in_darkmode" align=middle width=170.67435pt height=52.86534pt/></p>

The PPPF implied by the Pitman-Yor process is:
<p align="center"><img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/aaeab5c4459e02c055b6e5bede16eaf1.svg?invert_in_darkmode" align=middle width=482.9319pt height=50.226165pt/></p>
where <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/96b697078d351b7b43bd5b5dce0254cd.svg?invert_in_darkmode" align=middle width=22.08723pt height=22.46574pt/> is the number of unique source computers that have connected to <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/deceeaf6940a8c7a5a02373728002b0f.svg?invert_in_darkmode" align=middle width=8.6493pt height=14.15535pt/> up to time <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/55a049b8f161ae7cfeb0197d75aff967.svg?invert_in_darkmode" align=middle width=9.867pt height=14.15535pt/>, and <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/168b2248f63c4d12aa19fcf4c0103e7d.svg?invert_in_darkmode" align=middle width=132.03003pt height=22.46574pt/> is the number of times the source computer <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/1e07bbe353ff35b931d3b03db30af334.svg?invert_in_darkmode" align=middle width=126.201405pt height=22.63866pt/> has connected to <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/deceeaf6940a8c7a5a02373728002b0f.svg?invert_in_darkmode" align=middle width=8.6493pt height=14.15535pt/> in the fist <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/55a049b8f161ae7cfeb0197d75aff967.svg?invert_in_darkmode" align=middle width=9.867pt height=14.15535pt/> observed connections to the destination computer. 

Therefore, the <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width=8.270625pt height=14.15535pt/>-value for the <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/949707b3bc37b3be0f8b25742664879e.svg?invert_in_darkmode" align=middle width=50.962725pt height=24.6576pt/>-th observation is: 
<p align="center"><img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/c182d0ed7d70557480a9b1ddcc11b9a6.svg?invert_in_darkmode" align=middle width=238.3458pt height=46.87419pt/></p>
where:
<p align="center"><img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/deee18365deb11c87453e50ed05ec9c9.svg?invert_in_darkmode" align=middle width=329.08425pt height=44.897325pt/></p>

The code also uses mid-<img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width=8.270625pt height=14.15535pt/>-values <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/ddf070db9e957f370d2c285e5ad0df40.svg?invert_in_darkmode" align=middle width=141.84192pt height=22.63866pt/>, where:
<p align="center"><img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/adb1ddcd4a1f5507874c291bb27aaadc.svg?invert_in_darkmode" align=middle width=238.3458pt height=46.87419pt/></p>

The mid-<img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width=8.270625pt height=14.15535pt/>-values might be preferable since the distribution of the source nodes is discrete. 


### Combining p-values

A sequence of <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width=8.270625pt height=14.15535pt/>-values <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/0c5e0765d81b2b6f1fd949ea91e454f2.svg?invert_in_darkmode" align=middle width=95.042145pt height=14.15535pt/> can be combined in this code using 6 different methods, described in Heard and Rubin-Delanchy (2018):

* Edgington's method
<p align="center"><img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/8cf4a27cbb84480d003265f7768d300c.svg?invert_in_darkmode" align=middle width=381.98325pt height=47.80611pt/></p>

* Fisher's method - let <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/6ce73d15b9fabc46eb57c4f8fa5d0c74.svg?invert_in_darkmode" align=middle width=242.156805pt height=24.6576pt/>, then:
<p align="center"><img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/08100985de61b1195c446049b5fec837.svg?invert_in_darkmode" align=middle width=385.50105pt height=47.80611pt/></p>

* Pearson's method
<p align="center"><img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/3ac66a0216f3b2656e539c6990984133.svg?invert_in_darkmode" align=middle width=406.24485pt height=47.80611pt/></p>

* George's method 
<p align="center"><img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/7b48f1af7c10253dbc039773fe807528.svg?invert_in_darkmode" align=middle width=527.17995pt height=49.62705pt/></p>

* Stouffer's method - let <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/fd572b44cf8f2a97fc9474603fcc8c69.svg?invert_in_darkmode" align=middle width=46.872375pt height=26.76201pt/> denote the inverse of the CDF <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/f04e663ab860a40f062cc6e871367aa8.svg?invert_in_darkmode" align=middle width=29.223975pt height=24.6576pt/> of a standard normal distribution, then:
<p align="center"><img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/5ee1a9c5c643c957e2408aa34dea31fa.svg?invert_in_darkmode" align=middle width=384.80805pt height=47.80611pt/></p>

* Tippett's method (or minimum <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width=8.270625pt height=14.15535pt/>-value) method 
<p align="center"><img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/6f47354ed7c2e72922ef80fc243dbcf6.svg?invert_in_darkmode" align=middle width=418.97625pt height=21.41898pt/></p>

*Note that the distributional results are only valid under normal behaviour of the network.*

### Anomaly detection

In the code, the <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width=8.270625pt height=14.15535pt/>-values and mid-<img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width=8.270625pt height=14.15535pt/>-values are combined in two different stages. Suppose that for a given destination computer <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/3a49e7753441741b7224c79f23973f59.svg?invert_in_darkmode" align=middle width=41.982435pt height=22.46574pt/>, the <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width=8.270625pt height=14.15535pt/>-values (and mid-<img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width=8.270625pt height=14.15535pt/>-values) <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/0a565ce3c8be493d86a30905292bb751.svg?invert_in_darkmode" align=middle width=72.091305pt height=14.15535pt/> corresponding to each observed connection are computed using the PY posterior predictive probability.

* for all the connections on a given edge <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/3235cd4219d9ac6bb294560e93424cdd.svg?invert_in_darkmode" align=middle width=43.614945pt height=14.15535pt/>, it is possible to combine the <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width=8.270625pt height=14.15535pt/>-values and obtain a grouped <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width=8.270625pt height=14.15535pt/>-value <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/fdf7869674ef3b6332cf8320a6977b90.svg?invert_in_darkmode" align=middle width=22.80465pt height=14.15535pt/> for each edge,

* given the <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width=8.270625pt height=14.15535pt/>-values <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/fdf7869674ef3b6332cf8320a6977b90.svg?invert_in_darkmode" align=middle width=22.80465pt height=14.15535pt/> for each edge, it is possible to combine the <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width=8.270625pt height=14.15535pt/>-values <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/3aeedd4086c03ad3c8ef262af65d638b.svg?invert_in_darkmode" align=middle width=95.05716pt height=14.15535pt/> for a given source computer <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/332cc365a4987aacce0ead01b8bdcc0b.svg?invert_in_darkmode" align=middle width=9.3951pt height=14.15535pt/>, in order to obtain a <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width=8.270625pt height=14.15535pt/>-value for each source computer.

The <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width=8.270625pt height=14.15535pt/>-values computed at the second stage give an anomaly score for the source node <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/332cc365a4987aacce0ead01b8bdcc0b.svg?invert_in_darkmode" align=middle width=9.3951pt height=14.15535pt/>, which can be used for anomaly detection. 

## References

* Heard, N.A. and Rubin-Delanchy, P. (2016), "Network-wide anomaly detection via the Dirichlet process", Proceedings of IEEE workshop on Big Data Analytics for Cyber-Security Computing.

* Heard, N.A. and Rubin-Delanchy, P. (2018), "Choosing between methods of combining p-values", Biometrika 105(1), 239–246.

* Pitman, J. and Yor, M. (1997), "The two-parameter Poisson-Dirichlet distribution derived from a stable sub-ordinator", Annals of Probability 25, 855-900.


