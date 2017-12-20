
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

import re

def add_stress_to_full(full_file, out_file, out_full_no_time_file, name):

    # print name

    pattern = re.compile(r"""(?P<start>.+)\s(?P<end>.+)\s.+
        /A:.+\-(?P<cur_phone_position>.+)_.+\+.+
        /B:.+
        """,re.VERBOSE)

    syl_type = []
    for line in Utility.read_file_line_by_line(full_file):
        match = re.match(pattern, line)
        if match:
            cur_phone_position = match.group('cur_phone_position')
            # print cur_phone_position
            if (cur_phone_position == '1') | (cur_phone_position == 'x'):
                syl_type.append(cur_phone_position)

    count = 0
    o = []
    for line in Utility.read_file_line_by_line(full_file):
        match = re.match(pattern, line)
        if match:
            cur_phone_position = match.group('cur_phone_position')
            # print cur_phone_position
            if (cur_phone_position == '1') | (cur_phone_position == 'x'):
                count = count + 1
                # syl_id = '{}_{}'.format(name, count)
                # print syl_id

            pre_syl = '{}_{}'.format(name, count-1)
            cur_syl = '{}_{}'.format(name, count)
            suc_syl = '{}_{}'.format(name, count+1)

            if pre_syl not in db:
                if (count-1-1) < 0:
                    pre_stress = 'x'
                else :
                    if syl_type[count-1-1] == 'x':
                        pre_stress = 'x'
                    else:
                        pre_stress = 0
            else:
                pre_stress = db[pre_syl]['stress']

            if cur_syl not in db:
                if syl_type[count-1] == 'x':
                    cur_stress = 'x'
                else:
                    cur_stress = 0
            else :
                cur_stress = db[cur_syl]['stress']

            if suc_syl not in db:
                if (count-1+1) == len(syl_type):
                    suc_stress = 'x'
                else:
                    if syl_type[count-1+1] == 'x':
                        suc_stress = 'x'
                    else:
                        suc_stress = 0
            else:
                suc_stress = db[suc_syl]['stress']

            stress_context = '/I:{}-{}+{}'.format(pre_stress, cur_stress, suc_stress)
            # print stress_context

            context = '{}{}'.format(Utility.trim(line), stress_context)
            # print context

            o.append(context)

    o_no_time = get_remove_time(o)
    # print o_no_time

    if (not (len(Utility.read_file_line_by_line(full_file)) == len(o))) & (not (len(Utility.read_file_line_by_line(full_file)) == len(o_no_time))):
        print name

    Utility.write_to_file_line_by_line(out_file, o)
    Utility.write_to_file_line_by_line(out_full_no_time_file, o_no_time)

    pass

def get_remove_time(o):

    no_time = []

    for line in o:
        no_time.append(line.split(' ')[2])

    return no_time

db = Utility.load_obj('/work/w23/decha/decha_w23/Second_Journal/Evaluation_result/stress_label_list/02a_gplvm_result.pkl')

# print db

if __name__ == '__main__':

    full_path = '/work/w2/decha/Data/GPR_speccom_data/full_time/tsc/sd/'
    out_path = '/work/w2/decha/Data/GPR_speccom_data/speccom2_data/02_unsupervised_full_time_with_stress/tsc/sd/'
    out_full_path = '/work/w2/decha/Data/GPR_speccom_data/speccom2_data/02_unsupervised_full_with_stress/tsc/sd/'

    for s in Utility.char_range('a', 'z'):

        if s in ['k', 'n', 'q', 's']: continue

        print s

        full_set_path = '{}/{}/'.format(full_path, s)
        out_set_path = '{}/{}/'.format(out_path, s)
        out_set_full_path = '{}/{}/'.format(out_full_path, s)

        Utility.make_directory(out_set_path)
        Utility.make_directory(out_set_full_path)

        for f in Utility.list_file(full_set_path):

            if f.startswith('.'): continue

            base = Utility.get_basefilename(f)

            full_file = '{}/{}'.format(full_set_path, f)
            # print full_file

            out_file = '{}/{}'.format(out_set_path, f)
            # print out_file

            out_full_no_time_file = '{}/{}'.format(out_set_full_path, f)

            add_stress_to_full(full_file, out_file, out_full_no_time_file, base)

            # sys.exit()

    pass
