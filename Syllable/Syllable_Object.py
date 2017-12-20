#!/usr/bin/python

import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
from tool_box.util.utility import Utility

import numpy as np

class Syllable(object):
    """docstring for Syllable"""
    def __init__(self, id, tone, consonant, vowel, finalconsonant, duration, raw_lf0):
        super(Syllable, self).__init__()
        self.id = id
        self.tone = tone
        self.consonant = consonant
        self.vowel = vowel
        self.finalconsonant = finalconsonant
        self.duration = duration
        self.raw_lf0 = raw_lf0
    
    @staticmethod
    def get_normailze_with_missing_data(y, num_sampling, dur):

        # print dur

        all_dur = 0
        for d in dur:
            all_dur = all_dur + (d/50000)

        consonant_part = (dur[0]/50000)/all_dur * len(y)

        y = np.array(y)
        # print len(y)

        y = y[consonant_part:len(y)]
        # print len(y), consonant_part, all_dur

        y[y<0] = np.nan

        x = np.linspace(0, len(y), num=num_sampling)
        y = np.interp(x, np.arange(len(y)), y)

        delta = np.gradient(y)
        delta2 = np.gradient(delta)
        y = np.append(y, delta)
        y = np.append(y, delta2)

        tonal_part = 0
        for idx, t in enumerate(dur) :
            if idx == 0: continue

            tonal_part = tonal_part + t/50000

        y = np.append(y, tonal_part)
        # print y, len(y)

        return y

        pass

    @staticmethod
    def get_normalize_gradient_interpolation(y, num_sampling, dur, debug=False):

        y = Syllable.cut_consoant(y, dur)
        # print 'Ori ', y

        y = Syllable.remove_head_tail(y, debug=debug)
        if y == 0:
            # print y
            return None

        y = Syllable.interpolate(y)
        y = Syllable.normailize(y, num_sampling)

        y = Syllable.add_delta(y)
        y = Syllable.add_dur(y, dur)

        return y

        pass

    @staticmethod
    def add_dur(y, dur):

        tonal_part = 0
        for idx, t in enumerate(dur) :
            if idx == 0: continue

            tonal_part = tonal_part + t/50000

        y = np.append(y, tonal_part)
        return y

    @staticmethod
    def add_delta(y):
        delta = np.gradient(y)
        delta2 = np.gradient(delta)
        y = np.append(y, delta)
        y = np.append(y, delta2)
        return y

    @staticmethod
    def normailize(y, num_sampling):
        x = np.linspace(0, len(y), num=num_sampling)
        y = np.interp(x, np.arange(len(y)), y)
        return y

    @staticmethod
    def normalized(y, num_sampling):
        x = np.linspace(0, len(y), num=num_sampling)
        y = np.interp(x, np.arange(len(y)), y)

        print len(y)

    @staticmethod
    def interpolate(y):

        y = np.array(y)
        y[y<0] = np.nan

        if len(y) < 2:
            return y

        x = np.arange(len(y))
        degree = 2

        tx = []
        ty = []

        unvoice_indecies = []

        for i in range(len(y)) :
            if not np.isnan(y[i]):
                # print i
                tx.append(x[i])
                ty.append(y[i])
            else :
                unvoice_indecies.append(i)

        poly_coeff = np.polyfit(np.array(tx), np.array(ty), degree)

        # print poly_coeff
        poly_val = np.polyval(poly_coeff, unvoice_indecies)
        # print poly_val

        for idx, i in enumerate(unvoice_indecies):
            y[i] = poly_val[idx]

        # print y

        return y

        pass

    @staticmethod
    def remove_head_tail(y, debug=False):

        y = y.tolist()

        # print '-------------------------------'

        start = 0

        # print y

        for d in y:
            # print d
            if d < 0: 
                start = start + 1
            else :
                break

        # print start

        end = len(y)
        for e in reversed(range(len(y))):
            if y[e] > 0:
                break
            else :
                end = end - 1

        if debug:
            print start, end

        if start >= end:
            return 0

        # print y, len(y), end

        for i in reversed(range(end, len(y))):
            # print i, y[i]
            del y[i]

        for i in reversed(range(0, start)):
            del y[i]

        # print y

        return y

        pass

    @staticmethod
    def cut_consoant(y, dur):
        all_dur = 0
        for d in dur:
            all_dur = all_dur + (d/50000)

        consonant_part = (dur[0]/50000)/all_dur * len(y)

        y = np.array(y)
        # print len(y)

        y = y[consonant_part:len(y)]
        return y

    @staticmethod
    def find_stress_info(stress_path, name):

        spl = name.split('_')
        sett = spl[0][5]
        syl_index = spl[1]

        filename = spl[0]

        # print sett, syl_index

        for s in Utility.list_file(stress_path):
            if s[0] == sett:
                file_path = '{}/{}/{}.lab'.format(stress_path, s, filename)
                # print file_path

                lines = Utility.read_file_line_by_line(file_path)
                ss = lines[int(syl_index)-1].split(' ')

                return Utility.trim(ss[3])

                break


