
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

from subprocess import call
from subprocess import check_output

import subprocess

import re

if __name__ == '__main__':

    pattern = re.compile(r""".+Samples:\s+(?P<num_frame>\d+)\s+File.+""",re.VERBOSE)


    mono_label = '/work/w2/decha/Data/GPR_speccom_data/mono/tsc/sd/'
    mono_remove_label = '/work/w2/decha/Data/GPR_speccom_data/mono_remove_silence/tsc/sd/'

    cmp_path = '/work/w2/decha/Data/GPR_speccom_data/cmp/tsc/sd/'
    out_path = '/work/w2/decha/Data/GPR_speccom_data/cmp_remove_silence/tsc/sd/'

    Utility.make_directory(out_path)

    for s in Utility.char_range('v', 'z'):
        mono_set_path = '{}/{}/'.format(mono_label, s)
        mono_remove_silence_path = '{}/{}/'.format(mono_remove_label, s)

        cmp_outpath = '{}/{}/'.format(out_path, s)
        Utility.make_directory(cmp_outpath)

        print s

        for f in Utility.list_file(mono_set_path):
            if f.startswith('.'): continue

            base = Utility.get_basefilename(f)

            mono = Utility.read_file_line_by_line('{}/{}.lab'.format(mono_set_path, base))
            mono_remove = Utility.read_file_line_by_line('{}/{}.lab'.format(mono_remove_silence_path, base))

            cmp_file = '{}/{}/{}.cmp'.format(cmp_path, s, base)
            out_cmp_file = '{}/{}/{}.cmp'.format(out_path, s, base)

            mono_head = mono[0].split(' ')
            mono_tail = mono[len(mono)-1].split(' ')

            mono_head_dur = int(mono_head[1]) - int(mono_head[0])
            mono_tail_dur = int(mono_tail[1]) - int(mono_tail[0])

            remove_head = mono_remove[0].split(' ')
            remove_tail = mono_remove[len(mono_remove)-1].split(' ')

            remove_head_dur = int(remove_head[1]) - int(remove_head[0])
            remove_tail_dur = int(remove_tail[1]) - int(remove_tail[0])

            head_dur = mono_head_dur - remove_head_dur
            tail_dur = mono_tail_dur - remove_tail_dur

            o = check_output(
                "HList -h {} | head -n 5".format(cmp_file),
                stderr=subprocess.STDOUT,
                shell=True
                )

            for line in o.split('\n'):
                match = re.match(pattern, line)
                if match:
                    num_frame = match.group('num_frame')

            mono_tail_freme = float(mono_tail[1])/50000

            diff = mono_tail_freme-float(num_frame)

            # print base
            # print diff, mono_tail_freme, num_frame

            if abs(diff) > 10:
                print 'May error : ', base
                print mono_tail_freme, num_frame

            # sys.exit()

    pass
