
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('../Syllable/')

from tool_box.util.utility import Utility

from Syllable_Object import Syllable

import numpy as np
import matplotlib.pyplot as plt

def gen_data(db_file, name_out_path):

    out = []

    debug = False

    for syl in Utility.load_obj(db_file) :

        # debug = False
        # if syl['id'] == 'tscsdj08_19':
        #     debug = True

        y = Syllable.get_normalize_gradient_interpolation(syl['raw_lf0'], 50, syl['dur'], debug=debug)
        # print y, len(y)

        if y is None:
            print syl['id']
            # print syl['raw_lf0']
            # sys.exit()
            continue

        syl['TF'] = dict()

        inte_data = dict()
        inte_data['data'] = y
        inte_data['description'] = 'Raw lf0 (first 50 + delta + delta-delta) + duration in frame unit (the last one). Unvoice frames are interpolated by 3-rd polynomial '

        syl['TF']['intepolate151'] = inte_data

        # print syl 

        out.append(syl)

        # sys.exit(0)

    Utility.save_obj(out, name_out_path)

    pass

if __name__ == '__main__':

    db_path = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/03_data_with_missing_for_training/'
    out_path = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/04_data_with_intepolate_for_training/'

    Utility.make_directory(out_path)

    for t in xrange(5):
        for f in ['nasal', 'no', 'non-nasal']:
            for v in ['long', 'short']:
                name = '{}_{}_{}'.format(t, v, f)
                db_file = '{}/{}.npy'.format(db_path, name)

                name_out_path = '{}/{}.npy'.format(out_path, name)

                print name

                if Utility.is_file_exist(db_file):
                    gen_data(db_file, name_out_path)

                    # sys.exit()

    pass
