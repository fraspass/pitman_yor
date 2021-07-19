# Modelling dynamic network evolution as a Pitman-Yor process

The model and datasets are described in *Sanna Passino, F. and Heard, N. A., "Modelling dynamic network evolution as a Pitman-Yor process", Foundations of Data Science, 2019, 1(3):293-306* ([link](https://www.aimsciences.org/article/doi/10.3934/fods.2019013)). 

This repository contains Python code used to perform network-wide anomaly detection in a computer network using the two parameter Poisson-Dirichlet or Pitman-Yor process (Pitman and Yor, 1997). 

This code builds up on the Hadoop-MapReduce procedure described in Heard and Rubin-Delanchy (2016). The Dirichlet process described by the authors in the paper is extended to include an extra parameter, which allows for more flexibility when modelling data exhibiting power-law behaviour.

## Methodology

### The Pitman-Yor process

A computer network can be interpreted as a directed graph <img src="svgs/73dde20bcffb31b6177c5d21c5a96f6d.svg?invert_in_darkmode" align=middle width=78.37895999999999pt height=24.6576pt/>, where <img src="svgs/a9a3a4a202d80326bda413b5562d5cd1.svg?invert_in_darkmode" align=middle width=13.242074999999998pt height=22.46574pt/> is the node set of computers and <img src="svgs/94db391751ae0befe931ce025807b400.svg?invert_in_darkmode" align=middle width=81.575175pt height=22.46574pt/> is the edge set of observed unique connections. 

Let us assume that <img src="svgs/93e8f48a97001313f47040c9f354a850.svg?invert_in_darkmode" align=middle width=98.41540499999999pt height=14.15535pt/> is a sequence of source computers that have connected to a destination computer <img src="svgs/3a49e7753441741b7224c79f23973f59.svg?invert_in_darkmode" align=middle width=41.982434999999995pt height=22.46574pt/>. For the given destination computer <img src="svgs/deceeaf6940a8c7a5a02373728002b0f.svg?invert_in_darkmode" align=middle width=8.6493pt height=14.15535pt/>, we assume that the exchangeable sequence of source computers has the following hierarchical distribution:
<p align="center"><img src="svgs/1143b12b6dc3c7fe87147d9885c524ac.svg?invert_in_darkmode" align=middle width=170.67434999999998pt height=52.865339999999996pt/></p>

The PPPF implied by the Pitman-Yor process is:
<p align="center"><img src="svgs/aaeab5c4459e02c055b6e5bede16eaf1.svg?invert_in_darkmode" align=middle width=482.9318999999999pt height=50.226165pt/></p>

where <img src="svgs/96b697078d351b7b43bd5b5dce0254cd.svg?invert_in_darkmode" align=middle width=22.087229999999998pt height=22.46574pt/> is the number of unique source computers that have connected to <img src="svgs/deceeaf6940a8c7a5a02373728002b0f.svg?invert_in_darkmode" align=middle width=8.6493pt height=14.15535pt/> up to time <img src="svgs/55a049b8f161ae7cfeb0197d75aff967.svg?invert_in_darkmode" align=middle width=9.867pt height=14.15535pt/>, and <img src="svgs/1d484b012b923f611683f2899bac1ba2.svg?invert_in_darkmode" align=middle width=137.509515pt height=22.46574pt/> is the number of times the source computer <img src="svgs/1e07bbe353ff35b931d3b03db30af334.svg?invert_in_darkmode" align=middle width=126.20140499999998pt height=22.638659999999998pt/> has connected to <img src="svgs/deceeaf6940a8c7a5a02373728002b0f.svg?invert_in_darkmode" align=middle width=8.6493pt height=14.15535pt/> in the fist <img src="svgs/55a049b8f161ae7cfeb0197d75aff967.svg?invert_in_darkmode" align=middle width=9.867pt height=14.15535pt/> observed connections to the destination computer. 

Therefore, the <img src="svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width=8.270624999999999pt height=14.15535pt/>-value for the <img src="svgs/949707b3bc37b3be0f8b25742664879e.svg?invert_in_darkmode" align=middle width=50.962725pt height=24.6576pt/>-th observation is: 
<p align="center"><img src="svgs/c182d0ed7d70557480a9b1ddcc11b9a6.svg?invert_in_darkmode" align=middle width=238.3458pt height=46.87419pt/></p>
where:
<p align="center"><img src="svgs/717a445608dc8369e881512f6fb1cfa0.svg?invert_in_darkmode" align=middle width=329.08425pt height=44.897324999999995pt/></p>

The code also uses mid-<img src="svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width=8.270624999999999pt height=14.15535pt/>-values <img src="svgs/6a4c7b1002ca391a5b1db9923532c6a9.svg?invert_in_darkmode" align=middle width=171.888255pt height=24.6576pt/>, where:
<p align="center"><img src="svgs/07a08b46583fe3c7fb18b1d3be6e3f3f.svg?invert_in_darkmode" align=middle width=238.3458pt height=46.87419pt/></p>

The mid-<img src="svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width=8.270624999999999pt height=14.15535pt/>-values might be preferable since the distribution of the source nodes is discrete. 

### Combining p-values

A sequence of <img src="svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width=8.270624999999999pt height=14.15535pt/>-values <img src="svgs/0c5e0765d81b2b6f1fd949ea91e454f2.svg?invert_in_darkmode" align=middle width=95.042145pt height=14.15535pt/> can be combined in this code using 6 different methods, described in Heard and Rubin-Delanchy (2018):

* Edgington's method:
<p align="center"><img src="svgs/ceb944bf71dc0ce0e0d1e68c9fbff0c9.svg?invert_in_darkmode" align=middle width=381.98325pt height=47.80611pt/></p>

* Fisher's method - let <img src="svgs/6ce73d15b9fabc46eb57c4f8fa5d0c74.svg?invert_in_darkmode" align=middle width=242.15680499999996pt height=24.6576pt/>, then:
<p align="center"><img src="svgs/08100985de61b1195c446049b5fec837.svg?invert_in_darkmode" align=middle width=385.50104999999996pt height=47.80611pt/></p>

* Pearson's method:
<p align="center"><img src="svgs/ba27c0ced6752672fbea205c53b85dfb.svg?invert_in_darkmode" align=middle width=406.24485pt height=47.80611pt/></p>

* George's method: 
<p align="center"><img src="svgs/3f0fd7c4baab7f2f1f08dbbd2071a3ae.svg?invert_in_darkmode" align=middle width=529.6153499999999pt height=49.62705pt/></p>

* Stouffer's method - let <img src="svgs/fd572b44cf8f2a97fc9474603fcc8c69.svg?invert_in_darkmode" align=middle width=46.872375pt height=26.76201pt/> denote the inverse of the CDF <img src="svgs/f04e663ab860a40f062cc6e871367aa8.svg?invert_in_darkmode" align=middle width=29.223975pt height=24.6576pt/> of a standard normal distribution, then:
<p align="center"><img src="svgs/5ee1a9c5c643c957e2408aa34dea31fa.svg?invert_in_darkmode" align=middle width=384.80805pt height=47.80611pt/></p>

* Tippett's method (or minimum <img src="svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width=8.270624999999999pt height=14.15535pt/>-value) method: 
<p align="center"><img src="svgs/6f47354ed7c2e72922ef80fc243dbcf6.svg?invert_in_darkmode" align=middle width=418.97625pt height=21.418979999999998pt/></p>

*Note that the distributional results are only valid under normal behaviour of the network.*

### Anomaly detection

In the code, the <img src="svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width=8.270624999999999pt height=14.15535pt/>-values and mid-<img src="svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width=8.270624999999999pt height=14.15535pt/>-values are combined in two different stages. Suppose that for a given destination computer <img src="svgs/3a49e7753441741b7224c79f23973f59.svg?invert_in_darkmode" align=middle width=41.982434999999995pt height=22.46574pt/>, the <img src="svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width=8.270624999999999pt height=14.15535pt/>-values (and mid-<img src="svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width=8.270624999999999pt height=14.15535pt/>-values) <img src="svgs/0a565ce3c8be493d86a30905292bb751.svg?invert_in_darkmode" align=middle width=72.09130499999999pt height=14.15535pt/> corresponding to each observed connection are computed using the PY posterior predictive probability.

* for all the connections on a given edge <img src="svgs/3235cd4219d9ac6bb294560e93424cdd.svg?invert_in_darkmode" align=middle width=43.614945pt height=14.15535pt/>, it is possible to combine the <img src="svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width=8.270624999999999pt height=14.15535pt/>-values and obtain a grouped <img src="svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width=8.270624999999999pt height=14.15535pt/>-value <img src="svgs/fdf7869674ef3b6332cf8320a6977b90.svg?invert_in_darkmode" align=middle width=22.80465pt height=14.15535pt/> for each edge,

* given the <img src="svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width=8.270624999999999pt height=14.15535pt/>-values <img src="svgs/fdf7869674ef3b6332cf8320a6977b90.svg?invert_in_darkmode" align=middle width=22.80465pt height=14.15535pt/> for each edge, it is possible to combine the <img src="svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width=8.270624999999999pt height=14.15535pt/>-values <img src="svgs/3aeedd4086c03ad3c8ef262af65d638b.svg?invert_in_darkmode" align=middle width=95.05716pt height=14.15535pt/> for a given source computer <img src="svgs/332cc365a4987aacce0ead01b8bdcc0b.svg?invert_in_darkmode" align=middle width=9.3951pt height=14.15535pt/>, in order to obtain a <img src="svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width=8.270624999999999pt height=14.15535pt/>-value for each source computer.

The <img src="svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width=8.270624999999999pt height=14.15535pt/>-values computed at the second stage give an anomaly score for the source node <img src="svgs/332cc365a4987aacce0ead01b8bdcc0b.svg?invert_in_darkmode" align=middle width=9.3951pt height=14.15535pt/>, which can be used for anomaly detection. 

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

Given the LANL edge list, it is possible to obtain method of moments estimates of the hyperparameters <img src="svgs/ebb66f0e96fcb4a8d842166969b28831.svg?invert_in_darkmode" align=middle width=10.5765pt height=14.15535pt/> and <img src="svgs/26989973be70aab1e939fdccf30b5e1f.svg?invert_in_darkmode" align=middle width=8.556075pt height=22.83138pt/> using the code in `py_parameters.py`:

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


