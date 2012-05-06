from HopfieldNetwork import HopfieldNetwork
from pylab import *
from numpy import random

def main():
    h = HopfieldNetwork(N=200)
    error = zeros((5,10),int);
    for p in range(1, 11):
        for q in range(5):
            r = random.randint(0,p)
            error[q,p-1]=(h.run(P=p, mu=r, flip_ratio=0.1))
    
    figure();
    plot(error);


if __name__=="__main__":
    main()

