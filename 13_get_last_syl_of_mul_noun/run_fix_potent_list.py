
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

db = Utility.load_obj('/work/w2/decha/Data/GPR_speccom_data/syllable_database/02_add_stress_database_07_nov/dict_version.pkl')

def get_syllable_type(syl):
    tone = syl['tone']
    final = None
    if syl['finalconsonant'] in ['n^', 'm^', 'ng^']:
        final = 'nasal'
    elif syl['finalconsonant'] in ['z^']:
        final = 'no'
    else:
        final = 'non-nasal'

    return '{}_{}'.format(tone, final)

def get_vowel_dur(syl):

    d = 0.0

    durs = syl['dur']
    for i in xrange(1, len(durs)):
        d = d + durs[i]

    return d/50000.0

if __name__ == '__main__':

    potent_list = Utility.load_obj('/work/w23/decha/decha_w23/Second_Journal/sync_google_drive/Second_journal_Code/13_get_last_syl_of_mul_noun/potential_list.pkl')

    restrict_list = {
        '0_nasal': 30, 
        '1_non-nasal': 40, 
        '1_no': 25,
        '2_nasal': 25, 
        '2_non-nasal': 30, 
        '4_nasal': 30,
        '3_no': 25,
        '3_non-nasal': 30,
        '4_no': 25,
        '4_non-nasal': 25
        }

    print 'src : ', len(potent_list)

    remove_list = []

    for p in potent_list:
        syl = db[p]
        syl_type = get_syllable_type(syl)

        # if p in ['tscsdj17_11', 'tscsdj42_18', 'tscsdj10_26', 'tscsdj47_20', 'tscsdj07_12', 'tscsdj21_19', 'tscsdj09_21', 'tscsdj45_33', 'tscsdj38_20', 'tscsdj03_12', 'tscsdj43_17']:
        #     print p
        #     # potent_list.remove(p)
        #     remove_list.append(p)
        #     continue

        if syl_type in restrict_list:
            less = restrict_list[syl_type]
            dur = get_vowel_dur(syl)

            if syl_type == '4_no':
                print p, dur
                # potent_list.remove(p)
                # continue

            if syl['id'] == 'tscsdj07_47':
                # print syl
                print dur

            if dur < less:
                # print dur, p
                # potent_list.remove(p)
                remove_list.append(p)

    potent_list = [fruit for fruit in potent_list if fruit not in remove_list]
    print 'After : ', len(potent_list)

    Utility.save_obj(potent_list, './potential_list_second.pkl')

        # sys.exit()

    pass
