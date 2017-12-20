
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('../GPy-devel/')
sys.path.append('../paramz-master/')
sys.path.append('../library/')

import GPy

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score

def run_data_processor(db_file):

    db = Utility.load_obj(db_file)

    real = []

    for syl in db:

        if syl['stress'] == '2':
            real.append(1)
        elif syl['stress'] in ['0' , '1']:
            real.append( int(syl['stress']) )
        else :
            print syl['stress']
            real.append( int(syl['stress']) )

    real = np.array(real)

    return real

    pass

def cal_result(real, pred):

    acc = accuracy_score(real, pred) 
    f1 = f1_score(real, pred, average=None) 

    return (acc, f1)

    pass

def get_prediction_result(base_method_path, db_file):

    pred = Utility.load_obj('{}/prediction_labels.pkl'.format(base_method_path))
    real = run_data_processor(db_file)

    acc, f1 = cal_result(real, pred)

    return (pred, real, acc, f1)

    pass

if __name__ == '__main__':

    # base_path = '/work/w23/decha/decha_w23/Second_Journal/Unsupervised_learning_result/00_raw_data_link_clustering_accuracy/'

    # base_path = '/work/w23/decha/decha_w23/Second_Journal/Unsupervised_learning_result/01_gplvm_link_clustering_accuracy/'

    # base_path = '/work/w23/decha/decha_w23/Second_Journal/Unsupervised_learning_result/02_pca_link_clustering_accuracy/'

    # base_path = '/work/w23/decha/decha_w23/Second_Journal/Unsupervised_learning_result/02a_pca_rerun/'

    base_path = '/work/w23/decha/decha_w23/Second_Journal/Unsupervised_learning_result/002a_pca/dim_2/'

    db_path = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/13_merge_vowel_08c/'

    acc_scores = dict()
    f1_scores = dict()

    all_p = np.array([]) 
    all_r = np.array([]) 

    for t in xrange(5):

        all_pred = np.array([]) 
        all_real = np.array([]) 

        for f in ['nasal', 'no', 'non-nasal']:
            name = '{}_{}'.format(t, f)
            print name
            base_method_path = '{}/{}/'.format(base_path, name)

            db_file = '{}/{}.npy'.format(db_path, name)

            if Utility.is_file_exist(db_file):
                pred, real, acc, f1 = get_prediction_result(base_method_path, db_file)
                acc_scores[name] = acc
                f1_scores[name] = f1
                print f1
                all_pred = np.append(all_pred, pred)
                all_real = np.append(all_real, real)

        acc, f1 = cal_result(all_real, all_pred)

        all_p = np.append(all_p, all_pred)
        all_r = np.append(all_r, all_real)

        acc_scores['{}_all'.format(t)] = acc
        f1_scores['{}_all'.format(t)] = f1
        print f1

    all_acc, all_f1 = cal_result(all_r, all_p)

    all_result = []
    all_result.append('{}'.format(all_acc))
    all_result.append('{}\t{}'.format(all_f1[0], all_f1[1]))

    a_log = []
    f_log = []
    for t in xrange(5):
        a_out = ''
        f_out = ''
        for f in ['nasal', 'no', 'non-nasal', 'all']:
            name = '{}_{}'.format(t, f)
            a = acc_scores[name]
            f = f1_scores[name]

            a_out = a_out + '{}'.format(a) + '\t'
            f_out = f_out + '{}'.format(f[0]) + '\t' + '{}'.format(f[1]) + '\t'

        a_log.append(a_out)
        f_log.append(f_out)

    Utility.write_to_file_line_by_line('{}/accuracy_score.txt'.format(base_path), a_log)
    Utility.write_to_file_line_by_line('{}/f1_score.txt'.format(base_path), f_log)

    Utility.write_to_file_line_by_line('{}/all_score.txt'.format(base_path), all_result)

    pass
