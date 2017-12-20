
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('../../GPy-devel/')
sys.path.append('../../paramz-master/')
sys.path.append('../../library/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import DBSCAN
import GPy

import matplotlib

def run_dbscan(x, inverselengthscale, eps, m, out_base_path):

    lengthscale=1/np.array(inverselengthscale, dtype=float)
    k = GPy.kern.RBF(len(x[0]), ARD=True, lengthscale=lengthscale)
    XX = -1*np.log(k.K(x, x))

    mins = len(x)*0.05
    print mins

    db = DBSCAN(eps=eps, min_samples=mins, metric='precomputed').fit(XX)
    labels = db.labels_                
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

    for s in set(labels):
        print s, len(labels[labels==s])

    plot(x, inverselengthscale, labels, out_base_path)

    pass

def plot(data, inverselengthscale, labels, out_base_path):
    most_dominants = Utility.get_input_sensitivity(inverselengthscale, 2)

    x = data[ :, most_dominants[0] ]
    y = data[ :, most_dominants[1] ]

    label = map(int, labels)
    label = np.array(labels)

    print set(labels)

    colors = Utility.get_color_map(len(set(labels)))

    plt.clf()

    for idx, s in enumerate( sorted( set(labels)) ):
        print s
        plt.scatter(x[labels==s], y[labels==s], c=colors[idx] , label=s)
    plt.legend()
    plt.savefig( '{}/dbscan_result.eps'.format(out_base_path) )

def find_distance_stat(x, inverselengthscale, out_base_path, bar_scale=100000000000):

    lengthscale=1/np.array(inverselengthscale, dtype=float)
    k = GPy.kern.RBF(len(x[0]), ARD=True, lengthscale=lengthscale)

    XX = -1*np.log(k.K(x, x))
    XX[XX==0] = 1000000000

    print 'min'
    XXX = XX.min(axis=1)

    print XXX.shape

    bin = int( len(x) )

    hist = np.histogram(XXX, bins=bin)
    print hist

    plt.clf()

    lab = (hist[1])[0:bin]*bar_scale

    print lab

    plt.bar(lab, hist[0])
    plt.savefig('{}/distance_histogram.eps'.format(out_base_path))

    max_x = XXX.shape[0]
    c = 0
    tar = 0
    for idx, f in enumerate(hist[0]):
        c = c + f
        if c > max_x*0.95:
            print hist[1][idx], idx
            tar = idx
            break

    ng_list = []
    for data in XX:
        ng_list.append( len(data[data<hist[1][tar]]) )

    ng_list = np.array(ng_list)

    bin = max(ng_list)
    hist2 = np.histogram(ng_list, bins=bin)
    lab = (hist2[1])[0:bin]

    print hist2

    plt.clf()
    plt.bar(lab, hist2[0])
    plt.savefig('{}/number_of_neighbor_histogram.eps'.format(out_base_path))

    c = 0
    tar2 = 0
    for idx, f in enumerate(hist2[0]):
        if idx==0 : continue
        c = c + f
        if c > max_x*0.10:
            print hist2[1][idx], idx
            tar2 = idx
            break

    print 'Out : ', (hist[1][tar], int(hist2[1][tar2]) )
    return (hist[1][tar], int(hist2[1][tar2]) )

    pass

def call_run_dbscan(data_path, inverselengthscale_path, out_base_path):

    x = Utility.load_obj(data_path)

    print x.shape

    inverselengthscale = Utility.load_obj(inverselengthscale_path)

    eps, m = find_distance_stat(x, inverselengthscale, out_base_path)

    run_dbscan(x, inverselengthscale, eps, m, out_base_path)

    pass

if __name__ == '__main__':

    method_path = '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/12c_normalization_by_preprocessing_of_11_data/input_dim_10/'
    out_main_path = '/work/w23/decha/decha_w23/Second_Journal/Unsupervised_learning_result/12c_normalization_by_preprocessing_of_11_data/'

    Utility.make_directory(out_main_path)

    for t in xrange(5):
        for f in ['nasal', 'no', 'non-nasal']:
            for v in ['long', 'short']:
                name = '{}_{}_{}'.format(t, v, f)

                base_path = '{}/{}/'.format(method_path, name)

                data_path = '{}/x.pkl'.format(base_path)
                inverselengthscale_path = '{}/input_sensitivity.pkl'.format(base_path)

                out_base_path = '{}/{}/'.format(out_main_path, name)
                
                if Utility.is_file_exist(data_path):
                    Utility.make_directory(out_base_path)
                    call_run_dbscan(data_path, inverselengthscale_path, out_base_path)
                else:
                    print 'no ', data_path

        # sys.exit()

    pass
