
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':

    db_dict = dict()

    lab_path = '/work/w23/decha/decha_w23/Second_Journal/sync_google_drive/Second_journal_Code/12_plot_j_set/j_set_for_3_level_stress_label/'

    for f in Utility.list_file(lab_path):
        if 'wav' in f: continue
        if f.startswith('.'): continue

        print f

        count = 0
        for line in Utility.read_file_line_by_line('{}/{}'.format(lab_path, f)):

            count = count + 1
            name = '{}_{}'.format( Utility.get_basefilename(f) , count)

            spl = line.split(' ')

            stress = Utility.trim(spl[2].split('_')[5])

            # print name, stress

            if stress not in ['0', '1', '2']:
                print name, 'Error'
                sys.exit()

            syl = dict()
            syl['stress'] = stress

            db_dict[name] = syl

    print len(db_dict)
    Utility.save_obj(db_dict, './stress_dict_for_j_set_with_manual_3_level_stress_labeling.pkl')

    pass
