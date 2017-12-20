
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('../../GPy-devel/')
sys.path.append('../../paramz-master/')
sys.path.append('../../library/')

from tool_box.util.utility import Utility
from sklearn.cluster import AgglomerativeClustering
from sklearn.neighbors import kneighbors_graph

import numpy as np
import matplotlib.pyplot as plt

import matplotlib

import GPy

def link_clustering(x, inverselengthscale, n_clusters, n_neighbors):

    global log

    linkage = 'complete'
    log.append('linkage : {}'.format(linkage))

    # n_clusters = 2
    # n_neighbors = int(len(x)*0.05)

    # print 'n_neighbors : ', n_neighbors

    knn_graph = kneighbors_graph(x, n_neighbors, include_self=False)

    lengthscale=1/np.array(inverselengthscale, dtype=float)
    k = GPy.kern.RBF(len(x[0]), ARD=True, lengthscale=lengthscale)

    XX = -1*np.log(k.K(x, x))

    clustering = AgglomerativeClustering(linkage=linkage, n_clusters=n_clusters, affinity='precomputed', connectivity=knn_graph)
    clustering.fit(XX)

    labels = clustering.labels_
    # print labels
    for s in set(labels):
        log.append('Cluster : {}, Size : {}'.format(s, len(labels[labels==s])))

    return labels

def plot(data, inverselengthscale, labels, name_out_file, title):

    most_dominants = Utility.get_input_sensitivity(inverselengthscale, 2)

    x = data[ :, most_dominants[0] ]
    y = data[ :, most_dominants[1] ]

    label = map(int, labels)
    label = np.array(labels)

    # print set(labels)

    # colors = ['red','green','blue','purple']

    colors = Utility.get_color_map(len(set(labels)))

    plt.clf()
    # plt.scatter(x, y, c=labels, cmap=matplotlib.colors.ListedColormap(colors))
    for idx, s in enumerate( sorted( set(labels)) ):
        plt.scatter(x[labels==s], y[labels==s], c=colors[idx] , label=s)
    plt.legend()
    plt.title(title)

    plt.savefig( name_out_file )

def link_cluster_caller(name, base_path, db_file, name_out_path):

    global log

    x = Utility.load_obj('{}/x.pkl'.format(base_path))
    inverselengthscale = Utility.load_obj('{}/input_sensitivity.pkl'.format(base_path))

    for n_clusters in xrange(2, 6):
        for mul in [0.2]:

            n_neighbors = int( len(x)*mul )

            title = 'param_n_cluster_{}_n_neighbors_{}x'.format(n_clusters, mul)
            name_out_file = '{}/{}.eps'.format(name_out_path, title)

            log.append(title)
            log.append('n_cluster : {}'.format(n_clusters))
            log.append('n_neighbors for kernel : {}'.format(n_neighbors))

            labels = link_clustering(x, inverselengthscale, n_clusters, n_neighbors)
            plot(x, inverselengthscale, labels, name_out_file, title)

            Utility.save_obj(labels, '{}/{}.pkl'.format(name_out_path, title) )


    Utility.write_to_file_line_by_line('{}/{}_log.txt'.format(name_out_path, name), log)

    pass

log = []
if __name__ == '__main__':

    model_path = '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/14_merge_vowel_13_data/input_dim_10/'
    db_path = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/13_merge_vowel_08c/'
    out_path = '/work/w23/decha/decha_w23/Second_Journal/Unsupervised_learning_result/15_Agglomerative_clustering/' 

    for t in xrange(5):
        for f in ['nasal', 'no', 'non-nasal']:
            # for v in ['long', 'short']:
            name = '{}_{}'.format(t, f)

            db_file = '{}/{}.npy'.format(db_path, name)

            name_out_path = '{}/{}/'.format(out_path, name)
            
            base_path = '{}/{}/'.format(model_path, name)

            if Utility.is_file_exist(db_file):

                print name

                Utility.make_directory(name_out_path)
                log = []

                link_cluster_caller(name, base_path, db_file, name_out_path)

        # sys.exit()


    pass
