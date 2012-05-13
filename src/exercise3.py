from Hopfield import HopfieldNetwork
from exercise2 import pmax
import numpy as np
from pylab import *

def exercise3(N = 200, c= 0.1, pcut=0, repetition=10):
    '''
    Exercise 3: Random asymmetry
    To investigate the robustness of pattern retrieval against asymmetry in the
    weight matrix, consider now networks where for each pairs of nodes (i, j), 
    the directed connection from node i to node j is cut with probability pcut .
    This will introduce asymmetry in the Hebbian weight matrix Eq. 1.
    Set c=0.1 and N = 200. As in Ex. 2 calculate and plot the mean alpha_N,max for
    varying pcut with error bars (at least 10 repetitions). At which pcut does
    the maximal load drop below 50% of the value estimated in Ex. 2? State the
    confidence interval.
    Note: Bare in mind that the convergence assertion of Question 1.1 does not 
    necessarily hold for pcut > 0.
    '''
    
    for rep in range(repetition):
        for pcut in np.linspace(0,1,num=11):
            pmax(N=N,flip_ratio=c,pcut=pcut)

if __name__=="__main__":
    exercise3()

