"""
Set c=0.1. Calculate a_N,max for at least 10 network realizations and state
the mean together with confidence intervals. Do this for N = 100, 250 and 
one other larger network size. Shortly interpret the resulting values and 
compare with results from literature. Hint: To calculate Pmax , successively
add patterns and calculate the mean retrieval error over.
"""

from pylab import *
from hopfield import HopfieldNetwork, load_max

def exercise2(N_lst=(100, 250, 500), tests=10, confidence=0.95):
    print 'Exercise 2:'
    with open('../tex/dat/ex2-table-N%d-Q%d-C%d.tex' % 
        (N_lst[-1], tests , confidence*100),'w') as fp:
        fp.write(
            '\\begin{tabular}{|l|l|l|l|l|l|l|} \n'
            '\\hline \n'
            'N & tests & C-level & maximal load & lower bound & '
            'upper bound & $P_{N,max}$\\\\ \n'
            ' \\hline \\hline \n'
            ) 
        for N in N_lst:
            print N
            [load_mean, load_mean_lb, load_mean_ub, pmax_mean, 
                load_std] = load_max(
                    N=N, flip_ratio=0.1, pcut=0, 
                    tests=tests, confidence=confidence)
            fp.write('%d & %d & %0.1f $ \\%% $& %0.4f & %0.4f & %0.4f & %0.2f \\\\ \n' % \
                (N, tests, confidence*100, \
                load_mean, load_mean_lb, load_mean_ub, \
                pmax_mean))
        fp.write(
            '\\hline \n'
            '\\end{tabular} \n'
            )
    fp.closed

    print 'The maximal load of the Hopfield Network' \
        'with N=%d is %.5f with a 0.95 confidence intervall ' \
        'of [%.5f,%.5f].\nThe capacity of the network is %.5f' \
        % (N, load_mean,load_mean_lb ,load_mean_ub,pmax_mean)        

if __name__=="__main__":
    exercise2()

