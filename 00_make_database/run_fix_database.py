
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

def change_stress(change_list, less_than):

    global db 

    out_list = []

    for syl in db:
        
        if syl[1] in change_list:
            st = '1'
            if syl[2] == '1':
                st = '0'
            else:
                st = '1'

            # if (not syl[2] in ['0', '1']) :
            #     print syl , 'Wired'

            new_syl = (syl[0], syl[1], st)

            # print syl
            # print new_syl
            out_list.append(new_syl)

        elif (float(syl[0])/50000) < float(less_than):
            # if syl[2] == '1':
            #     print syl
            out_list.append((syl[0], syl[1], '0'))
        else:
            out_list.append(syl)
            pass

    if not (len(out_list) == len(db)):
        print 'Not equal'

    return out_list

    pass

def fix_database(db_file, change_list_file, out_file):

    global db 
    db = None
    db = Utility.load_obj(db_file)

    change_list = []

    less_than = None

    for line in Utility.read_file_line_by_line(change_list_file):
        if 'tsc' in line:
            n = Utility.trim(line).replace(' ', '_')
            change_list.append(n)
        elif '<' in line:
            # print line
            less_than = line.split(' ')[1]
            pass

    # print change_list
    # print less_than

    if (len(change_list) == 0) | (less_than == None):
        raise 'Change list file false'

    new_list = change_stress(change_list, less_than)

    Utility.save_obj(new_list, out_file)

    pass

db = None

if __name__ == '__main__':

    db_path = '/work/w2/decha/Data/GPR_speccom_data/figure/plot_sort_list/01_non_fix/'

    change_list_path = '/work/w23/decha/decha_w23/Second_Journal/sync_google_drive/Second_journal_Code/change_list/'

    out_path = '/work/w2/decha/Data/GPR_speccom_data/figure/plot_sort_list/02_check_stress_07_nov/'

    Utility.make_directory(out_path)

    for t in xrange(5):
        for f in ['nasal', 'no', 'non-nasal']:
            for v in ['long', 'short']:
                name = '{}_{}_{}'.format(t, v, f)
                db_file = '{}/{}.list'.format(db_path, name)

                change_list_file = '{}/{}.txt'.format(change_list_path, name)

                name_out_path = '{}/{}.list'.format(out_path, name)

                if Utility.is_file_exist(db_file):

                    print name

                    fix_database(db_file, change_list_file, name_out_path)

                    # sys.exit()

    pass
