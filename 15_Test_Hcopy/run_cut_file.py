
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

    lf0_inpath = '/work/w2/decha/Data/GPR_speccom_data/lf0/tsc/sd/'
    mcep_inpath = '/work/w2/decha/Data/GPR_speccom_data/mcep/tsc/sd/'
    bap_inpath = '/work/w2/decha/Data/GPR_speccom_data/bap/tsc/sd/'

    lf0_outpath = '/work/w2/decha/Data/GPR_speccom_data/lf0_remove_silence/tsc/sd/'
    mcep_outpath = '/work/w2/decha/Data/GPR_speccom_data/mcep_remove_silence/tsc/sd/'
    bap_outpath = '/work/w2/decha/Data/GPR_speccom_data/bap_remove_silence/tsc/sd/'

    Utility.make_directory(out_path)
    Utility.make_directory(lf0_outpath)
    Utility.make_directory(mcep_outpath)
    Utility.make_directory(bap_outpath)

    for s in Utility.char_range('a', 'z'):
        mono_set_path = '{}/{}/'.format(mono_label, s)
        mono_remove_silence_path = '{}/{}/'.format(mono_remove_label, s)

        cmp_outpath = '{}/{}/'.format(out_path, s)

        lf0_out_path = '{}/{}/'.format(lf0_outpath, s)
        mcep_out_path = '{}/{}/'.format(mcep_outpath, s)
        bap_out_path = '{}/{}/'.format(bap_outpath, s)

        # Utility.make_directory(cmp_outpath)

        Utility.make_directory(lf0_out_path)
        Utility.make_directory(mcep_out_path)
        Utility.make_directory(bap_out_path)

        print s

        for f in Utility.list_file(mono_set_path):
            if f.startswith('.'): continue

            base = Utility.get_basefilename(f)

            # print base

            mono = Utility.read_file_line_by_line('{}/{}.lab'.format(mono_set_path, base))
            mono_remove = Utility.read_file_line_by_line('{}/{}.lab'.format(mono_remove_silence_path, base))

            # cmp_file = '{}/{}/{}.cmp'.format(cmp_path, s, base)
            # out_cmp_file = '{}/{}/{}.cmp'.format(out_path, s, base)

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

            lf0_file = '{}/{}/{}.lf0'.format(lf0_inpath, s, base)
            lf0_out_file = '{}/{}/{}.lf0'.format(lf0_outpath, s, base)

            mcep_file = '{}/{}/{}.mcep'.format(mcep_inpath, s, base)
            mcep_out_file = '{}/{}/{}.mcep'.format(mcep_outpath, s, base)

            bap_file = '{}/{}/{}.bap'.format(bap_inpath, s, base)
            bap_out_file = '{}/{}/{}.bap'.format(bap_outpath, s, base)

            if (head_dur < 0) | (tail_dur < 0):
                print base
                # call(["HCopy", '{}'.format( cmp_file ), '{}'.format( out_cmp_file ) ])
                call(['cp', lf0_file, lf0_out_file])
                call(['cp', mcep_file, mcep_out_file])
                call(['cp', bap_file, bap_out_file])
                continue

            # print head_dur, tail_dur
            # print cmp_file
            # print out_cmp_file

            # call(["HCopy", "-s", '{}'.format( head_dur ), "-e", '-{}'.format( tail_dur ), '{}'.format( cmp_file ), '{}'.format( out_cmp_file ) ])

            h_cut = head_dur/50000
            t_cut = tail_dur/50000

            # print ['bcut', '-s', '{}'.format(h_cut), '-e', '{}'.format( (int(mono_tail[1])/50000) - t_cut), '-l', '40', '+f', mcep_file, ' > ', mcep_out_file] 

            f = open(mcep_out_file, "w")
            call( ['bcut', '-s', '{}'.format(h_cut), '-e', '{}'.format( (int(mono_tail[1])/50000) - t_cut), '-l', '40', '+f', mcep_file], stdout=f )

            f = open(bap_out_file, "w")
            call( ['bcut', '-s', '{}'.format(h_cut), '-e', '{}'.format( (int(mono_tail[1])/50000) - t_cut), '-l', '5', '+f', bap_file], stdout=f )

            f = open(lf0_out_file, "w")
            call( ['bcut', '-s', '{}'.format(h_cut), '-e', '{}'.format( (int(mono_tail[1])/50000) - t_cut), '-l', '1', '+f', lf0_file], stdout=f )

            all_frame = int(remove_tail[1])/50000

            o_mcep = check_output(
                "x2x +fa {}".format(mcep_out_file),
                stderr=subprocess.STDOUT,
                shell=True
                )

            if abs( len(o_mcep.split('\n'))/40 - all_frame ) > 5:
                print base, 'mcep is Error'
                print len(o_mcep.split('\n'))/40, all_frame

            o_bap = check_output(
                "x2x +fa {}".format(bap_out_file),
                stderr=subprocess.STDOUT,
                shell=True
                )

            if abs( len(o_bap.split('\n'))/5 - all_frame ) > 5:
                print base, 'bap is Error'
                print len(o_bap.split('\n'))/5, all_frame

            o_lf0 = check_output(
                "x2x +fa {}".format(lf0_out_file),
                stderr=subprocess.STDOUT,
                shell=True
                )

            if abs( len(o_lf0.split('\n')) - all_frame ) > 5:
                print base, 'lf0 is Error'
                print len(o_lf0.split('\n')), all_frame

            # sys.exit()

            # o = check_output(
            #     "HList -h {} | head -n 5".format(out_cmp_file),
            #     stderr=subprocess.STDOUT,
            #     shell=True
            #     )

            # # print 'Result : ', o

            # for line in o.split('\n'):
            #     match = re.match(pattern, line)
            #     if match:
            #         num_frame = match.group('num_frame')
            #         # print num_frame

            # remove_num_freme = float(remove_tail[1])/50000

            # diff = remove_num_freme-float(num_frame)
            # # print diff

            # if abs(diff) > 10:
            #     print 'May error : ', base
            #     print remove_num_freme, num_frame

            # sys.exit()

    pass
