
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

import re

def get_last_syllable(filepath, name):

    # sil-sil+sil/A:X-X+X/S:l-x+z^/B:x-x+3/C:x_x-x_x+1_1/D:x-x+2/E:x-x+1/F:x_x-x_x+2_1/G:x_35_23/H:x-x+45

    global out

    pattern = re.compile(r"""(?P<start>.+)\s(?P<end>.+)\s.+\-(?P<curphone>.+)\+.+/A:.+/C:.+\-(?P<cur_position_syl>.+)_.+\+.+/D:.+/F:.+\-.+_(?P<cur_num_syl>.+)\+.+/G:.+""",re.VERBOSE)

    count = 0

    for line in Utility.read_file_line_by_line(filepath):

        count = count + 1

        match = re.match(pattern, line)
        if match:
           cur_position_syl = match.group('cur_position_syl')
           cur_num_syl = match.group('cur_num_syl')

           iden = '{}_{}'.format(name, count)
           # print iden

           if cur_position_syl == 'x': continue

           if ( cur_position_syl == cur_num_syl ) & ( ( cur_num_syl != '1' ) ):
                # print iden
                out.append(iden)

    pass

out = []

if __name__ == '__main__':

    label_path = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/full_time/tsc/sd/'

    for sett in ['j']:
        label_set_path = '{}/{}/'.format(label_path, sett)

        for f in Utility.list_file(label_set_path):
            if f.startswith('.'): continue

            filepath = '{}/{}'.format(label_set_path, f)
            get_last_syllable(filepath, Utility.get_basefilename(f))

            # sys.exit()

    Utility.save_obj(out, './potential_list.pkl')

    pass
