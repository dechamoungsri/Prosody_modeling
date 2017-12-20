
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('../GPy-devel/')
sys.path.append('../paramz-master/')
sys.path.append('../Syllable/')

from tool_box.util.utility import Utility

from Syllable_Object import Syllable

import numpy as np
import matplotlib.pyplot as plt

import GPy

if __name__ == '__main__':

    db = Utility.load_obj('/work/w2/decha/Data/GPR_speccom_data/syllable_database/03_data_with_missing_for_training/4_long_nasal.npy')

    # print db[0]
    # # Syllable.interpolate(db[0]['raw_lf0'])
    # Syllable.get_normailze_with_missing_data(db[0]['raw_lf0'], 50, db[0]['dur'])

    Syllable.get_normalize_gradient_interpolation(db[413]['raw_lf0'], 50, db[413]['dur'])

    # print db[432]
    # Syllable.interpolate(db[432]['raw_lf0'])

    # m = GPy.examples.dimensionality_reduction.bgplvm_test_model()

    # print m
    # print m.input_sensitivity()
    # print np.array( m.X.mean )

    # input_dim = 10
    # num_inputs = 100
    # num_inducing = 5

    # output_dim = 5

    # X = np.random.rand(num_inputs, input_dim)
    # lengthscales = np.random.rand(input_dim)
    # k = GPy.kern.RBF(input_dim, .5, lengthscales, ARD=True)
    # K = k.K(X)
    # Y = np.random.multivariate_normal(np.zeros(num_inputs), K, (output_dim,)).T

    # print Y

    # print Y.shape

    # m = GPy.models.BayesianGPLVM(Y, input_dim, kernel=k, num_inducing=num_inducing)

    # m.optimize('scg', messages=1)

    # m.plot()
    # plt.title('After optimisation')

    # plt.savefig('test.eps')

    pass
