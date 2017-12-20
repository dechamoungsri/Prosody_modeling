
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('../GPy-devel/')
sys.path.append('../paramz-master/')
sys.path.append('../library/')

from tool_box.util.utility import Utility
from sklearn.cluster import AgglomerativeClustering
from sklearn.neighbors import kneighbors_graph

import numpy as np
import matplotlib.pyplot as plt

import matplotlib

import GPy

def link_clustering(x, inverselengthscale):

    linkage = 'average'
    n_clusters = 2

    n_neighbors = int(len(x)*0.05)

    print 'n_neighbors : ', n_neighbors

    knn_graph = kneighbors_graph(x, n_neighbors, include_self=False)

    lengthscale=1/np.array(inverselengthscale, dtype=float)
    k = GPy.kern.RBF(len(x[0]), ARD=True, lengthscale=lengthscale)

    XX = -1*np.log(k.K(x, x))

    clustering = AgglomerativeClustering(linkage=linkage, n_clusters=n_clusters, affinity='precomputed', connectivity=knn_graph)
    clustering.fit(XX)

    labels = clustering.labels_
    print labels
    for s in set(labels):
        print s, len(labels[labels==s])

    plot(x, inverselengthscale, labels)

def plot(data, inverselengthscale, labels):
    most_dominants = Utility.get_input_sensitivity(inverselengthscale, 2)

    x = data[ :, most_dominants[0] ]
    y = data[ :, most_dominants[1] ]

    label = map(int, labels)
    label = np.array(labels)

    print set(labels)

    colors = ['red','green','blue','purple']

    plt.clf()
    plt.scatter(x, y, c=labels, cmap=matplotlib.colors.ListedColormap(colors))
    plt.savefig( './link_clustering_test.eps' )

if __name__ == '__main__':

    x = Utility.load_obj('/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/08c_preprocessing_normaiize/input_dim_10/0_long_no/x.pkl')

    print x.shape

    inverselengthscale = Utility.load_obj('/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/08c_preprocessing_normaiize/input_dim_10/0_long_no/input_sensitivity.pkl')

    # db = Utility.load_obj(name)

    link_clustering(x, inverselengthscale)

    pass
