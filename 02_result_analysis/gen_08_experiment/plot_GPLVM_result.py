
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

import matplotlib

sys.path.append('../../GPy-devel/')
sys.path.append('../../paramz-master/')
sys.path.append('../../library/')

import GPy

def plot_latent_space(base_path, db_file, name_out_path):

    names_file = '{}/names.pkl'.format(base_path)
    out_data = '{}/x.pkl'.format(base_path)
    input_sensitivity = '{}/input_sensitivity.pkl'.format(base_path)

    if not Utility.is_file_exist(out_data) : 
        print out_data
        print 'Not exist'
        return

    names = Utility.load_obj(names_file)

    db = Utility.load_obj(db_file)

    name_list = []
    for d in db:
        name_list.append( d['id'] )

    label = []
    for nn in names:
        idx = name_list.index(nn)
        label.append(db[idx]['stress'])

    out = Utility.load_obj(out_data)

    print out.shape

    input_sent = Utility.load_obj(input_sensitivity)
    print input_sent
    most_dominants = Utility.get_input_sensitivity(input_sent, 2)

    x = out[ :, most_dominants[0] ]
    y = out[ :, most_dominants[1] ]

    label = map(int, label)
    label = np.array(label)

    print set(label)

    colors = ['red','green','blue','purple']

    plt.clf()
    plt.scatter(x, y, c=label, cmap=matplotlib.colors.ListedColormap(colors))
    plt.savefig( name_out_path )

if __name__ == '__main__':

    # method_08a = {
    #     'model_path' : '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/08a_standardization_data/input_dim_10/',
    #     'out_path' : '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/08a_standardization_data/figure_dim_10/',
    #     'db_path' : '/work/w2/decha/Data/GPR_speccom_data/syllable_database/08a_standardization_of_04/'
    # }

    # method_08b = {
    #     'model_path' : '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/08b_robustscale_data/input_dim_10/',
    #     'out_path' : '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/08b_robustscale_data/figure_dim_10/',
    #     'db_path' : '/work/w2/decha/Data/GPR_speccom_data/syllable_database/08b_robustsacle_of_04/'
    # }

    # method_08c = {
    #     'model_path' : '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/08c_preprocessing_normaiize/input_dim_10/',
    #     'out_path' : '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/08c_preprocessing_normaiize/figure_dim_10/',
    #     'db_path' : '/work/w2/decha/Data/GPR_speccom_data/syllable_database/08c_normalize_of_04/'
    # }

    # method_10a = {
    #     'model_path' : '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/10a_standardization_of_03_data/input_dim_10/',
    #     'out_path' : '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/10a_standardization_of_03_data/figure_dim_10/',
    #     'db_path' : '/work/w2/decha/Data/GPR_speccom_data/syllable_database/10a_standardization_of_03/'
    # }

    # method_10b = {
    #     'model_path' : '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/10b_robust_scale_of_03_data/input_dim_10/',
    #     'out_path' : '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/10b_robust_scale_of_03_data/figure_dim_10/',
    #     'db_path' : '/work/w2/decha/Data/GPR_speccom_data/syllable_database/10b_robustsacle_of_03/'
    # }

    # method_10c = {
    #     'model_path' : '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/10c_normalization_by_preprocessing_of_03_data/input_dim_10/',
    #     'out_path' : '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/10c_normalization_by_preprocessing_of_03_data/figure_dim_10/',
    #     'db_path' : '/work/w2/decha/Data/GPR_speccom_data/syllable_database/10c_normalize_of_03/'
    # }

    method_12a = {
        'model_path' : '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/12a_standardization_of_11_data/input_dim_10/',
        'out_path' : '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/12a_standardization_of_11_data/figure_dim_10/',
        'db_path' : '/work/w2/decha/Data/GPR_speccom_data/syllable_database/12a_standardization_of_11/'
    }

    method_12b = {
        'model_path' : '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/12b_robust_scale_of_11_data/input_dim_10/',
        'out_path' : '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/12b_robust_scale_of_11_data/figure_dim_10/',
        'db_path' : '/work/w2/decha/Data/GPR_speccom_data/syllable_database/12b_robustsacle_of_11/'
    }

    method_12c = {
        'model_path' : '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/12c_normalization_by_preprocessing_of_11_data/input_dim_10/',
        'out_path' : '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/12c_normalization_by_preprocessing_of_11_data/figure_dim_10/',
        'db_path' : '/work/w2/decha/Data/GPR_speccom_data/syllable_database/12c_normalize_of_11/'
    }

    for method in [ method_12a, method_12b, method_12c ]:

        model_path = method['model_path']

        out_path = method['out_path']
        Utility.make_directory(out_path)

        db_path = method['db_path']

        for t in xrange(5):
            for f in ['nasal', 'no', 'non-nasal']:
                for v in ['long', 'short']:
                    name = '{}_{}_{}'.format(t, v, f)
                    db_file = '{}/{}.npy'.format(db_path, name)

                    name_out_path = '{}/{}.eps'.format(out_path, name)

                    base_path = '{}/{}/'.format(model_path, name)

                    if Utility.is_file_exist(db_file):
                        print name
                        plot_latent_space(base_path, db_file, name_out_path)

        # sys.exit()


    pass
