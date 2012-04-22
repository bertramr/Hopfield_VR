from my_hopfield_network import HopfieldNetwork

def main():
	h = HopfieldNetwork(N=10)
	h.make_pattern(P=1,ratio=0.5)
	h.run(mu=0, flip_ratio=0.4)

if __name__=="__main__":
	main()
