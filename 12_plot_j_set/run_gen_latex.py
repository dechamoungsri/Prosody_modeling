
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

def find_syl(db_syl, name):

    for syl in db_syl:
        if syl['id'] == name:
            return syl

    pass

def gen_latex(db_filepath, figure_path_name, name_out_path, syl_db_name):

    print db_filepath

    syl_list = Utility.load_obj(db_filepath)

    print 'List length : {}'.format(len(syl_list))

    fig_path = '{}/{}/'.format(figure_path, figure_path_name)

    tex_file = []
    tex_file.append('\\documentclass{article}')
    tex_file.append('\\usepackage{geometry}')
    tex_file.append('\\usepackage[usenames, dvipsnames]{color}')
    tex_file.append('\\geometry{margin=1cm}')
    tex_file.append('\\usepackage[english]{babel}')
    tex_file.append('\\usepackage{graphicx}')
    tex_file.append('\\begin{document}')
    tex_file.append('\\begin{figure}[t]')

    count = 0

    db = Utility.load_obj(syl_db_name)

    for syl in syl_list:
        # print syl
        name = syl[0]

        syl_info = find_syl(db, name)

        # print name
        tex_file.append('\\begin{minipage}[b]{.24\\textwidth}')

        if (syl_info['id'] in potential_list) & (syl[2] == '1'): 
            tex_file.append('\colorbox{yellow}{Stress and potent}')
        elif (syl_info['id'] in potential_list) & (syl[2] == '2'): 
            tex_file.append('\colorbox{green}{May Stress and potent}')
        elif syl[2] == '1':
            tex_file.append('\colorbox{red}{Stress}')
        elif syl[2] == '2':
            tex_file.append('\colorbox{blue}{May Stress}')
        elif syl_info['id'] in potential_list:
            tex_file.append('\colorbox{Apricot}{Potent}')
        else:
            tex_file.append('UnStress')
        tex_file.append('\\centering')

        eps = None
        long_eps = '/work/w2/decha/Data/GPR_speccom_data/figure/lf0_plot_by_vowel_finalconsonant/{}_long_{}/{}.eps'.format(figure_path_name.split('_')[0], figure_path_name.split('_')[1], name)
        if Utility.is_file_exist(long_eps):
            eps = long_eps
        else :
            eps = '/work/w2/decha/Data/GPR_speccom_data/figure/lf0_plot_by_vowel_finalconsonant/{}_short_{}/{}.eps'.format(figure_path_name.split('_')[0], figure_path_name.split('_')[1], name)

        tex_file.append('\\includegraphics[width=\\textwidth]{{{}}}'.format(eps))
        tex_file.append('{} {}-{}-{}-{} {}'.format(name.replace('_', '-'), syl_info['consonant'], syl_info['vowel'], syl_info['finalconsonant'].replace('^', '\\textasciicircum'), syl_info['tone'],  syl[1]/50000))
        tex_file.append('\\end{minipage}')

        count = count + 1
        if count == 20:
            tex_file.append('\\end{figure}')
            tex_file.append('\\clearpage')
            tex_file.append('\\begin{figure}[t]')
            count = 0
        elif count%4 == 0:
            tex_file.append('\\end{figure}')
            tex_file.append('')
            tex_file.append('\\begin{figure}[t]')
        
    # if not count == 0:
    tex_file.append('\\end{figure}')

    tex_file.append('\\end{document}')

    Utility.write_to_file_line_by_line(name_out_path, tex_file)

    pass

figure_path = '/work/w2/decha/Data/GPR_speccom_data/figure/lf0_plot_by_vowel_finalconsonant/'

potential_list = Utility.load_obj('/work/w23/decha/decha_w23/Second_Journal/sync_google_drive/Second_journal_Code/13_get_last_syl_of_mul_noun/potential_list.pkl')

if __name__ == '__main__':

    # db_path = '/work/w2/decha/Data/GPR_speccom_data/figure/plot_sort_list/'
    # syl_db_path = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/'

    # out_path = '/work/w2/decha/Data/GPR_speccom_data/figure/tex_file/'

    db_path = '/work/w2/decha/Data/GPR_speccom_data/syllable_database/14_j_set_database/'
    syl_db_path = db_path

    out_path = './figure/'
    Utility.make_directory(out_path)

    for t in xrange(5):
        for f in ['nasal', 'no', 'non-nasal']:
            # for v in ['long', 'short']:
            name = '{}_{}'.format(t, f)
            db_file = '{}/{}_sorted_list.npy'.format(db_path, name)

            syl_db_name = '{}/{}.npy'.format(syl_db_path, name)

            name_out_path = '{}/{}.tex'.format(out_path, name)

            if Utility.is_file_exist(db_file):
                gen_latex(db_file, name, name_out_path, syl_db_name)
                # sys.exit()

        # sys.exit()

    pass
