
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

import matplotlib
import matplotlib.mlab as mlab

import sklearn
from sklearn import mixture
from scipy.stats import multivariate_normal
from scipy.spatial import distance

import scipy as sp
import scipy.stats
import scipy.stats as stats

# import GPy

print('The scikit-learn version is {}.'.format(sklearn.__version__))

sys.path.append('../GPy-devel/')
sys.path.append('../paramz-master/')
sys.path.append('../library/')

import GPy

from sklearn import svm

def mean_confidence_interval(data, confidence=0.99):
    a = 1.0*np.array(data)
    n = len(a)
    m, se = np.mean(a, axis=0), scipy.stats.sem(a, axis=0)
    # print 'm', m
    h = se * sp.stats.t._ppf((1+confidence)/2., n-1)
    return m, m-h, m+h, h

def make_ellipses(gmm):
    for n, color in enumerate('g'):
        # print n
        v, w = np.linalg.eigh(gmm._get_covars()[n][:2, :2])
        u = w[0] / np.linalg.norm(w[0])
        angle = np.arctan2(u[1], u[0])
        angle = 180 * angle / np.pi  # convert to degrees
        v *= 9
        ell = mpl.patches.Ellipse(gmm.means_[n, :2], v[0], v[1],
                                  180 + angle, color=color)
        ell.set_clip_box(plt.gca().bbox)
        ell.set_alpha(0.5)
        plt.gca().add_artist(ell)

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
        
        if db[idx]['stress'] == '1':
            label.append(db[idx]['stress'])
        elif nn in potential_list:
            label.append('3')
        else :
            label.append(db[idx]['stress'])


    out = Utility.load_obj(out_data)

    # print out.shape

    input_sent = Utility.load_obj(input_sensitivity)
    # print 'input_sensitivity : ', sorted(input_sent)
    most_dominants = Utility.get_input_sensitivity(input_sent, 2)

    x = out[ :, most_dominants[0] ]
    y = out[ :, most_dominants[1] ]

    label = map(int, label)
    label = np.array(label)

    # print set(label)

    train = np.append( out[label==2] , out[label==3], axis=0 )
    # train = out[label==2] 
    # print train.shape

    test = out[label==0]

    lengthscale=1/np.array(input_sent, dtype=float)
    k = GPy.kern.RBF(len(train[0]), ARD=True, lengthscale=lengthscale)

    plt.clf()

    colors = ['red','green','blue','purple']

    md = most_dominants[0]

    mean = np.mean(train, axis=0)
    var = np.var(train, axis=0)
    # rv = multivariate_normal(mean=np.mean(train, axis=0), cov=np.var(train, axis=0))

    sd = np.std(train[:,most_dominants[0]], axis=0)

    for idx, lab in enumerate(label): 
        # if lab == 2: continue
        # if lab == 3: continue

        # print out[idx][md], mean

        d = distance.euclidean(out[idx][md], mean[md])
        # print d

        if d < sd:
            # label[idx] = 4
            label[idx] = 2
        elif d < 2*sd:
            # label[idx] = 6
            label[idx] = 2
            pass

    label[label==3] = 2
    print len(out), len(names)
    print set(label), len(label)

    if len(set(label)) > 3:
        print 'error : ', name_out_path
        raise

    global syl_dict

    for n, lab in zip(names, label) :
        syllable = dict()
        syllable['stress'] = lab
        syl_dict[n] = syllable

    # print names
    # print label

    # return

    for idx, s in enumerate( [0,1,4,5,6,2,3] ):
        # if (s == 3) | (s == 2):
        if (s == 2):
            # plt.scatter(x[label==s], y[label==s], c=colors[s], label=s, s=100)
            plt.scatter(x[label==s], y[label==s], c=colors[s], label='Manual weak stress labeling', s=100)
            pass
        elif (s==-1):
            plt.scatter(x[label==s], y[label==s], c='red', label=s, s=20)
        elif (s==1):
            plt.scatter(x[label==s], y[label==s], c='red', label='Stress', s=7)
            pass
        elif (s==5):
            # plt.scatter(x[label==s], y[label==s], c='yellow', label=s, s=20, marker='^', linewidth='0')
            pass
        elif (s==4):
            plt.scatter(x[label==s], y[label==s], c='green', label='Weak stress in 1 SD', s=20, marker='*', linewidth='0')
        elif (s==6):
            plt.scatter(x[label==s], y[label==s], c='orange', label='Weak stress in 2 SD', s=20, marker='h', linewidth='0')
        # else:
        elif (s==0):
            plt.scatter(x[label==s], y[label==s], c='black', label='Unstress', s=7, marker='.', linewidth='0')
            pass

    plt.scatter(mean[most_dominants[0]], mean[most_dominants[1]], c='red', label=s, s=200, marker='x')

    x_lim = plt.xlim()
    y_lim = plt.ylim()

    xx, yy = np.mgrid[x_lim[0]:x_lim[1]:.01, y_lim[0]:y_lim[1]:.01]
    pos = np.empty(xx.shape + (2,))
    pos[:, :, 0] = xx; pos[:, :, 1] = yy

    x_train = train[ :, most_dominants[0] ]
    y_train = train[ :, most_dominants[1] ]

    # rv = multivariate_normal(
    #     [mean[most_dominants[0]], mean[most_dominants[1]] ], 
    #     [var[most_dominants[0]], var[most_dominants[1]] ])
    # print rv
    # print 'means : ', rv.pdf([np.mean(x_train), np.mean(y_train)])

    # plt.contourf(xx, yy, rv.pdf(pos), alpha=0.5)

    # plt.legend(prop={'size':12})
    plt.savefig( name_out_path )

potential_list = None

syl_dict = dict()

if __name__ == '__main__':

    method_14_dim_10 = {
        'model_path' : '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/14_merge_vowel_13_data/input_dim_10/',
        'out_path' : './figure_gplvm/',
        'db_path' : '/work/w2/decha/Data/GPR_speccom_data/syllable_database/13_merge_vowel_08c/'
    }

    potential_list = Utility.load_obj('/work/w23/decha/decha_w23/Second_Journal/sync_google_drive/Second_journal_Code/13_get_last_syl_of_mul_noun/potential_list_second.pkl')
    # potential_list = Utility.load_obj('/work/w23/decha/decha_w23/Second_Journal/sync_google_drive/Second_journal_Code/13_get_last_syl_of_mul_noun/potential_list.pkl')

    print 'Potent list', len(potential_list)
    print potential_list[0]

    count = 0

    sys.exit()

    for method in [ method_14_dim_10 ]:

        model_path = method['model_path']

        out_path = method['out_path']
        Utility.make_directory(out_path)

        db_path = method['db_path']
        
        for t in xrange(5):
            for f in ['nasal', 'no', 'non-nasal']:
                name = '{}_{}'.format(t, f)
                db_file = '{}/{}.npy'.format(db_path, name)

                count = count + len(Utility.load_obj(db_file))

                name_out_path = '{}/{}.pdf'.format(out_path, name)

                base_path = '{}/{}/'.format(model_path, name)

                if Utility.is_file_exist(db_file):
                    print name
                    plot_latent_space(base_path, db_file, name_out_path)

                    # sys.exit()

    print len(syl_dict), count
    Utility.save_obj(syl_dict, './by_product_dict_3_level_of_stress.pkl')

    pass
