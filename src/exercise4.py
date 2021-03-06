"""
Exercise 4: Dales law
Set c=0.1, N = 200 and turn off random asymmetry (pcut = 0). Set E in [0, 1]
to be the percentage of excitatory nodes.
For a given E, randomly split the network into an excitatory and an 
inhibitory subpopulation (of sizes E*N and (1-E)*N respectively). 
Now enforce Dales law on the network connectivity
by setting disallowed connection weights in the standard Hebbian weight
matrix Eq. 1 to zero. What percentage of the directed connections do you
expect to be cut for E = 1/2. As in Ex. 2 calculate and plot the mean
alpha_N,max for varying E with error bars (at least 10 repetitions).
Interpret the results and compare the value for E = 1 to 
your result from Ex. 3.
"""
from pylab import *
from hopfield import load_max

def exercise4(N=200, c=0.1, numint=11, tests=10, confidence=0.95):
    print('Exercise 4:')
    i = 0
    load_mean = zeros(numint,float)
    load_std = zeros(numint,float)
    for e in np.linspace(0,1,numint):
        [load_mean[i], load_mean_lb, load_mean_ub, pmax_mean,
             load_std[i]] = load_max(
                N=N, flip_ratio=c, pcut=0, tests=tests,
                confidence=confidence, excitatory=e)
        i += 1

    alpha_null = 0.128

    fig = figure()
    ax1 = fig.add_subplot(111)
    lp = errorbar(np.linspace(0,1,num=numint),load_mean/alpha_null,load_std/alpha_null)
    
    ax1.set_ylim(0,1)
    ax1.yaxis.grid(True, linestyle='-', which='major', 
        color=(0.2,0.2,0.2), alpha=0.5)
    ax1.set_axisbelow(True)
    ax1.set_title('Mean maximal load over different E (N=%d, Q=%d)' % 
        (N, tests))
    ax1.set_ylabel('mean maximal load')
    ax1.set_xlabel('E')
    savefig('../tex/dat/ex4-mean_max_load-N%d-Q%d-C%d.png' %
        (N, tests , confidence*100))
    close()
    

if __name__=='__main__':
    exercise4()
