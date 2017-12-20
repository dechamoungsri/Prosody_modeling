
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

nasal_list = ['n^', 'm^', 'ng^']
short_vowel = ['va', 'ia', 'q', '@', 'a', 'e', 'i', 'o', 'u', 'v', 'x', 'ua']

sep_list = dict()

def run_separate(db_obj, outpath):

    for syl in db_obj:
        # print syl

        vowel = syl['vowel']
        finalconsonant = syl['finalconsonant']
        tone = syl['tone']

        # print vowel, finalconsonant

        if vowel in short_vowel:
            v = 'short'
        else:
            v = 'long'

        if finalconsonant in nasal_list:
            f = 'nasal'
        elif finalconsonant == 'z^':
            f = 'no'
        else :
            f = 'non-nasal'

        name = '{}_{}_{}'.format(tone, v, f)
        if name in sep_list:
            sep_list[name].append(syl)

        # sys.exit()

    for key in sep_list:
        print key, ' : ', len(sep_list[key])
        if not len(sep_list[key]) == 0:
            Utility.save_obj(sep_list[key], '{}/{}.npy'.format(outpath ,key))
        

    pass

if __name__ == '__main__':

    database = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/all_syllable.npy'

    outpath = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/'

    for t in xrange(5):
        for f in ['no', 'nasal', 'non-nasal']:
            for v in ['short', 'long']:
                name = '{}_{}_{}'.format(t, v, f)
                sep_list[name] = []

    dat = Utility.load_obj(database)
    run_separate(dat, outpath)

    pass
