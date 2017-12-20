
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

import matplotlib

def plot_figure(base_path, db_filepath, figure_out_filepath):

    pca_output_file = '{}/pca_reduction_output.pkl'.format(base_path)

    names_file = '{}/names.pkl'.format(base_path)

    names = Utility.load_obj(names_file)
    out = Utility.load_obj(pca_output_file)

    db = Utility.load_obj(db_filepath)

    name_list = []
    for d in db:
        name_list.append( d['id'] )

    label = []
    for nn in names:
        idx = name_list.index(nn)
        label.append(db[idx]['stress'])

    print out.shape

    x = out[:,0]
    y = out[:,1]

    label = map(int, label)
    label = np.array(label)

    print set(label)

    colors = ['red','green','blue','purple']

    plt.clf()
    plt.scatter(x, y, c=label, cmap=matplotlib.colors.ListedColormap(colors))
    plt.savefig( figure_out_filepath )

    pass

if __name__ == '__main__':

    # method_13a = {
    #     'model_path' : '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/13a_pca_standardization_of_12_data/',
    #     'out_path' : '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/13a_pca_standardization_of_12_data/',
    #     'db_path' : '/work/w2/decha/Data/GPR_speccom_data/syllable_database/12a_standardization_of_11/'
    # }

    # method_13b = {
    #     'model_path' : '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/13b_pca_robust_scale_of_12_data/',
    #     'out_path' : '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/13b_pca_robust_scale_of_12_data/',
    #     'db_path' : '/work/w2/decha/Data/GPR_speccom_data/syllable_database/12b_robustsacle_of_11/'
    # }

    # method_13c = {
    #     'model_path' : '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/13c_pca_normalization_by_preprocessing_of_12_data/',
    #     'out_path' : '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/13c_pca_normalization_by_preprocessing_of_12_data/',
    #     'db_path' : '/work/w2/decha/Data/GPR_speccom_data/syllable_database/12c_normalize_of_11/'
    # }

    method_09a = {
        'model_path' : '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/09a_standardization/',
        'out_path' : '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/09a_standardization/',
        'db_path' : '/work/w2/decha/Data/GPR_speccom_data/syllable_database/08a_standardization_of_04/'
    }

    method_09b = {
        'model_path' : '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/09b_robustscale/',
        'out_path' : '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/09b_robustscale/',
        'db_path' : '/work/w2/decha/Data/GPR_speccom_data/syllable_database/08b_robustsacle_of_04/'
    }

    method_09c = {
        'model_path' : '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/09c_preprocessing_normalize/',
        'out_path' : '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/09c_preprocessing_normalize/',
        'db_path' : '/work/w2/decha/Data/GPR_speccom_data/syllable_database/08c_normalize_of_04/'
    }

    for method in [ method_09a, method_09b, method_09c ]:

        model_path = method['model_path']

        out_path = method['out_path']
        Utility.make_directory(out_path)

        db_path = method['db_path']

        for dim in [2, 5, 10]:

            out_dim_path = '{}/figure_dim_{}/'.format(out_path, dim)

            Utility.make_directory(out_dim_path)

            for t in xrange(5):
                for f in ['nasal', 'no', 'non-nasal']:
                    for v in ['long', 'short']:
                        name = '{}_{}_{}'.format(t, v, f)
                        db_file = '{}/{}.npy'.format(db_path, name)

                        model_dim_path = '{}/input_dim_{}/{}/'.format(model_path, dim, name)

                        name_out_path = '{}/{}.eps'.format(out_dim_path, name)

                        if Utility.is_file_exist(db_file):
                            print name
                            plot_figure(model_dim_path, db_file, name_out_path)

    pass
