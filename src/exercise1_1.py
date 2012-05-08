from Hopfield import HopfieldNetwork

def exercise1_1():
    '''
    Implement the Hopfield network as described above. [...] 
    For the first two unit steps of the retrieval of one pattern
    plot the changing values of the energy function and the
    overlap of the network with the pattern as the state of 
    each node is sequentially updated
    '''
    
    print "Exercise 1.1:"
    h = HopfieldNetwork(N=200)
    h.run(P=5, flip_ratio=0.2)

if __name__=="__main__":
    exercise1_1()
