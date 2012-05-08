from Hopfield import HopfieldNetwork
from pylab import *
from numpy import random

def exercise1_3():
    '''
    Set N = 200 and c = 0.1. Plot the mean retrieval error of 
    a randomly chosen pattern averaged
    over different network realizations as a function of
    the dictionary size P . Average over enough
    network realizations to give a smooth curve 
    and give error bars for the estimation of the mean
    (you can assume the variation to be normally distributed).
    From your data points and the chosen
    confidence interval, roughly estimate
    a maximal P at which patterns can be retrieved from the
    network with a mean retrieval error of less than 2%?
    '''
    
    print "Exercise 1.3:"
    h = HopfieldNetwork(N=200)
    error = zeros((5,10),int);
    for p in range(1, 11):
        for q in range(5):
            r = random.randint(0,p)
            error[q,p-1]=(h.run(P=p, mu=r, flip_ratio=0.1))
    
    figure();
    plot(error);


if __name__=="__main__":
    exercise1_3()

