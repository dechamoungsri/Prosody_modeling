
import sys

# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('../')

from tool_box.util.utility import Utility
from Syllable.Syllable_Object import Syllable

import matplotlib.pyplot as plt

def sort_db(db_name, outfile):
    db = Utility.load_obj(db_name)

    s_list = []

    for syl in db:
        print syl

        name = syl['id']
        dur = syl['dur']

        if len(dur) == 3:
            vowel_final_dur = dur[1] + dur[2]
        else:
            vowel_final_dur = dur[1] 

        vowel_final_dur = float(vowel_final_dur)

        stress = Syllable.find_stress_info(stress_path, name)

        # print stress

        s_list.append((vowel_final_dur, name, stress))

    Utility.sort_by_index(s_list, 0)

    # print s_list

    Utility.write_to_file_line_by_line(outfile, s_list)
    Utility.save_obj(s_list, outfile)

    # sys.exit()

    pass

stress_path = '/work/w2/decha/Data/GPR_speccom_data/stress label/'

if __name__ == '__main__':

    db_path = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/'

    out_path = '/work/w2/decha/Data/GPR_speccom_data/figure/plot_sort_list/'

    Utility.make_directory(out_path)

    for t in xrange(5):
        for f in ['nasal', 'no', 'non-nasal']:
            for v in ['long', 'short']:
                name = '{}_{}_{}'.format(t, v, f)
                db_file = '{}/{}.npy'.format(db_path, name)

                name_out_path = '{}/{}.list'.format(out_path, name)

                if Utility.is_file_exist(db_file):
                    print db_file
                    sort_db(db_file, name_out_path)
                    # sys.exit()

    pass
