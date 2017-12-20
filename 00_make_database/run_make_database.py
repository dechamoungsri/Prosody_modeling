
import sys

# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

def plot(cur_lf0, o):

    print o

    cur_lf0[cur_lf0<0] = np.nan

    Utility.plot_graph( np.exp(cur_lf0), o)

    pass

def plot_syllable(lab_path, lf0_path, out_set_path, name, plot_set_out):

    lines = Utility.read_file_line_by_line(lab_path)
    lf0 = Utility.read_lf0_into_ascii(lf0_path)

    print lf0

    path = '{}/{}/'.format(out_set_path, name)

    Utility.make_directory(path)

    for idx, line in enumerate(lines):

        line = Utility.trim(line)
        spl = line.split(' ')
        # print spl

        start = float(spl[0])/50000
        end = float(spl[1])/50000

        syl = spl[2]

        # print start, end, syl

        if end > len(lf0):
            end = len(lf0)-1

        cur_lf0 = lf0[start:end]
        # print len(cur_lf0)

        o = '{}_{}'.format((idx+1), syl)

        out_name = '{}/{}.lf0'.format(path, o )
        print out_name
        # Utility.write_to_file_line_by_line(out_name, cur_lf0)

        Utility.make_directory('{}/{}/'.format(plot_set_out, name))

        plot_out_file_path = '{}/{}/{}.eps'.format(plot_set_out, name, o)

        plot(cur_lf0, plot_out_file_path)

    print len(lf0)

    pass

if __name__ == '__main__':

    stress_data_path = '/work/w2/decha/Data/GPR_speccom_data/stress label'
    lf0_path = '/work/w2/decha/Data/GPR_speccom_data/lf0/tsc/sd/'

    out_path = '/work/w2/decha/Data/GPR_speccom_data/lf0_in_syllable/'

    plot_out_path = '/work/w2/decha/Data/GPR_speccom_data/f0_in_syllable_plot/'

    start = 'k'
    stop = 'z'

    Utility.make_directory(plot_out_path)

    for sett in Utility.char_range(start, stop):
        print sett

        set_path = '{}/{} lab/'.format(stress_data_path, sett)

        if not Utility.is_dir_exists(set_path):
            print 'Inexist : {}'.format(set_path)
            continue

        lf0_set_path = '{}/{}/'.format(lf0_path, sett)

        out_set_path = '{}/{}/'.format(out_path, sett)

        plot_set_out = '{}/{}/'.format(plot_out_path, sett)
        Utility.make_directory(plot_set_out)

        for f in Utility.list_file(set_path):

            if f.startswith('.'):
                continue

            file_path = '{}/{}'.format(set_path, f)
            # print file_path

            base = Utility.get_basefilename(file_path)

            print f, base

            lf0_file_path = '{}/{}.lf0'.format(lf0_set_path, base)

            # print plot_set_out

            plot_syllable(file_path, lf0_file_path, out_set_path, base, plot_set_out)

            # sys.exit()

    pass
