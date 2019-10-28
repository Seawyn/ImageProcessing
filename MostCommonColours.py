import os
import sys
from PIL import Image
from itertools import product

def parseColours(imgName):
	if imgName in os.listdir():
		im = Image.open(imgName)
		pix = im.load()
		size = im.size
		colours = {}
		print("Parsing image of size", size)
		for i, j in product(range(size[0]), range(size[1])):
			if pix[i, j] == (0, 0, 0):
				print(i, j)
			if pix[i, j] not in colours:
				colours[pix[i, j]] = 1
			else:
				colours[pix[i, j]] += 1
		return colours
	else:
		print("No such file")
		return -1

def mostCommonColours(colours, n):
	mostCommonColours = sorted(colours, key=colours.get)[-n:]
	return mostCommonColours

def main():
	if len(sys.argv) != 5:
		print("Please input your arguments in the following order:")
		print("[Script] -f [filename] -n [number of colours]")
		return -1
	colours = parseColours(sys.argv[2])
	for colour in mostCommonColours(colours, int(sys.argv[4])):
		print(colour, "-", colours[colour], "pixels")

main()
