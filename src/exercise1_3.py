from Hopfield import HopfieldNetwork
from pylab import *
from numpy import random, dot, max, min, divide

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
    P = 50;
    tests = 10
    error = zeros((P,tests),float)
    for p in range(P):
        for q in range(tests):
            if p > 0:
                r = random.randint(0,p)
            else:
                r = 0
            error[p,q]=(h.run(P=p+1, mu=r, flip_ratio=0.1, bPlot=False))
    
    print error;
    max_error = max(error,axis=1)
    min_error = min(error,axis=1)
        
    figure()
    boxplot(transpose(error))
    savefig('../tex/img/plots/error-avg-%d.png' % tests)
    close()

if __name__=="__main__":
    exercise1_3()

