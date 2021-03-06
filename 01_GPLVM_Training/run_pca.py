
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('../GPy-devel/')
sys.path.append('../paramz-master/')
sys.path.append('../library/')

from tool_box.util.utility import Utility

from GPy_Interface.gpy_interface import GPy_Interface

import numpy as np
import matplotlib.pyplot as plt

def run_training(db_file, name_out_path, n_components):

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
        'n_components' : n_components,
        'data' : Y
    }

    print config

    m, Y_r = GPy_Interface.pca(config)

    # print Y_r.shape

    Utility.save_obj(m, '{}/model.pkl'.format(name_out_path))
    Utility.save_obj(Y_r, '{}/pca_reduction_output.pkl'.format(name_out_path))

    Utility.save_obj(names, '{}/names.pkl'.format(name_out_path))
    Utility.save_obj(Y, '{}/training_data.pkl'.format(name_out_path))

    pass

if __name__ == '__main__':

    db_path = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/04_data_with_intepolate_for_training/'

    out_path = '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/03_pca_with_interpolate_data/'

    print out_path

    for n_components in [2, 5, 10]:
        for t in xrange(5):
            for f in ['nasal', 'no', 'non-nasal']:
                for v in ['long', 'short']:
                    name = '{}_{}_{}'.format(t, v, f)
                    db_file = '{}/{}.npy'.format(db_path, name)

                    name_out_path = '{}/input_dim_{}/{}/'.format(out_path, n_components, name)

                    Utility.make_directory(name_out_path)

                    if Utility.is_file_exist(db_file):
                        run_training(db_file, name_out_path, n_components)

    # t = '4'
    # v = 'long'
    # f = 'no' 

    # name = '{}_{}_{}'.format(t, v, f)
    # db_file = '{}/{}.npy'.format(db_path, name)

    # name_out_path = '{}/{}/'.format(out_path, name)

    # Utility.make_directory(name_out_path)

    # if Utility.is_file_exist(db_file):
    #     run_training(db_file, name_out_path)
    #     sys.exit()

    pass
