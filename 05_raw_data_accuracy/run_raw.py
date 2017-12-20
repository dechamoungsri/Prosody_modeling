
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
    Y = []

    for syl in db:

        if syl['stress'] == '2':
            real.append(1)
        elif syl['stress'] in ['0' , '1']:
            real.append( int(syl['stress']) )
        else :
            print syl['stress']
            real.append( int(syl['stress']) )

        Y.append(syl['TF']['intepolate151_normalize_by_preprocessing.normalize']['data'])

        # sys.exit()

    real = np.array(real)
    Y = np.array(Y)

    return (Y,real)

    pass

def run_processor(db_file, name_out_path, name):

    Y, real = run_data_processor(db_file)

    inverselengthscale = np.ones(len(Y[0]))

    real = map(int, real)

    acc_score = 0.0
    f1_score = None
    best_cluster = 2
    best_neighbors = 0.025
    best_pred = None
    best_subset_1 = None
    best_subset_0 = None

    for n_cluster in [2,3,4,5]:
        for n_neighbors in [0.025, 0.05, 0.075, 0.1, 0.2, 0.5, 0.75, 0.8, 0.9]:
            labels = link_clustering(Y, inverselengthscale, n_cluster, n_neighbors)
            Utility.save_obj(labels, '{}/n_cluster_{}_n_neighbors_{}x.pkl'.format(name_out_path, n_cluster, n_neighbors) )

            log.append('Name {}, Neighbor : {}, N_cluster : {}'.format(name, n_neighbors, n_cluster))
            log.append('result set : {}'.format(set(labels)))

            print 'Cluster : {}'.format(n_cluster)
            print 'Neighbor : {}'.format(n_neighbors)
            print 'result set : {}'.format(set(labels))

            for s in set(labels):
                print s, len(labels[labels==s])
                log.append('{} : {}'.format(s, len(labels[labels==s])))

            log_cal_path = '{}/n_cluster_{}_n_neighbors_{}x.txt'.format(name_out_path, n_cluster, n_neighbors)
            acc, f1, pred, subset_1, subset_0 = cal_accuracy_and_f1(real, labels, log_cal_path)

            log.append('Sebset 1 : {}'.format(subset_1))
            log.append('Sebset 0 : {}'.format(subset_0))
            log.append('acc : {}'.format(acc))
            log.append('f1 : {}'.format(f1))

            if acc > acc_score:
                acc_score = acc
                best_cluster = n_cluster
                best_neighbors = n_neighbors
                f1_score = f1
                best_pred = pred
                best_subset_1 = subset_1
                best_subset_0 = subset_0

        # sys.exit()

    log.append('------------------------------')

    print 'Name : {}'.format(name)
    print 'Subset 1 : {}'.format(best_subset_1)
    print 'Subset 0 : {}'.format(best_subset_0)
    print 'Best nc : {}'.format(best_cluster)
    print 'Best ng : {}'.format(best_neighbors)
    print 'Best acc : {}'.format(acc_score)
    print 'Best f1 : {}'.format(f1_score)

    log.append('Name : {}'.format(name))
    log.append('Best nc : {}'.format(best_cluster))
    log.append('Best ng : {}'.format(best_neighbors))
    log.append('Best acc : {}'.format(acc_score))
    log.append('Best f1 : {}'.format(f1_score))
    log.append('Subset 1 : {}'.format(best_subset_1))
    log.append('Subset 0 : {}'.format(best_subset_0))

    Utility.save_obj(best_pred, '{}/prediction_labels.pkl'.format(name_out_path))

    log.append('------------------------------')

    pass

def cal_accuracy_and_f1(real, pred, log_cal_path):

    log_cal = []

    pred = np.array(pred)

    s = set(pred)

    ret = (0.0, 0.0, 0.0, None, None)

    for i in xrange(1, len(s)-1):

        ss = Utility.findsubsets(s, i)

        for a in ss:

            pred_1 = np.copy(pred)
            pred_2 = np.copy(pred)

            set_1 = set(a)
            set_2 = s-set(a)

            for e in set_1:
                pred_1[pred_1==e] = 999
            for e in set_2:
                pred_1[pred_1==e] = 555

            pred_1[pred_1==999] = 1
            pred_1[pred_1==555] = 0

            pred_2[pred_1==1] = 0
            pred_2[pred_1==0] = 1

            print set(pred_1)

            acc_1 = accuracy_score(real, pred_1) 
            f1_1 = f1_score(real, pred_1, average=None) 

            acc_2 = accuracy_score(real, pred_2) 
            f1_2 = f1_score(real, pred_2, average=None) 

            print acc_1, f1_1
            print acc_2, f1_2

            log_cal.append('---------------------------------------')
            log_cal.append('SubSet : {}'.format(ss))
            log_cal.append('Set 1 : {}'.format(set_1))
            log_cal.append('Set 2 : {}'.format(set_2))
            log_cal.append('Acc 1 : {}'.format(acc_1))
            log_cal.append('Acc 2 : {}'.format(acc_2))
            log_cal.append('F1 1 : {}'.format(f1_1))
            log_cal.append('F2 2 : {}'.format(f1_2))
            # log_cal.append('---------------------------------------')

            if acc_1 > ret[0]:
                ret = (acc_1, f1_1, pred_1, set_1, set_2)

            if acc_2 > ret[0]:
                ret = (acc_2, f1_2, pred_2, set_2, set_1)

    Utility.write_to_file_line_by_line(log_cal_path, log_cal)
    return ret

    pass

log = []

if __name__ == '__main__':

    db_path = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/13_merge_vowel_08c/'

    out_path = '/work/w23/decha/decha_w23/Second_Journal/Unsupervised_learning_result/00a_raw_data_rerun/'

    for t in xrange(5):
        for f in ['nasal', 'no', 'non-nasal']:
            name = '{}_{}'.format(t, f)

            db_file = '{}/{}.npy'.format(db_path, name)

            name_out_path = '{}/{}/'.format(out_path, name)

            if Utility.is_file_exist(db_file):
                Utility.make_directory(name_out_path)
                run_processor(db_file, name_out_path, name)
                # sys.exit()

    Utility.write_to_file_line_by_line('{}/log.txt'.format(out_path), log)

    pass
