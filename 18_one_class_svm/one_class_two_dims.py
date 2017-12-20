
import sys
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('../GPy-devel/')
sys.path.append('../paramz-master/')
sys.path.append('../library/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

from sklearn import svm

from sklearn import preprocessing

import GPy

kern = None

def rbf_kernel(X, Y):

    XX = -1*np.log(kern.K(X, Y))
    # print 'Shape', XX.shape

    # p = XX.reshape(1, XX.shape[0]*XX.shape[1])
    # print max(p), min(p)

    return XX

def svm_classifier(train_data, train_label, test_data, test_label, output_figure, plane, xx, yy):

    # fit the model
    clf = svm.OneClassSVM( kernel=rbf_kernel, nu=0.3, tol=1.0 )
    clf.fit(train_data)

    y_pred_train = clf.predict(train_data)
    n_error_train = y_pred_train[y_pred_train == -1].size
    print 'Predict', y_pred_train, y_pred_train.size, n_error_train

    print plane.shape, xx.shape

    Z = clf.decision_function(plane)
    Z = Z.reshape(xx.shape)

    print Z.max(), Z.min()

    plt.contour(xx, yy, Z, levels=[0], linewidths=2, colors='darkred')
    plt.scatter(train_data[:, 0], train_data[:, 1], c='white')
    plt.savefig('./test.pdf')
    pass

def run_training(base_path, db_file, name_out_path):

    names_file = '{}/names.pkl'.format(base_path)
    out_data = '{}/x.pkl'.format(base_path)
    input_sensitivity = '{}/input_sensitivity.pkl'.format(base_path)

    names = Utility.load_obj(names_file)
    db = Utility.load_obj(db_file)

    name_list = []
    for d in db:
        name_list.append( d['id'] )

    label = []
    for nn in names:
        idx = name_list.index(nn)
        
        if nn in potential_list:
            label.append('3')
        elif db[idx]['stress'] == '1':
            label.append(db[idx]['stress'])
        else :
            label.append(db[idx]['stress'])

    out = Utility.load_obj(out_data)
    input_sent = Utility.load_obj(input_sensitivity)

    print 'Input sensitivity', input_sent

    most_dominants = Utility.get_input_sensitivity(input_sent, 2)

    label = map(int, label)
    label = np.array(label)

    train = np.append( out[label==2] , out[label==3], axis=0 )

    train = np.c_[
        train[:,most_dominants[0]], train[:,most_dominants[1]]
        ]

    print train.shape

    global kern
    lengthscale=1/np.array(input_sent, dtype=float)
    kern = GPy.kern.RBF(len(train[0]), ARD=True, lengthscale=[lengthscale[most_dominants[0]], lengthscale[most_dominants[1]]])

    print most_dominants

    xx, yy = np.meshgrid(np.linspace(-5, 5, 500), np.linspace(-5, 5, 500))
    plane = np.c_[xx.ravel(), yy.ravel()]
    svm_classifier(train, '', '', '', '', plane, xx, yy )

    pass

if __name__ == '__main__':

    method_14_dim_10 = {
        'model_path' : '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/14_merge_vowel_13_data/input_dim_10/',
        'out_path' : './figure_gplvm/',
        'db_path' : '/work/w2/decha/Data/GPR_speccom_data/syllable_database/13_merge_vowel_08c/'
    }

    potential_list = Utility.load_obj('/work/w23/decha/decha_w23/Second_Journal/sync_google_drive/Second_journal_Code/13_get_last_syl_of_mul_noun/potential_list_second.pkl')

    print 'Potent list', len(potential_list)

    count = 0

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
                    # plot_latent_space(base_path, db_file, name_out_path)

                    X = 0.3 * np.random.randn(100, 2)
                    X_train = np.r_[X + 2, X - 2]

                    X = 0.3 * np.random.randn(20, 2)
                    X_test = np.r_[X + 2, X - 2]

                    X_outliers = np.random.uniform(low=-4, high=4, size=(20, 2))

                    run_training(base_path, db_file, name_out_path)

                    sys.exit()

    pass
