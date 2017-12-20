
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

def load_name_and_label(name_file, label_file):

    global d

    names = Utility.load_obj(name_file)
    labels = Utility.load_obj(label_file)

    for n, lab in zip(names, labels):
        print n, lab
        d[n] = { 'stress': lab }

    pass

d = dict()

if __name__ == '__main__':

    name_path = '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/14_merge_vowel_13_data/input_dim_10/' 
    best_predicted_path = '/work/w23/decha/decha_w23/Second_Journal/Unsupervised_learning_result/01a_gplvm_rerun_dim10/'

    outpath = '/work/w23/decha/decha_w23/Second_Journal/Evaluation_result/gplvm_result.pkl'

    for t in xrange(5):
        for f in ['nasal', 'no', 'non-nasal']:
                name = '{}_{}'.format(t, f)

                name_file = '{}/{}/names.pkl'.format(name_path, name)
                label_file = '{}/{}/prediction_labels.pkl'.format(best_predicted_path, name)

                if Utility.is_file_exist(name_file):
                    load_name_and_label(name_file, label_file)

        # sys.exit()

    Utility.save_obj(d, outpath)


    pass
