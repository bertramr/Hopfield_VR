from Hopfield import HopfieldNetwork
from exercise2 import pmax, load_max
import numpy as np
from pylab import *
import pickle

def exercise3(N = 200, c= 0.1, confidence=0.95, numint = 11, repetition=10):
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
    print 'Exercise 3:'

    i = 0
    load_mean = zeros(numint,float)
    load_std = zeros(numint,float)
    for pcut in np.linspace(0,1,num=numint):
        [load_mean[i], load_mean_lb, load_mean_ub, pmax_mean, load_std[i]] = \
            load_max(N=N, flip_ratio=c, pcut=pcut, tests=repetition, confidence=confidence)
        i += 1

    fig = figure()
    ax1 = fig.add_subplot(111)
    lp = errorbar(np.linspace(0,1,num=numint),load_mean,load_std)
    
    ax1.set_ylim(0,1)
    ax1.yaxis.grid(True,linestyle='-',which='major',color=(0.2,0.2,0.2),alpha=0.5)
    ax1.set_axisbelow(True)
    ax1.set_title('Mean maximal load over different P_cut (N=%d, Q=%d)' % (N, repetition))
    ax1.set_ylabel('mean maximal load')
    ax1.set_xlabel('P_cut')
    savefig('../tex/img/plots/exer3_mean_max_load-N%d-Q%d.png' % (N,repetition))
    close()
    
    save_dump = [load_mean, load_mean_lb, load_mean_ub, pmax_mean, load_std]
    with open('../tex/img/plots/exercise3_pmaxval','w') as f:
        pickle.dump(save_dump,f)
    f.closed

if __name__=="__main__":
    exercise3()

