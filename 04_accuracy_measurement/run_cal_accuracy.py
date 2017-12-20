
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score

def load_real_label(db):

    real = []

    for syl in db:
        # print syl
        if syl['stress'] == '2':
            real.append(1)
        elif syl['stress'] in ['0' , '1']:
            real.append( int(syl['stress']) )
        else :
            print syl['stress']
            real.append( int(syl['stress']) )

    if not len(db) == len(real):
        print len(db), len(real)

    return real

def find_config(name):

    for line in config_setting:
        spl = Utility.trim(line).split(' ')
        
        if name == spl[0]:
            print spl
            n_cluster = spl[1]
            n_neighbor = spl[2]
            return (n_cluster, n_neighbor)

def call_accuracy(db_file, x_base_file, setting, name):

    db = Utility.load_obj(db_file)

    real = load_real_label(db)
    n_cluster, n_neighbor = find_config(name)

    unstress_list = setting[0]
    stress_list = setting[1]

    x_file = '{}/param_n_cluster_{}_n_neighbors_{}x.pkl'.format(x_base_file, n_cluster, n_neighbor)
    pred = Utility.load_obj(x_file)
    print pred.shape

    print set(pred), setting

    for un in unstress_list:
        pred[pred==un] = 555 # Unstress

    for st in stress_list:
        pred[pred==st] = 999 # Stress

    pred[pred==999] = 1
    pred[pred==555] = 0

    if name == '1_non-nasal':
        print set(pred)

    acc = accuracy_score(real, pred) 

    f1 = f1_score(real, pred, average=None) 

    print 'acc : ', acc
    print 'f1 : ', f1

    global acc_scores
    global f1_scores

    # spl = name.split('_')
    acc_scores[name] = acc
    f1_scores[name] = f1

    result_file = dict()
    result_file['pred'] = pred
    result_file['real'] = real
    result_file['acc'] = acc
    result_file['f1'] = f1
    result_file['name'] = name
    result_file['n_cluster'] = n_cluster
    result_file['n_neighbors'] = n_neighbor

    Utility.save_obj(result_file, '{}/result_file.pkl'.format(x_base_file))

    pass

def print_result(outfile):

    print_list_acc = []
    print_list_acc.append('\t{}\t{}\t{}'.format('nasal', 'no', 'non-nasal'))

    print_list_f1 = []
    print_list_f1.append('\t{}\t\t{}\t\t{}'.format('nasal', 'no', 'non-nasal'))
    print_list_f1.append('\t{}\t{}\t{}\t{}\t{}\t{}'.format('Unstress', 'Stress', 'Unstress', 'Stress','Unstress', 'Stress'))

    for t in xrange(5):

        acc = 'Tone_{}'.format(t)
        f1 = 'Tone_{}'.format(t)

        for f in ['nasal', 'no', 'non-nasal']:
            acc = acc + '\t' + '{}'.format(acc_scores['{}_{}'.format(t, f)])

            f1 = f1 + '\t' + '{}'.format(f1_scores['{}_{}'.format(t, f)][0]) + '\t' + '{}'.format(f1_scores['{}_{}'.format(t, f)][1])

        print_list_acc.append(acc)
        print_list_f1.append(f1)

    print print_list_acc
    acc_out = '{}/acc_result.txt'.format(outfile)
    Utility.write_to_file_line_by_line(acc_out, print_list_acc)

    print print_list_f1
    f1_out = '{}/f1_result.txt'.format(outfile)
    Utility.write_to_file_line_by_line(f1_out, print_list_f1)

f1_scores = dict()
acc_scores = dict()

if __name__ == '__main__':

    db_path = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/13_merge_vowel_08c'
    out_path = '/work/w23/decha/decha_w23/Second_Journal/Unsupervised_learning_result/15_Agglomerative_clustering/'
    x_path = '/work/w23/decha/decha_w23/Second_Journal/Unsupervised_learning_result/15_Agglomerative_clustering/'

    selected_result = '/work/w23/decha/decha_w23/Second_Journal/Unsupervised_learning_result/15_Agglomerative_clustering/gplvm_result.txt'
    config_setting = Utility.read_file_line_by_line(selected_result)

    result = {
        '0_nasal' : [[0,1],[2]],
        '0_no' : [[0,1],[2]],
        '0_non-nasal' : [[0],[1]],
        '1_nasal' : [[0,2,3,4],[1]],
        '1_no' : [[0,1,3,4],[2]],
        '1_non-nasal' : [[0],[1]],
        '2_nasal' : [[0,1,2,4],[3]],
        '2_no' : [[0],[1]],
        '2_non-nasal' : [[0,1],[2]],
        '3_nasal' : [[0,1,3],[2]],
        '3_no' : [[0],[1]],
        '3_non-nasal' : [[0],[1]],
        '4_nasal' : [[0,1],[2]],
        '4_no' : [[0,1],[2,3]],
        '4_non-nasal' : [[1],[0]]
    }

    for t in xrange(5):
        for f in ['nasal', 'no', 'non-nasal']:

            name = '{}_{}'.format(t, f)

            setting = result[name]

            db_file = '{}/{}.npy'.format(db_path, name)
            x_base_file = '{}/{}/'.format(x_path, name)

            if Utility.is_file_exist(db_file):
                call_accuracy(db_file, x_base_file, setting, name)
                # sys.exit()

    
    print_result(out_path)

    pass
