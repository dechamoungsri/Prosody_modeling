
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

import traceback

def build_db(db_file):

    global db

    d = Utility.load_obj(db_file)
    db = db + d

    # print len(db)

    pass

def run_gen_easy_access(dict_outpath):

    global db_dict

    for d in db:
        db_dict[d['id']] = d
        print d['id']

    Utility.save_obj(db_dict, dict_outpath)

    pass

def add_stress(yaml, count, name):

    for unit in yaml:
        # print '------------------------------'
        # print unit
        if (unit['unit'] == 'phone'):
            if ( (unit['entity'] == 'pau') | (unit['entity'] == 'sil') ):
                count[0] = count[0] + 1
        else :
            if unit['unit'] == 'syllable':
                count[0] = count[0] + 1
                # print db_dict['{}_{}'.format(name, count[0])]
                if '{}_{}'.format(name, count[0]) in db_dict:
                    unit['stress'] = int(db_dict['{}_{}'.format(name, count[0])]['stress'])
                else :
                    print 'No {} in db_dict'.format('{}_{}'.format(name, count[0]))
                    unit['stress'] = 0
                    global coun_no
                    coun_no = coun_no + 1
                # print unit
            else:
                add_stress(unit['inners'], count, name)

    pass

db = []

db_dict = dict()

coun_no = 0

if __name__ == '__main__':

    dict_path = '/work/w23/decha/decha_w23/Second_Journal/Evaluation_result/gplvm_result.pkl'
    db_dict = Utility.load_obj(dict_path)

    stress_path = '/work/w2/decha/Data/GPR_speccom_data/stress_label/'
    utt_base_path = '/work/w2/decha/Data/GPR_speccom_data/utt/tsc/sd/'
    syllable_full_path = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/full_time/tsc/sd/'

    out_path = '/work/w2/decha/Data/GPR_speccom_data/speccom2_data/utt_with_unsupervised_stress/tsc/sd/'
    # print db_dict['tscsdv01_29']

    for ch in Utility.char_range('a', 'z'):

        set_stress_path = '{}/{} lab/'.format(stress_path, ch)

        set_utt_base_path = '{}/{}/'.format(utt_base_path, ch)

        set_syllable_full_path = '{}/{}/'.format(syllable_full_path, ch)

        set_out_path = '{}/{}/'.format(out_path, ch)

        Utility.make_directory(set_out_path)

        if Utility.is_dir_exists(set_stress_path) & Utility.is_dir_exists(set_utt_base_path):
            print ch

            for i in xrange(1, 51):

                name = 'tscsd{}{}'.format(ch, Utility.fill_zero(i, 2))

                yaml_filename = '{}/{}.utt.yaml'.format(set_utt_base_path, name )
                if not Utility.is_file_exist(yaml_filename):
                    continue

                # print yaml_filename

                full_file = '{}/{}.lab'.format(set_syllable_full_path, name)

                count = [0]
                yaml = Utility.yaml_load(yaml_filename)
                add_stress(yaml, count, name)

                if not (len(Utility.read_file_line_by_line(full_file)) == count[0] ):
                    print 'Not equal'
                    print name, len(Utility.read_file_line_by_line(full_file)), count[0]

                # print yaml

                out_file = '{}/{}.utt.yaml'.format(set_out_path, name)
                Utility.yaml_save(out_file, yaml)

                # print yaml
                # print count
                # sys.exit()

    print 'all no {} names '.format(coun_no)

    # yaml_file = '/work/w2/decha/Data/GPR_speccom_data/utt/tsc/sd/a/tscsda01.utt.yaml'
    # yaml = Utility.yaml_load(yaml_file)

    # count = [0]
    # find_syllable_list(yaml, count)

    # print 'Count : ', count

    pass
