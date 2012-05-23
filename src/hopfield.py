"""
    Provides the HopfieldNetwork class and related functions for the miniproject
    Robustness of storage capacity in more realistic Hopfield networks
"""

from pylab import *
from copy import copy

TMAX = 20


class HopfieldNetwork:
    """ Main class for the Miniproject. """
    def __init__(self):
        """ HopfieldNetwork init """

    def create_pattern(self,P=5,ratio=0.5):            
        self.P = P
        self.pattern = -ones((P,self.N),int) 
        idx = int(ratio*self.N) 
        for i in range(P):
            self.pattern[i,:idx] = 1 
            self.pattern[i] = permutation(self.pattern[i]) 

    def calc_weight(self):
        self.weight=1./self.N*np.dot((self.pattern[:,:]).T,self.pattern[:,:])
        self.weight[eye(self.N,self.N,dtype='bool')] = 0
    
    def cut_weight(self, Pcut):
        """
            Exercise 3: Random asymetry
            ...consider now networks where for each pairs of nodes (i, j), the 
            directed connection from node i to node j is cut with probability 
            pcut.
        """
        if Pcut > 0:
            self.weight[rand(self.N,self.N)<Pcut] = 0


    def set_init_state(self,mu,flip_ratio):
        self.x=np.zeros((1,self.N))
        self.x[0,:] = self.pattern[mu,:]
        flip = permutation(arange(self.N))   
        idx = int(self.N*flip_ratio) 
        self.x[0,flip[0:idx]] *= -1         
        self.t = [0]         
        overlap = [self.overlap(mu)]     

    def energy(self):
        e=-np.dot(self.x,np.dot(self.weight,(self.x).T))
        return e[0,0]
    
    def dynamic_seq(self,j):
        if sign(np.dot(self.x[:,:],self.weight[:,:])[0,j])==0:
            self.x[0,j]=1
        else:
            self.x[0,j]=sign(np.dot(self.x[:,:],self.weight[:,:])[0,j])
    
    def overlap(self,mu=0):
        return np.dot(self.pattern[mu,:],self.x[0,:])/float(self.N)

    def normalized_pixel_distance(self,mu=0):
        """
            Exercise 1.2: Normalized pixel distance
            Using the overlap defined in 1.1, derive an expression for the 
            percentage of pixels in the network state S which differ from 
            the pattern mu. This is the (normalized) pixel distance.
        """
        return (1-self.overlap(mu))/2

    def init_excitatory(self, percentage=0.5):
        """
            Exercise 4: Dale's law
            ... enforce Dale's law on the network connectivity by setting
            disallowed connection weights in the standard Hebbian
            weight to zero ...
        """
        idx_exc = int(percentage * self.N)
        idx_inh = int((1-percentage) * self.N)
        flip = permutation(arange(self.N)) 
        self.excitatory_nodes = flip[0:idx_exc]
        self.inhibitory_nodes = flip[idx_exc+1:]
        for i in self.excitatory_nodes:
            self.weight[i, self.weight[i,:] < 0 ] = 0
        for i in self.inhibitory_nodes:
            self.weight[i, self.weight[i,:] > 0 ] = 0

    def run(self, N=200, P=5, ratio=0.5, mu=0,
            flip_ratio=0.2, pcut=0, excitatory=-1,
            bPlot=True, bDebug=False):
        self.N=N
        self.create_pattern(P, ratio)
        self.calc_weight()
        self.set_init_state(mu,flip_ratio)
        self.cut_weight(pcut)
        if (0 <= excitatory) & (excitatory <= 1) :
            self.init_excitatory(percentage=excitatory)
        if bDebug:
            print self.weight
        t = [0]
        overlap = [self.overlap(mu)]
        energy = [self.energy()]
        normalized_pixel_distance = [self.normalized_pixel_distance()]
        x_old = copy(self.x)
        for i in range(TMAX):
            #update each field sequentially
            s=1
            for j in permutation(range(self.N)):
                self.dynamic_seq(j)
                overlap.append(self.overlap(mu))
                energy.append(self.energy())
                normalized_pixel_distance.append(
                                self.normalized_pixel_distance(mu))
                t.append(i+divide(s,float(self.N)))
                s+=1
            # check the exit condition
            i_fin = i+1
            if sum(abs(x_old-self.x))==0:
                break
            x_old = copy(self.x)
        if bPlot:
            # prepare the figure
            figure(num=None, figsize=(7, 8), 
                    dpi=80, facecolor='w', edgecolor='k')
            # plot the time course of the energy
            subplot(311)
            g1, = plot(t,energy,'b',lw=2)
            axis('auto')
            xlim(0, 2) 
            ylabel('energy')
            grid('on')
            # plot the time course of the overlap
            subplot(312)
            g2, = plot(t,overlap,'b',lw=2) 
            axis('auto')
            xlim(0,2)
            ylabel('overlap')
            grid('on')
            # plot the time course of the normalized pixel distance
            subplot(313)
            g3, = plot(t,normalized_pixel_distance,'b',lw=2) 
            axis('auto')
            xlim(0,2)
            xlabel('time step')
            ylabel('normalized pixel distance')
            grid('on')            

            draw()

        
        if bDebug:
            print 'pattern recovered in %i time steps with final overlap %.3f '\
                ' and energy %.3f' % (i_fin,overlap[-1],energy[-1]) 
        return normalized_pixel_distance[-1]


def pmax(N, flip_ratio, pcut, excitatory=-1):
    """ pmax calculates the maximum capacity of a network."""
    h = HopfieldNetwork()
    p = 1
    meanerror = 0
    while meanerror <= 0.02:
        error=zeros((1,p),float)
        for r in range(p):
            error[0,r] = h.run(N=N, P = p + 1, mu=r, flip_ratio=flip_ratio, 
                pcut=pcut, bPlot=False, excitatory=excitatory)
        meanerror = np.mean(error[0, :])
        p = p + 1
        print '%d: %.4f' % (p, meanerror)
    return p - 1

def load_max(N, flip_ratio, pcut=0,
             tests=10, confidence=0.95, excitatory=-1):
    """ 
        load_max calculates the mean maximum load and the confidence intervall
        as well as the maximum capacity of a network.
    """
    pmaxval=zeros((1,tests),float)
    for i in range(tests):
        pmaxval[0, i]=pmax(N=N, flip_ratio=flip_ratio, pcut=pcut, 
            excitatory=excitatory)
    loadmax = pmaxval[0,:] / N
    load_mean = np.mean(loadmax)
    pmax_mean = np.mean(pmaxval[0,:])
    load_std = np.std(loadmax)
    ci = load_std * ((1 + confidence) / 2) / tests

    out = [load_mean, load_mean - ci, load_mean + ci, pmax_mean, load_std]
    return out

