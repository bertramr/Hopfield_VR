import Image
from copy import copy
from time import sleep
from pylab import *

plot_dic={'cmap':cm.gray,'interpolation':'nearest'}

tmax = 20

class hopfield_network:
    def __init__(self,N):
        self.N = N
        """
        DEFINITION
        initialization of the class

        INPUT
        N: size of the network, i.e. if N=10 it will consists of 10x10 pixels

        -L.Ziegler 03.2009.
        """

    def make_pattern(self,P=1,ratio=0.5,letters=None):
        """
        DEFINITION
        creates and stores patterns

        INPUT
        P: number of patterns (used only for random patterns)
        ratio: percentage of 'on' pixels for random patterns
        letters: to store characters use as input a string with the desired letters
            ex. make_pattern(letters='abcdjft')

        -L.Ziegler 03.2009.
        """

        if letters:
            if self.N!=10:
                raise ValueError, 'the network size must be equal to 10'
            alph = alphabet()
            self.pattern = -ones((len(letters),self.N**2),int)
            idx = 0
            for i in letters:
                self.pattern[idx] = alph.__dict__[i]
                idx += 1
        else:
            self.pattern = -ones((P,self.N**2),int)
            idx = int(ratio*self.N**2)
            for i in range(P):
                self.pattern[i,:idx] = 1
                self.pattern[i] = permutation(self.pattern[i])
        self.weight = zeros((self.N**2,self.N**2))
        for i in range(self.N**2):
            self.weight[i] = 1./self.N**2*sum(self.pattern[k,i]*self.pattern[k] for k in range(self.pattern.shape[0]))

    def grid(self,mu=None):
        """
        DEFINITION
        reshape an array of length NxN to a matrix NxN

        INPUT
        mu: None -> reshape the test pattern x
            an integer i < P -> reshape pattern nb i

        -L.Ziegler 03.2009.
        """

        if mu is not None:
            x_grid = reshape(self.pattern[mu],(self.N,self.N))
        else:
            x_grid = reshape(self.x,(self.N,self.N))
        return x_grid

    def dynamic(self):
        """
        DEFINITION
        executes one step of the dynamics

        -L.Ziegler 03.2009.
        """

        h = sum(self.weight*self.x,axis=1)
        self.x = sign(h)

    def overlap(self,mu):
        """
        DEFINITION
        computes the overlap of the test pattern with pattern nb mu

        INPUT
        mu: the index of the pattern to compare with the test pattern

        -L.Ziegler 03.2009.
        """

        return 1./self.N**2*sum(self.pattern[mu]*self.x)

    def run(self,mu=0,flip_ratio=0):
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
        
        try:
            self.pattern[mu]
        except:
            raise IndexError, 'pattern index too high'
        
        # set the initial state of the net
        self.x = copy(self.pattern[mu])
        flip = permutation(arange(self.N**2))
        idx = int(self.N**2*flip_ratio)
        self.x[flip[0:idx]] *= -1
        t = [0]
        overlap = [self.overlap(mu)]
        
        # prepare the figure
        figure()
        
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
            
            # update the plotted data
            g1.set_data(self.grid())
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


class alphabet():
    def __init__(self):
        """
        DEFINITION
        loads the gif files in alphabet/ and stores them as arrays of length 10x10

        -L.Ziegler 03.2009.
        """

        for i in 'abcdefghijklmnopqrstuvwyxz':
            im = Image.open('alphabet/'+i+'.gif')
            pix = array(list(im.getdata()))
            self.__dict__[i]= sign(pix-1)
