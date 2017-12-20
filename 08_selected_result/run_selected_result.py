
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':

    # obj = '/work/w23/decha/decha_w23/Second_Journal/Unsupervised_learning_result/01a_gplvm_rerun/4_no/n_cluster_2_n_neighbors_0.1x.pkl'

    # print Utility.load_obj(obj)

    db_path = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/13_merge_vowel_08c/'

    out_path = '/work/w23/decha/decha_w23/Second_Journal/Unsupervised_learning_result/00_result_conslusion/'

    link_path = '/work/w23/decha/decha_w23/Second_Journal/Unsupervised_learning_result/00_result_conslusion/'

    for t in xrange(5):
        for f in ['nasal', 'no', 'non-nasal']:
            for v in ['long', 'short']:
                name = '{}_{}_{}'.format(t, v, f)
                db_file = '{}/{}.npy'.format(db_path, name)

                name_out_path = '{}/{}/'.format(out_path, name)

                if Utility.is_file_exist(db_file):
                    draw_figure(db_file, name_out_path)

        # sys.exit()

    pass
