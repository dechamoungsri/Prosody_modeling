
import sys

sys.path.append('../../GPy-devel/')

import GPy

from sklearn.decomposition import PCA

class GPy_Interface(object):
    """docstring for GPy_Interface"""
    def __init__(self, arg):
        super(GPy_Interface, self).__init__()
        self.arg = arg
     
    @staticmethod
    def pca(config):

        n_components = config['n_components']
        Y = config['data']

        pca = PCA(n_components=n_components)
        # Y_r = pca.fit(Y).transform(Y)
        Y_r = pca.fit_transform(Y)

        print pca.explained_variance_ratio_

        return (pca, Y_r)

        pass

    @staticmethod
    def Bayesian_GPLVM_Training(config):

        input_dim = config['input_dim']
        Y = config['data']
        num_inducing = config['num_inducing']
        max_iters = config['max_iters']
        missing_data = config['missing_data']
        optimize_algo = config['optimize_algo']

        k = GPy.kern.RBF(input_dim, ARD=True)

        print 'start training'

        m = GPy.models.BayesianGPLVM(Y, input_dim, kernel=k, num_inducing=num_inducing, missing_data=True)

        print 'start optimization'
        print 'Max iters : ', max_iters
        m.optimize(optimize_algo, messages=1, max_iters=max_iters)

        return m
