from ColourParser import ColourParser
import numpy as np
from sklearn.cluster import KMeans

def kmeansClustering(imgName):
	colours = np.array(ColourParser.parseColours(imgName))
	print("Fitting Model with KMeans Clustering...")
	kmeans = KMeans(n_clusters=10, random_state=0).fit(colours)
	print(kmeans.cluster_centers_.astype(int))
	print(kmeans.labels_)
