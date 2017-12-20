
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

    # XX = -1*np.log(kern.K(X, Y)) 
    XX = kern.K(X, Y)
    # print 'Shape', XX.shape

    print XX.min(), XX.max()

    # print XX

    return XX

def svm_classifier(train_data, train_label, test_data, test_label, output_figure, plane, xx, yy, most_dominants, inverse_lengthscale):

    # print inverse_lengthscale

    # fit the model
    clf = svm.SVC( kernel='rbf', verbose=True, class_weight={1: 10})
    # clf = svm.SVC( kernel='rbf', tol=1, verbose=True, gamma=inverse_lengthscale)
    clf.fit(train_data, train_label)

    print 'Label : ', set(train_label)

    test = clf.predict(train_data)
    print 'all data : ', len(train_data)
    print 'Test predict negative : ', test[test==-1].size
    print 'Test predict positive: ', test[test==1].size

    y_pred_test = clf.predict(test_data)

    # plt.clf()

    # plt.scatter(test_data[:, most_dominants[0]][y_pred_test==-1], test_data[:, most_dominants[1]][y_pred_test==-1], c='blue', label='Unlabel : Negative')
    # plt.scatter(test_data[:, most_dominants[0]][y_pred_test==1], test_data[:, most_dominants[1]][y_pred_test==1], c='red', label='Unlabel : Positive')
    # plt.scatter(train_data[:, most_dominants[0]][train_label==-1], train_data[:, most_dominants[1]][train_label==-1], c='white', label='Label : Negative')
    # plt.scatter(train_data[:, most_dominants[0]][train_label==1], train_data[:, most_dominants[1]][train_label==1], c='yellow', label='Label : Positive')
    # plt.legend()
    # plt.title('SVC')
    # plt.savefig(output_figure)

    return y_pred_test

    pass

def run_training(base_path, db_file, name_out_path, name):

    names_file = '{}/names.pkl'.format(base_path)
    out_data = '{}/x.pkl'.format(base_path)
    input_sensitivity = '{}/input_sensitivity.pkl'.format(base_path)

    names = Utility.load_obj(names_file)
    db = Utility.load_obj(db_file)

    name_list = []
    for d in db:
        name_list.append( d['id'] )

    label = []

    train_name_list = []

    train_idx = []

    true_label = []

    out = []

    for i, nn in enumerate(names) :
        idx = name_list.index(nn)
    
        out.append(db[idx]['TF']['intepolate151_normalize_by_preprocessing.normalize']['data'])
        # print db[idx]['TF']['intepolate151_normalize_by_preprocessing.normalize']['data']
        # sys.exit()

        if 'j' in nn:
            train_name_list.append(nn)
            train_idx.append(i)

        elif db[idx]['stress'] == '2':
            train_name_list.append(nn)
            train_idx.append(i)

        if db[idx]['stress'] == '1':
            # label.append(db[idx]['stress'])
            label.append(-1)
        elif nn in potential_list:
            # label.append('3')
            label.append(1)
        elif db[idx]['stress'] == '2':
            label.append(1)
        else :
            # label.append(db[idx]['stress'])
            label.append(-1)

        if db[idx]['stress'] == '2':
            true_label.append(1)
        else:
            true_label.append(int(db[idx]['stress']))

    # out = Utility.load_obj(out_data)
    out = np.array(out)
    print out.shape
    input_sent = Utility.load_obj(input_sensitivity)

    most_dominants = Utility.get_input_sensitivity(input_sent, 2)

    label = map(int, label)
    label = np.array(label)

    train = out[train_idx]
    train_lab = label[train_idx]

    print len(train), len(train_lab), set(train_lab)

    global kern
    lengthscale=1/np.array(input_sent, dtype=float)

    lengthscale = lengthscale/lengthscale.min()

    # print 'lengthscale : ', lengthscale
    # kern = GPy.kern.RBF(len(train[0]), ARD=True, lengthscale=lengthscale)
    # kern = GPy.kern.RBF(len(train[0]), ARD=True, lengthscale=lengthscale)

    min_max_dims = []
    ten_or_not = []

    for d in xrange(len(out[0])):
        out_d = out[:, d]
        m = []
        m.append(min(out_d))
        m.append(max(out_d))
        min_max_dims.append(m)

        if d in most_dominants:
            ten_or_not.append(100),
        else :
            ten_or_not.append(1)

    m = min_max_dims
    # for mm in m:
    #     print mm

    # print most_dominants

    m_grid = []
    for d in xrange(len(out[0])):
        if ten_or_not[d] != 1:
            m_grid.append( np.linspace(m[d][0], m[d][1], ten_or_not[d]) )
        else:
            m_grid.append([0])

    d0, d1, d2, d3, d4, d5, d6, d7, d8, d9 = np.meshgrid(
        m_grid[0], m_grid[1], m_grid[2], m_grid[3], m_grid[4], 
        m_grid[5], m_grid[6], m_grid[7], m_grid[8], m_grid[9]
        )

    plane = np.c_[
        d0.ravel(), d1.ravel(), d2.ravel(), d3.ravel(), d4.ravel(), 
        d5.ravel(), d6.ravel(), d7.ravel(), d8.ravel(), d9.ravel()
        ]

    # print plane

    y_pred_test = svm_classifier(train, train_lab, out, '', name_out_path, plane, np.linspace(m[most_dominants[0]][0], m[most_dominants[0]][1], ten_or_not[most_dominants[0]]), np.linspace(m[most_dominants[1]][0], m[most_dominants[1]][1], ten_or_not[most_dominants[1]]), most_dominants, input_sent)

    global syl_dict

    for n, y_pred, true_lab in zip(names, y_pred_test, true_label) :
        syllable = dict()

        if y_pred == 1:
            syllable['stress'] = 2
        else:
            syllable['stress'] = true_lab

        syl_dict[n] = syllable

    pass

syl_dict = dict()

if __name__ == '__main__':

    method_14_dim_10 = {
        'model_path' : '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/14_merge_vowel_13_data/input_dim_10/',
        'out_path' : './figure_gplvm_raw_data_class_weight/',
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

                    run_training(base_path, db_file, name_out_path, name)

                    # sys.exit()

    print len(syl_dict), count
    Utility.save_obj(syl_dict, './by_product_dict_3_level_raw_data_weight_svm.pkl')

    pass
