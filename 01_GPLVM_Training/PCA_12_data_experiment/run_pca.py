
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('../../GPy-devel/')
sys.path.append('../../paramz-master/')
sys.path.append('../../library/')

from tool_box.util.utility import Utility

from GPy_Interface.gpy_interface import GPy_Interface

import numpy as np
import matplotlib.pyplot as plt

def run_training(db_file, name_out_path, n_components, data_type):

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

    method_13a = {
        'db_path' : '/work/w2/decha/Data/GPR_speccom_data/syllable_database/12a_standardization_of_11/',
        'out_path' : '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/13a_pca_standardization_of_12_data/',
        'data_type' : 'intepolate151_with_consonant_unvoice_ratio_standardization'
    }

    method_13b = {
        'db_path' : '/work/w2/decha/Data/GPR_speccom_data/syllable_database/12b_robustsacle_of_11/',
        'out_path' : '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/13b_pca_robust_scale_of_12_data/',
        'data_type' : 'intepolate151_with_consonant_unvoice_ratio_robust_scale'
    }

    method_13c = {
        'db_path' : '/work/w2/decha/Data/GPR_speccom_data/syllable_database/12c_normalize_of_11/',
        'out_path' : '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/13c_pca_normalization_by_preprocessing_of_12_data/',
        'data_type' : 'intepolate151_with_consonant_unvoice_ratio_normalize_by_preprocessing.normalize'
    }

    for method in [method_13a, method_13b, method_13c]:

        db_path = method['db_path']

        out_path = method['out_path']

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
                            run_training(db_file, name_out_path, n_components, method['data_type'])


    pass