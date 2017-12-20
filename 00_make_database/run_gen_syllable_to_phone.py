
import sys
import re

# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

def gen_phone_duration_in_syllable(filepath, outpath_file):

    pattern = re.compile(r"""(?P<start>.+)\s(?P<end>.+)\s.+\-(?P<curphone>.+)\+.+/A:.+\-(?P<cur_phone_index>.+)_.+\+.+/B:.+/D:.+\-(?P<phone_number>.+)\+.+/E:.+""",re.VERBOSE)
    # 87545000 108545472 n^-sil+X/A:3_10-x_x+x_x/B:0-x+x/C:4_29-x_x+x_x/D:3-x+x/E:18-x+x/F:10_4-x_x+x_x/G:x_29_18/H:2-x+x
    # 85143750 87545000 aa-n^+sil/A:2_9-3_10+x_x/B:0-0+x/C:3_28-4_29+x_x/D:3-3+x/E:17-18+x/F:2_1-10_4+x_x/G:x_29_18/H:45-2+x

    main_duration = []
    temp_dur = []

    for line in Utility.read_file_line_by_line(filepath):
        # print line
        match = re.match(pattern, line)
        if match:

            start = float(match.group('start'))
            end = float(match.group('end'))

            phone_index = match.group('cur_phone_index')
            phone_number = match.group('phone_number')

            # print phone_index, phone_number, start, end

            if phone_index == 'x':
                temp_dur = []
                temp_dur.append(end-start)
                main_duration.append(temp_dur)
            elif phone_index == '1':
                temp_dur = []
                temp_dur.append(end-start)
            elif phone_index == phone_number:
                temp_dur.append(end-start)
                main_duration.append(temp_dur)
            else:
                temp_dur.append(end-start)

    # print main_duration

    c = 0

    for m in main_duration:
        # print m
        c = c + len(m)

    if c != len(Utility.read_file_line_by_line(filepath)):
        print 'No equal', filepath

    Utility.save_obj(main_duration, outpath_file)

    pass

    #pattern = re.compile(r"""(?P<start>.+)\s(?P<end>.+)\s.+\-(?P<curphone>.+)\+.+/A:.+""",re.VERBOSE)
    # match = re.match(pattern, line)
    #if match:
    #    
    #    phone = match.group('curphone')

if __name__ == '__main__':

    # phone_label_path = '/Users/dechamoungsri/Desktop/speccom2_data/data/phone_full_time/tsc/sd/'

    phone_label_path = '/work/w2/decha/Data/GPR_speccom_data/full_time/tsc/sd/'

    output_path = '/work/w2/decha/Data/GPR_speccom_data/phones_in_syllable_duration_object/'

    start = 'a'
    stop = 'z'

    for sett in Utility.char_range(start, stop):

        set_path = '{}/{}/'.format(phone_label_path, sett)

        set_output_path = '{}/{}/'.format(output_path, sett)
        Utility.make_directory(set_output_path)

        if not Utility.is_dir_exists(set_path):

            print 'No set : ', sett
            continue

        for f in Utility.list_file(set_path):

            if f.startswith('.'): continue

            # print f

            phone_full_label_path = '{}/{}'.format(set_path, f)

            out_file_path = '{}/{}.dur'.format(set_output_path, Utility.get_basefilename(f))

            gen_phone_duration_in_syllable(phone_full_label_path, out_file_path)

    # print Utility.load_obj('/work/w2/decha/Data/GPR_speccom_data/phones_in_syllable_duration_object/a/tscsda01.dur')

    pass
