
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

def gen_new_file(file_path, out_file):
    print file_path

    count = 0

    out = []

    base = Utility.get_basefilename(file_path)
    print base

    for line in Utility.read_file_line_by_line(file_path):

        count = count + 1

        name = '{}_{}'.format(base, count)
        # print name
        # print db['tscsdj46_2']

        # sys.exit()

        stress = 0
        syl = 'x_x_x_x'
        if name in db:
            if name in multi_level_list:
                stress = multi_level_list[name]['stress']
            else : 
                stress = 0
            syl = '{}_{}_{}_{}'.format(db[name]['consonant'], db[name]['vowel'], db[name]['finalconsonant'], db[name]['tone'] )

        if stress == 2: print name

        spl = line.split(' ')
        o = '{} {} {}_{}_{}'.format(spl[0], spl[1], syl, count, stress )
        # print o
        out.append(o)

    Utility.write_to_file_line_by_line(out_file, out)

db = None

multi_level_list = Utility.load_obj('/work/w23/decha/decha_w23/Second_Journal/Evaluation_result/stress_label_list/dict_3_level_of_stress.pkl')

if __name__ == '__main__':

    db_path = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/02_add_stress_database_07_nov/dict_version.pkl'
    db = Utility.load_obj(db_path)

    # for d in db:
    #     print d, db[d]
    #     sys.exit()

    # set_path = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/syllable_time/j/'

    # outpath = './j_set_for_3_level_stress_label/'
    # Utility.make_directory(outpath)

    for f in Utility.list_file(set_path):
        if f.startswith('.'): continue

        file_path = '{}/{}'.format(set_path, f)

        out_file = '{}/{}'.format(outpath, f)

        gen_new_file(file_path, out_file)

    pass
