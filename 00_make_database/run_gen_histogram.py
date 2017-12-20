
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

def draw_his(db_file, name_out_path):

    db = Utility.load_obj(db_file)

    syl_list = []
    for s in db:
        syl_list.append(s[0])
        # print s

    hist = np.histogram(syl_list, bins=100)
    print hist

    plt.clf()

    print len(hist[1]/50000), len(hist[0])

    lab = (hist[1]/50000)[0:100]

    plt.bar(lab, hist[0])
    plt.savefig(name_out_path)


if __name__ == '__main__':

    db_path = '/work/w2/decha/Data/GPR_speccom_data/figure/plot_sort_list/'
    out_path = '/work/w2/decha/Data/GPR_speccom_data/figure/histogram/'

    Utility.make_directory(out_path)

    for t in xrange(5):
        for f in ['nasal', 'no', 'non-nasal']:
            for v in ['long', 'short']:
                name = '{}_{}_{}'.format(t, v, f)
                db_file = '{}/{}.list'.format(db_path, name)

                name_out_path = '{}/{}.eps'.format(out_path, name)

                if Utility.is_file_exist(db_file):
                    draw_his(db_file, name_out_path)

                    # sys.exit()

    pass
