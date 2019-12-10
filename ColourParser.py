import os
from PIL import Image
from itertools import product

class ColourParser:
	def parseColours(imgName, Grouped=False):
		if imgName in os.listdir():
			im = Image.open(imgName)
			pix = im.load()
			size = im.size
			print("Parsing image of size", size)
			if Grouped:
				colours = {}
				for i, j in product(range(size[0]), range(size[1])):
					if pix[i, j] not in colours:
						colours[pix[i, j]] = 1
					else:
						colours[pix[i, j]] += 1
				return colours
			else:
				colours = []
				for i, j in product(range(size[0]), range(size[1])):
					colours.append(pix[i, j])
				return colours
		else:
			print("No such file")
		return -1

	def splitRGB(colours):
		R = []
		G = []
		B = []
		for colour in colours:
			R.append(colour[0])
			G.append(colour[1])
			B.append(colour[2])
		return R, G, B

	def mostCommonColours(colours, n):
		mostCommonColours = sorted(colours, key=colours.get)[-n:]
		return mostCommonColours
