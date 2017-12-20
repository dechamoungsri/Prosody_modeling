
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

import matplotlib.mlab as mlab
from tool_box.util.utility import Utility
import scipy.stats as stats

import numpy as np
import matplotlib.pyplot as plt

def plot(y, durs, n, name_out_path):
    plt.clf()

    y = np.array(y)
    y[y<0] = np.nan
    y = np.exp(y)

    plt.plot( xrange(len(y)) ,y)

    data_size = len(y)

    dur_length = sum(durs)

    outfile = '{}/{}.eps'.format(name_out_path, n)

    c = 0

    for idx, d in enumerate( durs ):
        if idx >= len(durs)-1: continue

        x = d/dur_length*data_size

        c = c + x

        if np.nanmax(y) < 417.991041301:
            plt.ylim(100, 417.991041301)

        plt.xlim(0, len(y))

        ylim = plt.ylim()
        # print ylim

        # print x

        plt.plot([c, c], [ylim[0], ylim[1]], 'k-', color='r')

    plt.savefig(outfile)

def draw_figure(db_name, name_out_path):
    db = Utility.load_obj(db_name)

    for syl in db:
        # print syl

        lf0 = syl['raw_lf0']
        durs = syl['dur']
        n = syl['id']

        plot(lf0, durs, n, name_out_path)

        # sys.exit(0)

def find_max_y(db_all):

    max_y = 0

    for syl in Utility.load_obj(db_all):

        if len(syl['raw_lf0']) == 0: continue

        if max( np.exp( syl['raw_lf0'] ) ) > 425:
            # print max( np.exp( syl['raw_lf0'] ) )
            continue

        if max( np.exp( syl['raw_lf0'] ) ) > max_y:
            max_y = max( np.exp( syl['raw_lf0'] ) )

    print 'max y = ', max_y

    pass

def find_min_y(db_all):

    max_y = 600

    for syl in Utility.load_obj(db_all):

        if len(syl['raw_lf0']) == 0: continue

        r = syl['raw_lf0']
        r = np.array(r)
        r[r<0] = np.nan

        # print r

        # sys.exit()

        if min( np.exp( r ) ) < 150:
            # print min( np.exp( r ) )
            continue

        if min( np.exp( r ) ) < max_y:
            max_y = min( np.exp( r ) )

    print 'min y = ', max_y

    pass

if __name__ == '__main__':

    db_all = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/all_syllable.npy'
    # m = find_max_y(db_all)
    # mi = find_min_y(db_all)

    db_path = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/'

    out_path = '/work/w2/decha/Data/GPR_speccom_data/figure/lf0_plot_by_vowel_finalconsonant/'

    for t in xrange(5):
        # t = 2
        for f in ['nasal', 'no', 'non-nasal']:
            for v in ['long', 'short']:
                name = '{}_{}_{}'.format(t, v, f)
                db_file = '{}/{}.npy'.format(db_path, name)

                name_out_path = '{}/{}/'.format(out_path, name)

                Utility.make_directory(name_out_path)

                if Utility.is_file_exist(db_file):
                    draw_figure(db_file, name_out_path)

        # sys.exit()

    pass
