
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

def merge(short_db, long_db):

    s = Utility.load_obj(short_db)
    l = Utility.load_obj(long_db)

    print len(s), len(l)

    merge = s+l

    print len(merge)

    return merge

    pass

if __name__ == '__main__':

    db_path = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/08c_normalize_of_04/'
    out_path = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/13_merge_vowel_08c/'

    Utility.make_directory(out_path)

    for t in xrange(5):
        for f in ['nasal', 'no', 'non-nasal']:
            # for v in ['long', 'short']:
            v = ['long', 'short']
            name_short = '{}_{}_{}'.format(t, v[1], f)
            db_short_file = '{}/{}.npy'.format(db_path, name_short)

            name_long = '{}_{}_{}'.format(t, v[0], f)
            db_long_file = '{}/{}.npy'.format(db_path, name_long)

            mer = Utility.load_obj(db_long_file)

            if Utility.is_file_exist(db_short_file):
                mer = merge(db_short_file, db_long_file)

            name_db = '{}_{}'.format(t, f)
            Utility.save_obj(mer, '{}/{}.npy'.format(out_path, name_db))

        # sys.exit()

    pass
