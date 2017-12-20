
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler, RobustScaler

def normalize_data(db_file, name_out_path, target_type, missing_db_file, missing_type):

    db = Utility.load_obj(db_file)

    missing_db = Utility.load_obj(missing_db_file)

    new_data = []

    for syl in db:
        d = syl['TF'][target_type]['data']

        # print syl['dur']

        dur = 0
        for du in syl['dur']:
            dur = dur + du
        consonant_ratio = syl['dur'][0] / dur
        # print consonant_ratio

        missing = None
        for m in missing_db:
            if syl['id'] == m['id']:
                missing = m
                break

        unvoice_frames = np.argwhere(np.isnan(missing['TF'][missing_type]['data']))
        # print unvoice_frames
        unvoice_frames_ratio = float( len(unvoice_frames) ) / float(len(d) - 1)

        d = np.append(d, consonant_ratio)
        d = np.append(d, unvoice_frames_ratio)
        # print d
        new_data.append(d)

        # if not len(unvoice_frames) == 0:
        #     sys.exit()

    new_data = np.array(new_data)

    print new_data.shape

    new_db = []

    for idx, syl in enumerate(db):
        syl['TF']['intepolate151_with_consonant_unvoice_ratio'] = dict()
        syl['TF']['intepolate151_with_consonant_unvoice_ratio']['data'] = new_data[idx]
        syl['TF']['intepolate151_with_consonant_unvoice_ratio']['description'] = 'intepolate151 adding ratio of consonant and unvoice frame in syllable'

        new_db.append(syl)

    Utility.save_obj(new_db, name_out_path)

    pass

if __name__ == '__main__':

    db_path = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/04_data_with_intepolate_for_training/'

    missing_db_path = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/03_data_with_missing_for_training/'

    out_path = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/11_consonant_unvoice_ratio/'

    target_type = 'intepolate151'

    Utility.make_directory(out_path)

    for t in xrange(5):
        # t = 4
        for f in ['nasal', 'no', 'non-nasal']:
            for v in ['long', 'short']:

                name = '{}_{}_{}'.format(t, v, f)

                db_file = '{}/{}.npy'.format(db_path, name)
                name_out_path = '{}/{}.npy'.format(out_path, name)

                missing_db_file = '{}/{}.npy'.format(missing_db_path, name)

                if Utility.is_file_exist(db_file):
                    normalize_data(db_file, name_out_path, target_type, missing_db_file, 'missing151')
                    # sys.exit()

    pass
