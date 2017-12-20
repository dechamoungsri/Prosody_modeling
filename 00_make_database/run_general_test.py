
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':

    db_path = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/03_data_with_missing_for_training/'

    # for t in xrange(5):
    t = 4
    for f in ['nasal', 'no', 'non-nasal']:
        for v in ['long', 'short']:
            name = '{}_{}_{}'.format(t, v, f)
            db_file = '{}/{}.npy'.format(db_path, name)

            if Utility.is_file_exist(db_file):
                db = Utility.load_obj(db_file)
                print db
                sys.exit()

    pass
