
import sys

# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('../')

from tool_box.util.utility import Utility
from Syllable.Syllable_Object import Syllable

import re

def run_make_obj_for_an_utterance(full_path, dur_path, lf0_path):

    global syl_database

    pattern = re.compile(r"""(?P<start>.+)\s(?P<end>.+)\s(?P<consonant>.+)\-(?P<vowel>.+)\+(?P<finalconsonant>.+)/A:.+/B:.+\-(?P<tone>.+)\+.+/C:.+/E:.+""",re.VERBOSE)

    # print dur_path
    # print lf0_path

    dur_list = Utility.load_obj(dur_path)

    lf0_list = Utility.list_file(lf0_path)

    lf0_list = sort_dur_list_by_index(lf0_list)

    # print lf0_list

    for idx, line in enumerate(Utility.read_file_line_by_line(full_path)):

        c = idx+1

        # print line
        l = Utility.trim(line)

        match = re.match(pattern, line)
        if match:

            start = float(match.group('start'))
            end = float(match.group('end'))

            consonant = match.group('consonant')
            vowel = match.group('vowel')
            finalconsonant = match.group('finalconsonant')
            tone = match.group('tone')

            dur = dur_list[idx]

            lf0 = Utility.read_file_line_by_line('{}/{}'.format(lf0_path, lf0_list[idx]))
            lf0 = [float(i) for i in lf0]

            iden = '{}_{}'.format(Utility.get_basefilename(full_path), c)

            # print start, end, consonant, vowel, finalconsonant, tone, dur, lf0, iden

            syl = dict()#Syllable(iden, tone, consonant, vowel, finalconsonant, dur, lf0)

            syl['id'] = iden
            syl['tone'] = tone
            syl['consonant'] = consonant
            syl['vowel'] = vowel
            syl['finalconsonant'] = finalconsonant
            syl['dur'] = dur
            syl['raw_lf0'] = lf0

            syl_database.append(syl)

            # sys.exit(0)

        else:
            raise TypeError("WTF")

    pass

def sort_dur_list_by_index(lf0_list):

    pattern = re.compile(r"""(?P<index>.+)_.+""",re.VERBOSE)

    out_list = []
    l = len(lf0_list)

    for x in xrange(l):
        idx = x+1
        for n in lf0_list:

            spl = n.split('_')
            # print spl
            if int(spl[0]) == idx:
                out_list.append(n)
                continue

            # print n
            # match = re.match(pattern, n)
            # if match:
                # index = int(match.group('index'))
                # if index == idx:
                #     out_list.append(n)
                #     continue

    if not l == len(out_list):
        raise TypeError("WTF : not equal, {}, {}".format(len(l), len(out_list)))

    return out_list

def run_gen(full_path, dur_path, lf0_path, start, stop):

    for sett in Utility.char_range(start, stop):

        dur_set_path = '{}/{}/'.format(dur_path, sett)
        full_set_path = '{}/{}/'.format(full_path, sett)
        lf0_set_path = '{}/{}/'.format(lf0_path, sett)

        if not (Utility.is_dir_exists(dur_set_path) & Utility.is_dir_exists(full_set_path) & Utility.is_dir_exists(lf0_set_path) ):
            print 'No set : ', sett
            continue

        for f in Utility.list_file(full_set_path):
            if f.startswith('.') : continue
            print f

            base = Utility.get_basefilename(f)

            dur_list = '{}/{}.dur'.format(dur_set_path, base)
            lf0_list = '{}/{}/'.format(lf0_set_path, base)
            full_list = '{}/{}.lab'.format(full_set_path, base)

            run_make_obj_for_an_utterance(full_list, dur_list, lf0_list)

            # sys.exit(0)

    pass

syl_database = []

if __name__ == '__main__':

    # Syllable('a', 'a', 'a', 'a', 'a', 'a', 'a')

    # Syllable(id, tone, consonant, vowel, finalconsonant, duration, raw_lf0)

    full_path = '/work/w2/decha/Data/GPR_speccom_data/00_syllable_level_data/full_time/tsc/sd/'

    dur_path = '/work/w2/decha/Data/GPR_speccom_data/phones_in_syllable_duration_object/'

    lf0_path = '/work/w2/decha/Data/GPR_speccom_data/lf0_in_syllable/'

    start = 'a'
    stop = 'z'

    run_gen(full_path, dur_path, lf0_path, start, stop)

    outpath_file = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/all_syllable.npy'

    Utility.save_obj(syl_database, outpath_file)
