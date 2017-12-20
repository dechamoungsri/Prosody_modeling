
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':

    base = '/work/w23/decha/decha_w23/Second_Journal/Speech_synthesis_system/00_conventional/testrun/sample_scripts/run_th_config_450_dur.sh'

    out_path = '/work/w23/decha/decha_w23/Second_Journal/Speech_synthesis_system/00_conventional/testrun/sample_scripts/'

    for n in [250, 650, 850]:
        r = Utility.read_file_line_by_line(base)
        out = []
        for line in r:
            l = Utility.trim(line)
            if 'set num = ' in line:
                o = 'set num = {}'.format(n) 
                out.append(o)
            else:
                out.append(l)

        Utility.write_to_file_line_by_line('{}/run_th_config_{}_dur.sh'.format(out_path, n), out)

    pass
