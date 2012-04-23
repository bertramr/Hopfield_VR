from HopfieldNetwork import HopfieldNetwork

def main():
	h = HopfieldNetwork(N=200)
	h.run(P=5, mu=0, flip_ratio=0.2)

if __name__=="__main__":
	main()
