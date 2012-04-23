from pylab import *
from copy import copy
from time import sleep
tmax = 20

class HopfieldNetwork:
    def __init__(self,N):
        self.N = N
        """
        DEFINITION
        initialization of the class

        INPUT
        N: size of the network, i.e. if N=10 it will consists of 10 pixels

        """

    def create_pattern(self,P=5,ratio=0.5):
        self.P = P
        self.pattern = -ones((P,self.N),int)

        idx = int(ratio*self.N)
        for i in range(P):
            self.pattern[i,:idx] = 1
            self.pattern[i] = permutation(self.pattern[i])

    def calc_weight(self):
        self.weight = zeros((self.N,self.N))
        
        for i in range(self.N):
            for j in range(self.N):
				if i != j:
					self.weight[i,j] = 1./self.N * sum(self.pattern[mu, i] * self.pattern[mu,j] for mu in range(self.P))
        
    def set_init_state(self,mu,flip_ratio):
        self.x = copy(self.pattern[mu])
        flip = permutation(arange(self.N))
        idx = int(self.N*flip_ratio)
        self.x[flip[0:idx]] *= -1
        self.t = [0]
        overlap = [self.overlap(mu)]

    def energy(self):
        h = 0        
        for i in range(self.N):
            for j in range(self.N):
                h = h + self.weight[i,j] * self.x[i] * self.x[j]
        return -h

    def dynamic(self):
        """
        DEFINITION
        executes one step of the dynamics

        -L.Ziegler 03.2009.
        """

        h = sum(self.weight*self.x,axis=1)
        self.x = sign(h)
        

    def overlap(self,mu=0):
        """
        DEFINITION
        computes the overlap of the test pattern with pattern nb mu

        INPUT
        mu: the index of the pattern to compare with the test pattern

        -L.Ziegler 03.2009.
        """

        return 1./self.N*sum(self.pattern[mu]*self.x)

    def run(self,P=5, ratio=0.5, mu=0, flip_ratio=0.2):
        """
        DEFINITION
        runs the dynamics and plots it in an awesome way
        
        INPUT
        mu: pattern number to use as test pattern
        flip_ratio: ratio of flipped pixels
                    ex. for pattern nb 5 with 5% flipped pixels use run(mu=5,flip_ratio=0.05)
        
        -L.Ziegler 03.2009.
        -N.Fremaux 03.2010.
        """
        
      #  try:
     #       self.pattern[mu]
     #   except:
 #           raise IndexError, 'pattern index too high'
        
        self.create_pattern(P, ratio)
        self.calc_weight()
        self.set_init_state(mu,flip_ratio)

        t = [0]
        overlap = [self.overlap(mu)]
        energy = [self.energy()]
        # prepare the figure
        figure()
        '''
        # plot the current network state
        subplot(221)
        g1 = imshow(self.grid(),**plot_dic)# we keep a handle to the image
        axis('off')
        title('x')
        
        # plot the target pattern
        subplot(222)
        imshow(self.grid(mu=mu),**plot_dic)
        axis('off')
        title('pattern %i'%mu)
        '''       

        subplot(211)
        g1, = plot(t,energy,'k',lw=2)
        axis([0,tmax,0,-self.N*5])
        xlabel('time step')
        ylabel('energy')

        # plot the time course of the overlap
        subplot(212)
        g2, = plot(t,overlap,'k',lw=2) # we keep a handle to the curve
        axis([0,tmax,-1,1])
        xlabel('time step')
        ylabel('overlap')
        
        # this forces pylab to update and show the fig.


        draw()
        
        x_old = copy(self.x)
        
        
        for i in range(tmax):

            # run a step
            self.dynamic()
            t.append(i+1)
            overlap.append(self.overlap(mu))
            energy.append(self.energy())
            
            # update the plotted data
            g1.set_data(t, energy)
            g2.set_data(t,overlap)
            
            # update the figure so that we see the changes
            draw()
            
            # check the exit condition
            i_fin = i+1
            if sum(abs(x_old-self.x))==0:
                break
            x_old = copy(self.x)
            sleep(0.5)
        print 'pattern recovered in %i time steps with final overlap %.3f'%(i_fin,overlap[-1])
        show()
