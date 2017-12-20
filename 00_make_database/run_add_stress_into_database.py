
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

def add_stress(db_file, stress_list_file, new_db_file):

    db = Utility.load_obj(db_file)

    stress_list = Utility.load_obj(stress_list_file)

    name_index = []
    for syl in stress_list:
        name = syl[1]
        # print name
        name_index.append(name)

    for syl in db:
        name = syl['id']
        index = name_index.index(name)
        # print stress_list[index][2]
        syl['stress'] = stress_list[index][2]

    # print db
    Utility.save_obj(db, new_db_file)

    pass

if __name__ == '__main__':

    db_path = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/01_database/'

    stress_list_path = '/work/w2/decha/Data/GPR_speccom_data/figure/plot_sort_list/02_check_stress_07_nov/'

    new_db_path = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/02_add_stress_database_07_nov/'

    Utility.make_directory(new_db_path)

    for t in xrange(5):
        for f in ['nasal', 'no', 'non-nasal']:
            for v in ['long', 'short']:
                name = '{}_{}_{}'.format(t, v, f)

                print name

                db_file = '{}/{}.npy'.format(db_path, name)

                new_db_file = '{}/{}.npy'.format(new_db_path, name)

                stress_list_file = '{}/{}.list'.format(stress_list_path, name)

                # name_out_path = '{}/{}/'.format(out_path, name)

                # Utility.make_directory(name_out_path)

                if Utility.is_file_exist(db_file):
                    # draw_figure(db_file, name_out_path)
                    add_stress(db_file, stress_list_file, new_db_file)
                    # sys.exit()

    pass
