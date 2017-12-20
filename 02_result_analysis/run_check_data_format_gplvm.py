
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

import matplotlib

sys.path.append('../GPy-devel/')
sys.path.append('../paramz-master/')
sys.path.append('../library/')

import GPy

if __name__ == '__main__':

    n = '2_long_no'

    f = 'input_dim_10/{}'.format(n)

    # pca_output_file = '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/03_pca_with_interpolate_data/{}/pca_reduction_output.pkl'.format(f)

    model = '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/02_Bayesian_GPLVM_with_interpolate_data/{}/model.pkl'.format(f)

    names_file = '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/02_Bayesian_GPLVM_with_interpolate_data/{}/names.pkl'.format(f)

    names = Utility.load_obj(names_file)
    m = Utility.load_obj(model)

    db = Utility.load_obj('/work/w2/decha/Data/GPR_speccom_data/syllable_database/04_data_with_intepolate_for_training/{}.npy'.format(n))

    out = 

    name_list = []
    for d in db:
        name_list.append( d['id'] )

    label = []
    for nn in names:
        idx = name_list.index(nn)
        label.append(db[idx]['stress'])

    # out = m.X.mean

    print m

    # print out.shape

    x = out[:,0]
    y = out[:,1]

    label = map(int, label)
    label = np.array(label)

    print set(label)

    colors = ['red','green','blue','purple']

    plt.scatter(x, y, c=label, cmap=matplotlib.colors.ListedColormap(colors))
    plt.savefig( './{}_pca.eps'.format(n) )

    pass
