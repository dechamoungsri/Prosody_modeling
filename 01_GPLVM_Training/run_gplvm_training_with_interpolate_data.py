
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('../GPy-devel/')
sys.path.append('../paramz-master/')
sys.path.append('../library/')

from tool_box.util.utility import Utility

from GPy_Interface.gpy_interface import GPy_Interface

import numpy as np
import matplotlib.pyplot as plt

import GPy
import paramz

from GPy.models.bayesian_gplvm import BayesianGPLVM
from GPy.core.sparse_gp_mpi import SparseGP_MPI

def run_training(db_file, name_out_path):

    db = Utility.load_obj(db_file)

    Y = []

    names = []

    for syl in db:
        feat = syl['TF']['intepolate151']['data']
        Y.append(feat)
        names.append(syl['id'])
        # sys.exit()

    Y = np.array(Y)

    print Y.shape
    # print Y[0]

    config = {
        'input_dim' : 10,
        'data' : Y,
        'num_inducing' : int(len(Y)*0.1),
        'max_iters' : 300,
        'missing_data' : True,
        'optimize_algo' : 'scg'
    }

    print config

    m = GPy_Interface.Bayesian_GPLVM_Training(config)

    print m
    print '---------------------------'
    print m.X
    print '---------------------------'
    print np.array(m.X.mean)
    print '---------------------------'
    print m.input_sensitivity()
    print '---------------------------'

    Utility.save_obj(m, '{}/model.pkl'.format(name_out_path))
    Utility.save_obj( np.array(m.X.mean), '{}/x.pkl'.format(name_out_path))

    Utility.save_obj(m.input_sensitivity(), '{}/input_sensitivity.pkl'.format(name_out_path))

    Utility.save_obj(names, '{}/names.pkl'.format(name_out_path))
    Utility.save_obj(Y, '{}/training_data.pkl'.format(name_out_path))

    pass

if __name__ == '__main__':

    db_path = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/04_data_with_intepolate_for_training/'

    out_path = '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/02_Bayesian_GPLVM_with_interpolate_data/input_dim_10/'

    print out_path

    for t in xrange(5):
        for f in ['nasal', 'no', 'non-nasal']:
            for v in ['long', 'short']:
                name = '{}_{}_{}'.format(t, v, f)
                db_file = '{}/{}.npy'.format(db_path, name)

                name_out_path = '{}/{}/'.format(out_path, name)

                Utility.make_directory(name_out_path)

                if Utility.is_file_exist(db_file):
                    run_training(db_file, name_out_path)
                    # m = '{}/model.pkl'.format(name_out_path)
                    # print Utility.load_obj(m)

    # t = '4'
    # v = 'long'
    # f = 'no' 

    # name = '{}_{}_{}'.format(t, v, f)
    # db_file = '{}/{}.npy'.format(db_path, name)

    # name_out_path = '{}/{}/'.format(out_path, name)

    # Utility.make_directory(name_out_path)

    # if Utility.is_file_exist(db_file):
    #     run_training(db_file, name_out_path)
        # sys.exit()

        # print Utility.load_obj('{}/x.pkl'.format(name_out_path))

    pass
