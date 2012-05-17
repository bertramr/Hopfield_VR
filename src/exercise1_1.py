"""
Implement the Hopfield network as described above. [...] 
For the first two unit steps of the retrieval of one pattern
plot the changing values of the energy function and the
overlap of the network with the pattern as the state of 
each node is sequentially updated
"""

from pylab import *
from hopfield import HopfieldNetwork

def exercise1_1(N=200,P=5,c=0.2):
    print "Exercise 1.1:"
    h = HopfieldNetwork()
    h.run(N=N, P=P, flip_ratio=c, bPlot=True)
    savefig('../tex/dat/ex1_1-energy_overlap-N%d-P%d-c%d.png' % (N,P,c*100))
    close()

if __name__=="__main__":
    exercise1_1()
