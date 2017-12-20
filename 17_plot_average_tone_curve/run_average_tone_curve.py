
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

def plot(db_file, name_outpath):

    feature = dict()
    feature[0] = [] # Unstress
    feature[1] = [] # Stress
    feature[2] = [] # Weak stress

    for syl in Utility.load_obj(db_file):
        # print syl['TF']['intepolate151']['data']
        # print syl['id']

        if syl['id'] in stres_labels:
            stress = stres_labels[syl['id']]['stress']
            feature[stress].append( syl['TF']['intepolate151']['data'][0:50] )

    ylim = [100,-100]

    for k in feature:

        feat = feature[k]

        m = np.mean(feat, axis=0)
        v = np.var(feat, axis=0)

        # print len(m)

        x = np.linspace(0, 100, num=50)

        plt.clf()
        plt.plot(x, m, 'k-')
        plt.fill_between(x, m-v, m+v)

        if plt.ylim()[0] < ylim[0]: ylim[0] = plt.ylim()[0]
        if plt.ylim()[1] > ylim[1]: ylim[1] = plt.ylim()[1]

    for k in feature:
        feat = feature[k]
        m = np.mean(feat, axis=0)
        v = np.var(feat, axis=0)
        x = np.linspace(0, 100, num=50)

        plt.clf()
        plt.plot(x, m, 'k-')
        plt.fill_between(x, m-v, m+v, alpha=0.5, color='red')
        plt.ylim(ylim)

        plt.savefig('{}/stress_type_{}.png'.format(name_outpath, k))

    pass

stres_labels = Utility.load_obj('/work/w23/decha/decha_w23/Second_Journal/Evaluation_result/stress_label_list/03a_dict_3_level_of_stress.pkl')

if __name__ == '__main__':

    db_path = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/13_merge_vowel_08c/'

    outpath = './figure_26_July/'

    for t in xrange(5):
        for f in ['nasal', 'no', 'non-nasal']:
            name = '{}_{}'.format(t, f)
            db_file = '{}/{}.npy'.format(db_path, name)

            name_outpath = '{}/{}/'.format(outpath, name)

            Utility.make_directory(name_outpath)

            if Utility.is_file_exist(db_file):
                print db_file
                plot(db_file, name_outpath)
                # sys.exit()

    pass
