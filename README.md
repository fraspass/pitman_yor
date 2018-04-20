## Network-wide anomaly detection using the Pitman-Yor process

This reposit contains Python code used to perform network-wide anomaly detection using the two parameter Poisson-Dirichlet or Pitman-Yor process (Pitman and Yor, 1997) in a computer network. 

This code builds up on the Hadoop-MapReduce procedure described in Heard and Rubin-Delanchy (2016). The Dirichlet process described by the authors in the paper is extended to include an extra parameter, which allows for more flexibility when modelling data exhibiting power-law behaviour.

# Methodology

A computer network can be interpreted as a directed graph <img src="https://rawgit.com/fraspass/pitman_yor/None/svgs/73dde20bcffb31b6177c5d21c5a96f6d.svg?invert_in_darkmode" align=middle width=78.37896pt height=24.6576pt/>, where <img src="https://rawgit.com/fraspass/pitman_yor/None/svgs/a9a3a4a202d80326bda413b5562d5cd1.svg?invert_in_darkmode" align=middle width=13.242075pt height=22.46574pt/> is the node set of computers and <img src="https://rawgit.com/fraspass/pitman_yor/None/svgs/94db391751ae0befe931ce025807b400.svg?invert_in_darkmode" align=middle width=81.575175pt height=22.46574pt/> is the edge set of observed unique connections. 

Let us assume that <img src="https://rawgit.com/fraspass/pitman_yor/None/svgs/93e8f48a97001313f47040c9f354a850.svg?invert_in_darkmode" align=middle width=98.415405pt height=14.15535pt/> is a sequence of source computers that have connected to a destination computer <img src="https://rawgit.com/fraspass/pitman_yor/None/svgs/3a49e7753441741b7224c79f23973f59.svg?invert_in_darkmode" align=middle width=41.982435pt height=22.46574pt/>. For the given destination computer <img src="https://rawgit.com/fraspass/pitman_yor/None/svgs/deceeaf6940a8c7a5a02373728002b0f.svg?invert_in_darkmode" align=middle width=8.6493pt height=14.15535pt/>, we assume that the exchangeable sequence of source computers has the following hierarchical distribution:
<p align="center"><img src="https://rawgit.com/fraspass/pitman_yor/None/svgs/8200749748ae36b2058d9caafc3d8805.svg?invert_in_darkmode" align=middle width=170.67435pt height=52.86534pt/></p>

The PPPF implied by the Pitman-Yor process is:
<p align="center"><img src="https://rawgit.com/fraspass/pitman_yor/None/svgs/aaeab5c4459e02c055b6e5bede16eaf1.svg?invert_in_darkmode" align=middle width=482.9319pt height=50.226165pt/></p>

Therefore, the <img src="https://rawgit.com/fraspass/pitman_yor/None/svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width=8.270625pt height=14.15535pt/>-value for the <img src="https://rawgit.com/fraspass/pitman_yor/None/svgs/949707b3bc37b3be0f8b25742664879e.svg?invert_in_darkmode" align=middle width=50.962725pt height=24.6576pt/>-th observation is: 
<p align="center"><img src="https://rawgit.com/fraspass/pitman_yor/None/svgs/c182d0ed7d70557480a9b1ddcc11b9a6.svg?invert_in_darkmode" align=middle width=238.3458pt height=46.87419pt/></p>
where:
<p align="center"><img src="https://rawgit.com/fraspass/pitman_yor/None/svgs/717a445608dc8369e881512f6fb1cfa0.svg?invert_in_darkmode" align=middle width=329.08425pt height=44.897325pt/></p>

The <img src="https://rawgit.com/fraspass/pitman_yor/None/svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width=8.270625pt height=14.15535pt/>-values <img src="https://rawgit.com/fraspass/pitman_yor/None/svgs/2212ac77cd4b90e98ea992ea6af765af.svg?invert_in_darkmode" align=middle width=108.165915pt height=14.15535pt/> obtained for each observed connection can be combined in this code using 6 different methods, described in Heard and Rubin-Delanchy (2018):

* Edgington's method: 
<p align="center"><img src="https://rawgit.com/fraspass/pitman_yor/None/svgs/8cf4a27cbb84480d003265f7768d300c.svg?invert_in_darkmode" align=middle width=381.98325pt height=47.80611pt/></p>

* Fisher's method: 
<p align="center"><img src="https://rawgit.com/fraspass/pitman_yor/None/svgs/bae718e42740c90174c04a556a61a5b6.svg?invert_in_darkmode" align=middle width=385.50105pt height=47.80611pt/></p> 
where <img src="https://rawgit.com/fraspass/pitman_yor/None/svgs/6ce73d15b9fabc46eb57c4f8fa5d0c74.svg?invert_in_darkmode" align=middle width=242.156805pt height=24.6576pt/>,

* Pearson's method: 
<p align="center"><img src="https://rawgit.com/fraspass/pitman_yor/None/svgs/3ac66a0216f3b2656e539c6990984133.svg?invert_in_darkmode" align=middle width=406.24485pt height=47.80611pt/></p>

* George's method: 
<p align="center"><img src="https://rawgit.com/fraspass/pitman_yor/None/svgs/ed46d7c790140751a1dbb8f36105ed41.svg?invert_in_darkmode" align=middle width=537.52875pt height=49.62705pt/></p>

* Stouffer's method:
<p align="center"><img src="https://rawgit.com/fraspass/pitman_yor/None/svgs/88d2de97afc9105c611b42f49e42216b.svg?invert_in_darkmode" align=middle width=384.80805pt height=47.80611pt/></p>
where <img src="https://rawgit.com/fraspass/pitman_yor/None/svgs/fd572b44cf8f2a97fc9474603fcc8c69.svg?invert_in_darkmode" align=middle width=46.872375pt height=26.76201pt/> is the inverse of the CDF <img src="https://rawgit.com/fraspass/pitman_yor/None/svgs/f04e663ab860a40f062cc6e871367aa8.svg?invert_in_darkmode" align=middle width=29.223975pt height=24.6576pt/> of a standard normal distribution,

* Tippett's method (or minimum <img src="https://rawgit.com/fraspass/pitman_yor/None/svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width=8.270625pt height=14.15535pt/>-value) method: 
<p align="center"><img src="https://rawgit.com/fraspass/pitman_yor/None/svgs/6f47354ed7c2e72922ef80fc243dbcf6.svg?invert_in_darkmode" align=middle width=418.97625pt height=21.41898pt/></p>

Note that the distributional results are only valid under normal behaviour of the network.

# References

* Heard, N.A. and Rubin-Delanchy, P. (2016), "Network-wide anomaly detection via the Dirichlet process", Proceedings of IEEE workshop on Big Data Analytics for Cyber-Security Computing.

* Heard, N.A. and Rubin-Delanchy, P. (2018), "Choosing between methods of combining p-values", Biometrika 105(1), 239–246.

* Pitman, J. and Yor, M. (1997), "The two-parameter Poisson-Dirichlet distribution derived from a stable sub-ordinator", Annals of Probability 25, 855-900.


