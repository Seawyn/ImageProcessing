from ColourParser import ColourParser
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def kmeansClustering(imgName, k):
	colours = np.array(ColourParser.parseColours(imgName))
	print("Fitting Model with KMeans Clustering...")
	kmeans = KMeans(n_clusters=k, random_state=0).fit(colours)
	return kmeans.cluster_centers_.astype(int), kmeans.labels_

def convertRGBScale(colour):
	return (colour[0] / 255, colour[1] / 255, colour[2] / 255)

def processColours(colours, labels, k):
	counter = []
	total = len(labels)
	for i in range(k):
		counter.append((labels.count(i) / total) * 100)
	fig = plt.figure()
	axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
	axes.set_xlim([0, 100])
	axes.set_ylim([0, 20])
	trace = 0
	for i in range(k):
		colour = convertRGBScale(colours[i])
		axes.add_patch(plt.Rectangle([trace, 0], counter[i], 20, facecolor = colour, edgecolor = colour))
		trace = counter[i]
	axes.set_aspect('equal')
	plt.axis("off")
	plt.show()
