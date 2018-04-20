## Network-wide anomaly detection using the Pitman-Yor process

This reposit contains Python code used to perform network-wide anomaly detection using the Pitman-Yor process in a computer network. 

A computer network can be interpreted as a directed graph <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/73dde20bcffb31b6177c5d21c5a96f6d.svg?invert_in_darkmode" align=middle width=78.37896pt height=24.6576pt/>, where <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/a9a3a4a202d80326bda413b5562d5cd1.svg?invert_in_darkmode" align=middle width=13.242075pt height=22.46574pt/> is the node set of computers and <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/94db391751ae0befe931ce025807b400.svg?invert_in_darkmode" align=middle width=81.575175pt height=22.46574pt/> is the edge set of observed unique connections. 

Let us assume that <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/93e8f48a97001313f47040c9f354a850.svg?invert_in_darkmode" align=middle width=98.415405pt height=14.15535pt/> is a sequence of source computers that have connected to a destination computer <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/3a49e7753441741b7224c79f23973f59.svg?invert_in_darkmode" align=middle width=41.982435pt height=22.46574pt/>. For the given destination computer <img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/deceeaf6940a8c7a5a02373728002b0f.svg?invert_in_darkmode" align=middle width=8.6493pt height=14.15535pt/>, we assume that the exchangeable sequence of source computers has the following hierarchical distribution:
<p align="center"><img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/e1dded7996541a17882ae3e641edd9e4.svg?invert_in_darkmode" align=middle width=169.2339pt height=52.86534pt/></p>

The PPPF implied by the Pitman-Yor process is:

<p align="center"><img src="https://rawgit.com/fraspass/pitman_yor/master/svgs/d414ce68b2b6ff92130f05d0677859e3.svg?invert_in_darkmode" align=middle width=304.60485pt height=35.18196pt/></p>

