
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

def get_j_set(db_file, out_file, sort_list_out_file):

    j_set_db = []
    j_set_sort_list = []

    db = Utility.load_obj(db_file)
    for syl in db:
        if 'j' in syl['id']:
            j_set_db.append(syl)
            # print syl['dur']
            dur = 0
            for idx, d in enumerate(syl['dur']) :
                if idx == 0: continue

                dur = dur + d

            j_set_sort_list.append( (syl['id'], d, syl['stress']) )

    Utility.sort_by_index(j_set_sort_list, 1)
    print j_set_sort_list

    Utility.save_obj(j_set_sort_list, sort_list_out_file)
    Utility.save_obj(j_set_db, out_file)

    pass

if __name__ == '__main__':

    db_path = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/13_merge_vowel_08c/'

    out_path = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/14_j_set_database/'

    Utility.make_directory(out_path)

    for t in xrange(5):
        for f in ['nasal', 'no', 'non-nasal']:
            name = '{}_{}'.format(t, f)
            db_file = '{}/{}.npy'.format(db_path, name)
            out_file = '{}/{}.npy'.format(out_path, name)
            sort_list_out_file = '{}/{}_sorted_list.npy'.format(out_path, name)

            if Utility.is_file_exist(db_file):
                get_j_set(db_file, out_file, sort_list_out_file)

                # sys.exit()

    pass
