import sys
from ColourCluster import *

def main(argv):
	k = 5
	filename = argv[0]
	(colours, labels) = kmeansClustering(filename, k)
	processColours(colours, labels.tolist(), k)

if __name__== "__main__":
	main(sys.argv[1:])
