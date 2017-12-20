
import sys

# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

import matplotlib.mlab as mlab
from tool_box.util.utility import Utility
import scipy.stats as stats

import numpy as np
import matplotlib.pyplot as plt

def recursion(unit, stress_list):

    for u in unit:
        # print u
        if (u['unit'] == 'phone'):
            if ( (u['entity'] == 'sil') | (u['entity'] == 'pau') ):
                stress_list.append('x')
        elif (u['unit'] == 'syllable'):
            stress_list.append(u['stress'])
        else:
            if 'inners' in u:
                recursion(u['inners'], stress_list)

    pass

def run_gen_mono(utt_set):

    set_path = '{}/{}/'.format(utterance_path, utt_set)

    set_syllable_base_path = '{}/{}/'.format(syllable_base, utt_set)

    out_set_path = '{}/{}/'.format(output_path, utt_set)
    Utility.make_directory(out_set_path)

    for i in xrange(1, 51):
        utt_file = Utility.yaml_load('{}/tscsd{}{}.utt.yaml'.format(set_path, utt_set, Utility.fill_zero(i, 2) ))
        # print utt_file

        out_file = '{}/tscsd{}{}.lab'.format(out_set_path, utt_set, Utility.fill_zero(i, 2) )

        stress_list = []
        recursion(utt_file, stress_list)

        syllable_time_label = Utility.read_file_line_by_line( '{}/tscsd{}{}.lab'.format(set_syllable_base_path, utt_set, Utility.fill_zero(i, 2) ) )
        # print stress_list, len(stress_list)
        # print len(syllable_time_label)
        if len(syllable_time_label) != len(stress_list):
            print utt_set, i
            # print 'Error'
            # sys.exit()

        out = []
        for idx, line in enumerate(syllable_time_label):
            # print line, stress_list[idx]
            o = '{}::{}'.format( Utility.trim(line).replace('-', '_').replace('+', '_') , stress_list[idx])
            # print o
            out.append(o)

        Utility.write_to_file_line_by_line(out_file, out)

        # sys.exit()

    pass

if __name__ == '__main__':

    utterance_path = '/work/w2/decha/Data/GPR_speccom_data/speccom2_data/utt_with_3_level_svm_class_weight/tsc/sd/'

    syllable_base = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/syllable_time/'

    output_path = '/home/h1/decha/Dropbox/SPECOM_2017/syllable_stress_for_manual_labeling/'

    sett = ['a', 'b']

    for s in sett:
        run_gen_mono(s)

    pass
