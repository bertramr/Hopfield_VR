from Hopfield import HopfieldNetwork, pmax, load_max
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

def exercise2(Nlst=(100,250,500),tests=10,confidence=0.95):
    print 'Exercise 2:'
    with open('../tex/img/plots/exercise2_table.tex','w') as fp:
        fp.write('N & tests & C-level & maximal load & lower bound & upper bound & $P_{N,max}$\\\\ \n \\hline \\hline \n') 
        for N in Nlst:
            print N
            [load_mean, load_mean_lb, load_mean_ub, pmax_mean, load_std] = \
               load_max(N=N, flip_ratio=0.1, pcut=0, tests=tests, confidence=confidence)
            fp.write('%d & %d & %0.1f & %0.4f & %0.4f & %0.4f & %0.2f \\\\ \n' % \
                (N, tests, confidence*100, \
                load_mean, load_mean_lb, load_mean_ub, \
                pmax_mean))
    fp.closed
        
    save_dump = [load_mean, load_mean_lb, load_mean_ub, pmax_mean, load_std]
    with open('../tex/img/plots/exercise2_pmaxval-%d-%d'% (N,tests) ,'w') as f:
        pickle.dump(save_dump,f)
    f.closed
    print 'The maximal load of the Hopfield Network with N=%d is %.5f with a 0.95 confidence intervall of [%.5f,%.5f].\nThe capacity of the network is %.5f'\
            % (N, load_mean,load_mean_lb ,load_mean_ub,pmax_mean)        


if __name__=="__main__":
    exercise2()

