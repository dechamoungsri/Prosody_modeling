
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('../../GPy-devel/')
sys.path.append('../../paramz-master/')
sys.path.append('../../library/')

from tool_box.util.utility import Utility

from GPy_Interface.gpy_interface import GPy_Interface

import numpy as np
import matplotlib.pyplot as plt

def run_training(db_file, name_out_path, data_type, input_dim):

    db = Utility.load_obj(db_file)

    Y = []

    names = []

    for syl in db:
        feat = syl['TF'][data_type]['data']
        Y.append(feat)
        names.append(syl['id'])
        # sys.exit()

    Y = np.array(Y)

    print Y.shape
    # print Y[0]

    num_inducing = int(len(Y)*0.01)
    if num_inducing > 100: 
        num_inducing = 100
    elif num_inducing < 10: 
        num_inducing = 10

    config = {
        'input_dim' : input_dim,
        'data' : Y,
        'num_inducing' : num_inducing,
        'max_iters' : 500,
        'missing_data' : True,
        'optimize_algo' : 'scg'
    }

    print config

    m = GPy_Interface.Bayesian_GPLVM_Training(config)

    print m
    print '---------------------------'
    print m.X
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

    db_path = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/13_merge_vowel_08c/'

    # for input_dim in [2, 5]:
    # for input_dim in [20]:
    for input_dim in [15]:

        out_path = '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/14_merge_vowel_13_data/input_dim_{}/'.format(input_dim)

        data_type = 'intepolate151_normalize_by_preprocessing.normalize'

        print out_path

        for t in [0]:
            for f in ['nasal', 'no', 'non-nasal']:
                name = '{}_{}'.format(t, f)
                db_file = '{}/{}.npy'.format(db_path, name)

                name_out_path = '{}/{}/'.format(out_path, name)

                Utility.make_directory(name_out_path)

                if Utility.is_file_exist(db_file):
                    print name
                    try:
                        run_training(db_file, name_out_path, data_type, input_dim)
                    except Exception, e:
                        print 'Error in : {}'.format(name)
                        print e

    pass
