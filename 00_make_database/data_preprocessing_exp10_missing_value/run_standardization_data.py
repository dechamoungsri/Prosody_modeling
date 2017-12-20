
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

from sklearn import preprocessing

def normalize_data(db_file, name_out_path):

    db = Utility.load_obj(db_file)

    new_data = []

    for syl in db:
        d = syl['TF']['missing151']['data']
        dd = np.array(d)
        dd[np.argwhere(np.isnan(d))] = un_voice
        new_data.append(dd)

    new_data = np.array(new_data)

    print new_data

    X_scaled = preprocessing.scale(new_data)

    print X_scaled
    print X_scaled.shape

    new_db = []
    for idx, syl in enumerate(db):
        syl['TF']['missing151_standardization'] = dict()
        syl['TF']['missing151_standardization']['data'] = X_scaled[idx]
        syl['TF']['missing151_standardization']['description'] = 'Standardized version of missing151'

        new_db.append(syl)

    Utility.save_obj(new_db, name_out_path)

    pass

un_voice = -100.0

if __name__ == '__main__':

    db_path = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/03_data_with_missing_for_training/'
    out_path = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/10a_standardization_of_03/'

    Utility.make_directory(out_path)

    for t in xrange(5):
        for f in ['nasal', 'no', 'non-nasal']:
            for v in ['long', 'short']:

                name = '{}_{}_{}'.format(t, v, f)

                db_file = '{}/{}.npy'.format(db_path, name)
                name_out_path = '{}/{}.npy'.format(out_path, name)

                if Utility.is_file_exist(db_file):
                    normalize_data(db_file, name_out_path)
                    # sys.exit()

    pass
