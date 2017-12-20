
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('../GPy-devel/')
sys.path.append('../paramz-master/')
sys.path.append('../library/')

import GPy

from tool_box.util.utility import Utility

from sklearn.cluster import AgglomerativeClustering
from sklearn.neighbors import kneighbors_graph

import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score

def link_clustering(x, inverselengthscale, n_clusters, n_neighbors):

    global log

    linkage = 'complete'

    log.append('Linkage : {}'.format(linkage))
    log.append('n_clusters : {} , n_neighbors : {}'.format(n_clusters, n_neighbors))

    # print n_neighbors, x.shape
    n_neighbors = int(len(x)*n_neighbors)

    knn_graph = kneighbors_graph(x, n_neighbors, include_self=False)

    lengthscale=1/np.array(inverselengthscale, dtype=float)
    k = GPy.kern.RBF(len(x[0]), ARD=True, lengthscale=lengthscale)

    XX = -1*np.log(k.K(x, x))

    clustering = AgglomerativeClustering(linkage=linkage, n_clusters=n_clusters, affinity='precomputed', connectivity=knn_graph)
    clustering.fit(XX)

    labels = clustering.labels_

    return labels

def run_data_processor(db_file):

    db = Utility.load_obj(db_file)

    real = []
    # Y = []

    for syl in db:

        if syl['stress'] == '2':
            real.append(1)
        elif syl['stress'] in ['0' , '1']:
            real.append( int(syl['stress']) )
        else :
            print syl['stress']
            real.append( int(syl['stress']) )

        # Y.append(syl['TF']['intepolate151_normalize_by_preprocessing.normalize']['data'])

        # sys.exit()

    real = np.array(real)
    # Y = np.array(Y)

    return real

    pass

def run_processor(db_file, name_out_path, name, base_path):

    real = run_data_processor(db_file)

    Y = Utility.load_obj('{}/x.pkl'.format(base_path))
    inverselengthscale = Utility.load_obj('{}/input_sensitivity.pkl'.format(base_path))

    real = map(int, real)

    acc_score = 0.0
    f1_score = None
    best_neighbors = 0.025
    best_pred = None

    for n_neighbors in [0.025, 0.05, 0.075, 0.1, 0.2, 0.5, 0.75, 0.8, 0.9]:
        labels = link_clustering(Y, inverselengthscale, 2, n_neighbors)
        Utility.save_obj(labels, '{}/n_neighbors_{}x.pkl'.format(name_out_path, n_neighbors))

        log.append('Name {}, Neighbor : {}'.format(name, n_neighbors))
        log.append('result set : {}'.format(set(labels)))

        print 'Neighbor : {}'.format(n_neighbors)
        print 'result set : {}'.format(set(labels))

        for s in set(labels):
            print s, len(labels[labels==s])
            log.append('{} : {}'.format(s, len(labels[labels==s])))

        acc, f1, pred = cal_accuracy_and_f1(real, labels)
        log.append('acc : {}'.format(acc))
        log.append('f1 : {}'.format(f1))

        if acc > acc_score:
            acc_score = acc
            best_neighbors = n_neighbors
            f1_score = f1
            best_pred = pred

        # sys.exit()

    log.append('------------------------------')

    print 'Name : {}'.format(name)
    print 'Best ng : {}'.format(best_neighbors)
    print 'Best acc : {}'.format(acc_score)
    print 'Best f1 : {}'.format(f1_score)

    log.append('Name : {}'.format(name))
    log.append('Best ng : {}'.format(best_neighbors))
    log.append('Best acc : {}'.format(acc_score))
    log.append('Best f1 : {}'.format(f1_score))

    Utility.save_obj(best_pred, '{}/prediction_labels.pkl'.format(name_out_path))

    log.append('------------------------------')

    pass

def cal_accuracy_and_f1(real, pred):
    # print real, pred
    pred = np.array(pred)
    
    acc_1 = accuracy_score(real, pred) 
    f1_1 = f1_score(real, pred, average=None) 

    swap = np.copy(pred)
    swap[swap==0] = 555
    swap[swap==1] = 999

    swap[swap==555] = 1
    swap[swap==999] = 0

    acc_2 = accuracy_score(real, swap) 
    f1_2 = f1_score(real, swap, average=None) 

    print acc_1, f1_1
    print acc_2, f1_2

    if acc_1 > acc_2:
        return (acc_1, f1_1, pred)
    else:
        return (acc_2, f1_2, swap)

    pass

log = []

if __name__ == '__main__':

    db_path = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/13_merge_vowel_08c/'

    out_path = '/work/w23/decha/decha_w23/Second_Journal/Unsupervised_learning_result/01_gplvm_link_clustering_accuracy/'

    model_path = '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/14_merge_vowel_13_data/input_dim_10/'

    for t in xrange(5):
        for f in ['nasal', 'no', 'non-nasal']:
            name = '{}_{}'.format(t, f)

            db_file = '{}/{}.npy'.format(db_path, name)

            name_out_path = '{}/{}/'.format(out_path, name)

            base_path = '{}/{}/'.format(model_path, name)

            if Utility.is_file_exist(db_file):
                Utility.make_directory(name_out_path)
                run_processor(db_file, name_out_path, name, base_path)
                # sys.exit()

    Utility.write_to_file_line_by_line('{}/log.txt'.format(out_path), log)

    pass
