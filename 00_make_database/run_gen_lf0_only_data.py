
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

from sklearn import preprocessing

def remove_duration_data(db_file, name_out_path):

    db = Utility.load_obj(db_file)

    new_data = []

    for syl in db:
        d = syl['TF']['intepolate151normailize']['data']
        new_data.append(d)

    new_data = np.array(new_data)

    print new_data

    new_data = np.delete(new_data, [150, 151], axis=1)

    print new_data

    print new_data.shape

    new_db = []
    for idx, syl in enumerate(db):
        syl['TF']['intepolate150_normailize_no_duration'] = dict()
        syl['TF']['intepolate150_normailize_no_duration']['data'] = new_data[idx]
        syl['TF']['intepolate150_normailize_no_duration']['description'] = 'Normalized version of intepolate151, but remove duration'

        new_db.append(syl)

    Utility.save_obj(new_db, name_out_path)

    pass

if __name__ == '__main__':

    db_path = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/05_normalize_of_04/'
    out_path = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/06_normalize_of_04_no_duration/'

    Utility.make_directory(out_path)

    for t in xrange(5):
        for f in ['nasal', 'no', 'non-nasal']:
            for v in ['long', 'short']:

                name = '{}_{}_{}'.format(t, v, f)

                db_file = '{}/{}.npy'.format(db_path, name)
                name_out_path = '{}/{}.npy'.format(out_path, name)

                if Utility.is_file_exist(db_file):
                    remove_duration_data(db_file, name_out_path)
                    # sys.exit()

    pass
