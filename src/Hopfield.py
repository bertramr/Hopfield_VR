from pylab import *
from numpy import *
from copy import copy
from time import sleep, strftime

tmax = 20

class HopfieldNetwork:
    def __init__(self):
        """
            DEFINITION
            initialization of the class

        """

    def create_pattern(self,P=5,ratio=0.5):
        """
            DEFINITION
            creates P patterns where the ratio of 1 to total 
            pixels is "ratio"
            
            INPUt
            P: Number of patterns
            ratio: ratio of 1/to pixels
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
        return (1-self.overlap(mu))/2

    def init_excitatory(self, percentage=0.5):
        idx_exc = int(percentage * self.N)
        idx_inh = int((1-percentage) * self.N)

        flip = permutation(arange(self.N)) 
        
        self.excitatory_nodes = flip[0:idx_exc]
        self.inhibitory_nodes = flip[idx_exc+1:]
        #print self.excitatory_nodes
        
        for i in self.excitatory_nodes:
            self.weight[i, self.weight[i,:] > 0 ] = 0
        
        for i in self.inhibitory_nodes:
            self.weight[i, self.weight[i,:] < 0 ] = 0

    def run(self, N=200, P=5, ratio=0.5, mu=0, flip_ratio=0.2, pcut=0, excitatory=-1, bPlot=True, bDebug=False):
        
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
        
        for i in range(tmax):
            
            #update each field sequentially
            s=1
            for j in permutation(range(self.N)):
                self.dynamic_seq(j)
                overlap.append(self.overlap(mu))
                energy.append(self.energy())
                normalized_pixel_distance.append(self.normalized_pixel_distance(mu))
                t.append(i+divide(s,float(self.N)))
                s+=1
            
            # check the exit condition
            i_fin = i+1
            if sum(abs(x_old-self.x))==0:
                break
            x_old = copy(self.x)
                
        if bPlot:
            # prepare the figure
            figure(num=None, figsize=(7, 8), dpi=80, facecolor='w', edgecolor='k')
    
            # plot the time course of the energy
            subplot(311)
            g1, = plot(t,energy,'b',lw=2)
            axis('auto')
            xlim(0, 2) 
            #xlabel('time step')
            ylabel('energy')
            grid('on')
        
            # plot the time course of the overlap
            subplot(312)
            g2, = plot(t,overlap,'b',lw=2) # we keep a handle to the curve
            axis('auto')
            xlim(0,2)
            #xlabel('time step')
            ylabel('overlap')
            grid('on')
        
            # plot the time course of the normalized pixel distance
            subplot(313)
            g3, = plot(t,normalized_pixel_distance,'b',lw=2) # we keep a handle to the curve
            axis('auto')
            xlim(0,2)
            xlabel('time step')
            ylabel('normalized pixel distance')
            grid('on')            
        
            # this forces pylab to update and show the fig.
            draw()
            show()
            savefig('../tex/img/plots/energy_overlap-%s.png' % (strftime('%s')))
            close()
        
        #print 'pattern recovered in %i time steps with final overlap %.3f and energy %.3f'%(i_fin,overlap[-1],energy[-1]) 
        return normalized_pixel_distance[-1]

