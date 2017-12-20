
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

import matplotlib
from matplotlib.patches import Ellipse

sys.path.append('../../GPy-devel/')
sys.path.append('../../paramz-master/')
sys.path.append('../../library/')

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
    iden = []

    target_id = []

    for nn in names:
        idx = name_list.index(nn)
        label.append(db[idx]['stress'])
        iden.append(nn)
        if nn in ['tscsdm38_55', 'tscsdu01_32', 'tscsdg02_21']:
            target_id.append(idx)

    target_id = np.array(target_id)

    out = Utility.load_obj(out_data)

    iden = np.array(iden)

    print out.shape

    input_sent = Utility.load_obj(input_sensitivity)
    print input_sent
    most_dominants = Utility.get_input_sensitivity(input_sent, 2)

    x = out[ :, most_dominants[0] ]
    y = out[ :, most_dominants[1] ]

    label = map(int, label)
    label = np.array(label)

    print set(label)

    # ind = np.random.choice(len(label), 20)
    # x = x[ind]
    # y = y[ind]
    # label = label[ind]
    # iden = iden[ind]

    colors = ['red','green','blue','purple']

    plt.clf()
    plt.scatter(x, y, c=label, cmap=matplotlib.colors.ListedColormap(colors), alpha=0.5)

    el = Ellipse((2, -1), 0.5, 0.5)

    for lab, xx, yy, yyy in zip(['Unstress',  'Strong stress', 'Weak stress'], x[target_id], y[target_id], [50, 100, 50]):
    # for lab, xx, yy in zip(iden, x, y):
        # yyy = 20
        plt.annotate(
            lab, 
            xy = (xx, yy), xytext = (0, yyy),
            textcoords = 'offset points', ha = 'left', va = 'bottom',
            bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
            arrowprops = dict(arrowstyle="simple",
                                fc="0.6", ec="none",
                                patchB=el,
                                connectionstyle="arc3,rad=0.3",
                                color='g'))
    plt.savefig( name_out_path )

if __name__ == '__main__':

    method_14 = {
        'model_path' : '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/14_merge_vowel_13_data/input_dim_10/',
        'out_path' : '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/14_merge_vowel_13_data/',
        'db_path' : '/work/w2/decha/Data/GPR_speccom_data/syllable_database/13_merge_vowel_08c/'
    }

    for method in [ method_14 ]:

        model_path = method['model_path']

        out_path = method['out_path']
        Utility.make_directory(out_path)

        db_path = method['db_path']

        name = '2_non-nasal'
        db_file = '{}/{}.npy'.format(db_path, name)

        name_out_path = '{}/{}_samples.eps'.format(out_path, name)

        base_path = '{}/{}/'.format(model_path, name)

        if Utility.is_file_exist(db_file):
            print name
            plot_latent_space(base_path, db_file, name_out_path)

        # sys.exit()


    pass
