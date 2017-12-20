
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
        d = syl['TF']['intepolate151_with_consonant_unvoice_ratio']['data']
        new_data.append(d)

    new_data = np.array(new_data)

    print new_data

    X_scaled = preprocessing.scale(new_data)

    print X_scaled

    new_db = []
    for idx, syl in enumerate(db):
        syl['TF']['intepolate151_with_consonant_unvoice_ratio_standardization'] = dict()
        syl['TF']['intepolate151_with_consonant_unvoice_ratio_standardization']['data'] = X_scaled[idx]
        syl['TF']['intepolate151_with_consonant_unvoice_ratio_standardization']['description'] = 'Standardized version of intepolate151_with_consonant_unvoice_ratio'

        new_db.append(syl)

    Utility.save_obj(new_db, name_out_path)

    pass

if __name__ == '__main__':

    db_path = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/11_consonant_unvoice_ratio/'
    out_path = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/12a_standardization_of_11/'

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
