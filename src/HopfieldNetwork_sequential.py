from pylab import *
from numpy import *
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
        """
            DEFINITION
            creates P patterns where the ratio of -1 to 1 pixels is "ratio"
            
            INPUt
            P: Number of patterns
            ratio: ratio of 1/-1 pixels
        """
            
        self.P = P
        self.pattern = -ones((P,self.N),int) #creates an array of ones of length self.N and height P of type int

        idx = int(ratio*self.N) #defines how many cells should be 1
        for i in range(P):
            self.pattern[i,:idx] = 1 # sets the first idx cells to 1
            self.pattern[i] = permutation(self.pattern[i]) #permutates the cells to create a random order ot 1 and -1 cells

    def calc_weight(self):
        """
            DEFINITION
            creates a matrix with all the weights corresponsing to the pattern self.pattern
        """
        self.weight = zeros((self.N,self.N)) # primarily creates a matrix of self.N times self.N dimensions that will house all the weights. 
        
        for i in range(self.N):
            for j in range(self.N):
				if i != j: # w_ii = 0 since all the weights add up symmetrically. 
					self.weight[i,j] = 1./self.N * sum(self.pattern[mu, i] * self.pattern[mu,j] for mu in range(self.P)) # the weights are not calculated for each pattern separately, but once for all of them
        
    def set_init_state(self,mu,flip_ratio):
        self.x = copy(self.pattern[mu]) # duplicate pattern mu as test pattern and save it as self.x
        flip = permutation(arange(self.N)) #create a random array of length self.N
        idx = int(self.N*flip_ratio) # define how many elements should be flipped
        self.x[flip[0:idx]] *= -1 # flip ids number of array
        self.t = [0] #set the inital time step to 0
        overlap = [self.overlap(mu)] # set the initial overlap to that of the pattern to iself

    def energy(self):
        """
            DEFINITION
            calculates the energy function of the pattern at a given state
        """
        e = 0        
        for i in range(self.N):
            for j in range(self.N):
                e = e + self.weight[i,j] * self.x[i] * self.x[j]
        return -e

    def dynamic(self):
        """
        DEFINITION
        executes one step of the dynamics

        -L.Ziegler 03.2009.
        """

        h = sum(self.weight*self.x,axis=1)
        self.x = sign(h)
    
    def dynamic_seq(self,j):
        """
            DEFINITION
            flips one pixel after the other and increases the timestep once all pixels have been flipped
            
            CONDITION
            for loop is required for i
            
        """
        """
           if sum(self.weight*self.x,axis=1)[j] == 0:
            self.x[j] = 1
        else:
        """
        h=sum(self.weight*self.x,axis=1)[j]
        self.x[j]=h
    
    def overlap(self,mu=0):
        """
        DEFINITION
        computes the overlap of the test pattern with pattern nb mu

        INPUT
        mu: the index of the pattern to compare with the test pattern

        -L.Ziegler 03.2009.
        """

        return dot(self.pattern[mu],self.x)/self.N

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
        #figure()
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
            """
            # run a step
            self.dynamic()
            overlap.append(self.overlap(mu))
            energy.append(self.energy())
            t.append(i+1)
            """
            
            #update each field sequentially
            for j in range(self.N):
                self.dynamic_seq(j)
                overlap.append(self.overlap(mu))
                energy.append(self.energy())
                t.append(i+divide(j,float(self.N)))
            
            print overlap
            print energy
            print t
            
            # update the plotted data
            g1.set_data(t,energy)
            g2.set_data(t,overlap)
            
            # update the figure so that we see the changes
            draw()
            
            # check the exit condition
            i_fin = i+1
            if sum(abs(x_old-self.x))==0:
                break
            x_old = copy(self.x)
            #sleep(0.5)
        print 'pattern recovered in %i time steps with final overlap %.3f and energy %.3f'%(i_fin,overlap[-1],energy[-1])
        show()
        return overlap[-1]
