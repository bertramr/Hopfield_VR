from pylab import *
from numpy import *
from copy import copy
from time import sleep, strftime
tmax = 20

class HopfieldNetwork:
    def __init__(self,N):
        self.N = N
        """
            DEFINITION
            initialization of the class

            INPUT
            N: size of the network, i.e. if N=10 
            it will consists of 10 pixels

        """

    def create_pattern(self,P=5,ratio=0.5):
        """
            DEFINITION
            creates P patterns where the ratio of -1 to 1 
            pixels is "ratio"
            
            INPUt
            P: Number of patterns
            ratio: ratio of 1/-1 pixels
        """
            
        self.P = P

        #creates an array of ones of length self.N and 
        #height P of type int
        self.pattern = -ones((P,self.N),int) 
        
        #defines how many cells should be 1
        idx = int(ratio*self.N) 
        
        for i in range(P):
            # sets the first idx cells to 1
            self.pattern[i,:idx] = 1 

            #permutates the cells to create
            # a random order ot 1 and -1 cells
            self.pattern[i] = permutation(self.pattern[i]) 

    def calc_weight(self):
        """
            DEFINITION
            creates a matrix with all the weights
            corresponsing to the pattern self.pattern
        """
        self.weight=1./self.N*np.dot((self.pattern[:,:]).T,self.pattern[:,:])
        
    def set_init_state(self,mu,flip_ratio):
        self.x=np.zeros((1,self.N))
        
        # duplicate pattern mu as test pattern and save it as self.
        self.x[0,:] = self.pattern[mu,:]

        #create a random array of length self.N
        flip = permutation(arange(self.N))   

        # define how many elements should be flipped
        idx = int(self.N*flip_ratio) 
        
        # flip ids number of array
        self.x[0,flip[0:idx]] *= -1         

        #set the inital time step to 0
        self.t = [0]         
        
        # set the initial overlap to that of the pattern to iself
        overlap = [self.overlap(mu)]     

    def energy(self):
        """
            DEFINITION
            calculates the energy function of the pattern at a given state
        """
        e=-np.dot(self.x,np.dot(self.weight,(self.x).T))
        return e[0,0]
    
    def dynamic_seq(self,j):
        """
            DEFINITION
            flips one pixel after the other and increases the
            timestep once all pixels have been flipped
            
            CONDITION
            for loop is required for i
            
        """

        if sign(np.dot(self.x[:,:],self.weight[:,:])[0,j])==0:
            self.x[0,j]=1
        else:
            self.x[0,j]=sign(np.dot(self.x[:,:],self.weight[:,:])[0,j])
    
    def overlap(self,mu=0):
        
        return np.dot(self.pattern[mu,:],self.x[0,:])/float(self.N)

    def normalized_pixel_distance(self,mu=0):
        return (1-self.overlap(mu))/2
    
    def run(self,P=5, ratio=0.5, mu=0, flip_ratio=0.2, bPlot=True):
                
        self.create_pattern(P, ratio)
        self.calc_weight()
        self.set_init_state(mu,flip_ratio)

        t = [0]
        overlap = [self.overlap(mu)]
        energy = [self.energy()]
        normalized_pixel_distance = [self.normalized_pixel_distance()]

        if bPlot:
            # prepare the figure
            figure()

            # plot the time course of the energy
            subplot(311)
            g1, = plot(t,energy,'b',lw=2)
            axis([0,tmax,-self.N*5,0])
            xlabel('time step')
            ylabel('energy')
            grid('on')
        
            # plot the time course of the overlap
            subplot(312)
            g2, = plot(t,overlap,'b',lw=2) # we keep a handle to the curve
            axis([0,tmax,-1,1])
            xlabel('time step')
            ylabel('overlap')
            grid('on')
        
            # plot the time course of the normalized pixel distance
            subplot(313)
            g3, = plot(t,normalized_pixel_distance,'b',lw=2) # we keep a handle to the curve
            axis([0,tmax,0,1])
            xlabel('time step')
            ylabel('normalized pixel distance')
            grid('on')
            
        
            # this forces pylab to update and show the fig.
            draw()
        
        x_old = copy(self.x)
        
        for i in range(tmax):
            
            #update each field sequentially
            s=1
            for j in permutation(range(self.N)):
                self.dynamic_seq(j)
                overlap.append(self.overlap(mu))
                energy.append(self.energy())
                t.append(i+divide(s,float(self.N)))
                s+=1
            
            if bPlot:
                # update the plotted data
                g1.set_data(t,energy)
                g2.set_data(t,overlap)
                g3.set_data(t,normalized_pixel_distance)    

            
                # update the figure so that we see the changes
                draw()
            
            # check the exit condition
            i_fin = i+1
            if sum(abs(x_old-self.x))==0:
                break
            x_old = copy(self.x)

        print 'pattern recovered in %i time steps with final overlap %.3f and energy %.3f'%(i_fin,overlap[-1],energy[-1])
        
        if bPlot:
            show()
            savefig('../tex/img/plots/energy_overlap-%s.png' % (strftime('%s')))
            close()

        return overlap[-1]

