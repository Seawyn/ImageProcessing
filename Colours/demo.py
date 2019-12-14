import sys
from ColourCluster import *

def main(argv):
	k = 5
	filename = argv[0]
	if len(argv) < 0:
		print("Please input your arguments in the following order:")
		print("demo.py <filename> [number of clusters]")
		sys.exit(2)
	else:
		filename = argv[0]
		if len(argv) > 1:
			k = int(argv[1])
		(colours, labels) = kmeansClustering(filename, k)
		processColours(colours, labels.tolist(), k)

if __name__== "__main__":
	main(sys.argv[1:])
