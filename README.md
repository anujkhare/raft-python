# RAFT
A very simple, naive implementation of RAFT. This is meant to be
for fun and to understand the inner workings of the algorithm.

I plan on using it for simple applications of my own. I will develop it
further according to my use cases.

The main objective of this implementation is to develop a complete implementation that works and can be used in real
applications which is also **easy to understand** and relate to the paper.

This implementation is a good companion to the paper for anyone looking to understand in more detail how a working
implementation looks.

The second and very important goal that I had was to make the implementation is to explore how strategies to make it
testable. I want to be able to simulate nodes going up and down and simulate various scenarios of cluster membership
changes. It might be very well possible to do that using simple mocking.

There are many implementations of RAFT online and many in Python. This implementation differs in the following ways:
1.
2.


## References
1. https://raft.github.io/
2. https://raft.github.io/raft.pdf
3. http://thesecretlivesofdata.com/raft/