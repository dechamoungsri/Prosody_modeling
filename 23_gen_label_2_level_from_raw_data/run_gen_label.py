
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

def gen_label(db_file, predicted_path):

    predict_file = '{}/prediction_labels.pkl'.format(predicted_path)

    db = Utility.load_obj(db_file)
    predict_list = Utility.load_obj(predict_file)

    # print predict_list

    # for p in set(predict_list):
    #     print p, len(predict_list[predict_list==p])

    for s, p in zip(db, predict_list) :
        print s['id']
        syllable = dict()
        syllable['stress'] = p

        syl_dict[s['id']] = syllable

    pass

syl_dict = dict()

if __name__ == '__main__':

    db_path = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/13_merge_vowel_08c/'
    predicted_label = '/work/w23/decha/decha_w23/Second_Journal/Unsupervised_learning_result/00_raw_data_link_clustering_accuracy/'

    count = 0

    for t in xrange(5):
        for f in ['nasal', 'no', 'non-nasal']:
            name = '{}_{}'.format(t, f)
            db_file = '{}/{}.npy'.format(db_path, name)
            count = count + len(Utility.load_obj(db_file))
            predicted_path = '{}/{}/'.format(predicted_label, name)

            if Utility.is_file_exist(db_file):
                gen_label(db_file, predicted_path)
                # sys.exit()


        # sys.exit()
    print len(syl_dict), count
    Utility.save_obj(syl_dict, './by_product_dict_2_level_raw_data.pkl')

    pass
