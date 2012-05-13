from Hopfield import HopfieldNetwork
from pylab import *
import numpy as np
import pickle

'''
        We now define the capacity of a Hopfield network of size N as the number of patterns PN,max that
        can be stored, such that the mean retrieval error averaged over all stored patterns (one retrieval
        attempt each) is at most 2%. This yields the maximal load N,max = PN,max . N
        
        Set c=0.1. Calculate N,max for at least 10 network realizations and state the mean together 
        with confidence intervals. Do this for N = 100, 250 and one other larger network size. 
        
        Shortly interpret the resulting values and compare with results from literature.
        
        Hint: To calculate Pmax, successively add patterns and calculate the mean retrieval error over.
'''


def pmax(N,flip_ratio,pcut):
    h = HopfieldNetwork()
    p=1
    meanerror = 0
    while meanerror <= 0.02:
        error=zeros((1,p),float)
        for r in range(p):
            error[0,r]=(h.run(N=N, P=p+1, mu=r, flip_ratio=flip_ratio,pcut=pcut, bPlot=False))
        meanerror=np.mean(error[0,:])
        p=p+1
        print '%d: %.4f' %( p , meanerror)
    return p-1

def exercise2(N=500,tests=10,confidence=0.95):
    print 'Exercise 2:'
    pmaxval=zeros((3,tests),float)
    n = 0
    for N in (100,250,N):
        print N
        for i in range(tests):
            pmaxval[n,i]=pmax(N,flip_ratio=0.1,pcut=0)
        loadmax=pmaxval[n,:]/N
        load_mean=np.mean(loadmax)
        pmax_mean=np.mean(pmaxval[n,:])
        load_std=np.std(loadmax)
        ci = load_std * ((1+confidence)/2)/ 10
        
        n += 1

        print 'The maximal load of the Hopfield Network with N=%d is %.5f with a 0.95 confidence intervall of [%.5f,%.5f].\nThe capacity of the network is %.5f'%(N, load_mean,load_mean-ci,load_mean+ci,pmax_mean)        
    
    with open('../tex/img/plots/exercise2_pmaxval','w') as f:
        pickle.dump(pmaxval,f)
    f.closed

if __name__=="__main__":
    exercise2()

