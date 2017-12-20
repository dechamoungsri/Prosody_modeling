
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

import re

if __name__ == '__main__':

    target_paths = [
        '/work/w23/decha/decha_w23/Second_Journal/Speech_synthesis_system/Experiment_A/05_3_level_svm_class_weight/testrun/sample_scripts/',
        '/work/w22/decha/decha_w22/speccom2/Speech_synthesis/06_3_level_svm_se_kernel/testrun/sample_scripts/',
        '/work/w12/decha/decha_w12/speccom2/speech_synthesis/07_3_level_raw_data_svm/testrun/sample_scripts/'
    ]

    data_size = [50, 250, 450, 650, 850]

    feats = ['lf0', 'dur']

    for p in target_paths:
        print p
        for f in feats:
            for data in data_size:
                the_file = '{}/log{}/log.tsc.{}'.format(p, data, f)
                pattern = re.compile(r""".+RMSE:\s(?P<rmse>.+)\sin.+""",re.VERBOSE)

                for line in Utility.read_file_line_by_line(the_file):
                    if 'RMSE' in line:
                        # print line
                        match = re.match(pattern, line)
                        if match:
                            rmse = match.group('rmse')
                            print '{} data size {} : '.format(f, data) , rmse

    pass
