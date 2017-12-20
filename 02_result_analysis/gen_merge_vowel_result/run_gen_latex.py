
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

def plot_latex_for_compasison(figure_paths, method_names, name_out_path):

    methods = len(figure_paths)

    tex_file = []
    tex_file.append('\\documentclass{article}')
    tex_file.append('\\usepackage{geometry}')
    tex_file.append('\\usepackage[usenames, dvipsnames]{color}')
    tex_file.append('\\geometry{margin=1cm}')
    tex_file.append('\\usepackage[english]{babel}')
    tex_file.append('\\usepackage{graphicx}')
    tex_file.append('\\begin{document}')

    count = 0

    for t in xrange(5):
        for f in ['nasal', 'no', 'non-nasal']:
            name = '{}_{}'.format(t, f)
            #------------ Figure ----------------#
            print '{}/{}.eps'.format(figure_paths[0], name)

            if Utility.is_file_exist('{}/{}.eps'.format(figure_paths[0], name)):
                tex_file.append('\\begin{figure}[t]')

                # minipage #
                for idx, i in enumerate( figure_paths ):    
                    eps = '{}/{}.eps'.format(figure_paths[idx], name)
                    if Utility.is_file_exist(eps):
                        tex_file.append('\\begin{{minipage}}[b]{{{}\\textwidth}}'.format( 1.0/float(methods) - 0.01 ))
                        tex_file.append('\\centering')
                        tex_file.append('\\includegraphics[width=\\textwidth]{{{}/{}.eps}}'.format(figure_paths[idx], name))
                        tex_file.append('{}'.format(method_names[idx]))
                        tex_file.append('\\end{minipage}')

                # minipage #
                tex_file.append('\\caption{{{}}}'.format(name.replace('_', '\_')) )
                tex_file.append('\\end{figure}')

            #------------ Figure ----------------#

            count = count + 1
            if count == 4:
                tex_file.append('\\clearpage')
                count = 0

    tex_file.append('\\end{document}')

    Utility.write_to_file_line_by_line(name_out_path, tex_file)

    pass

if __name__ == '__main__':

    figure_paths = [
        '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/14_merge_vowel_13_data/figure_dim_2/',
        '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/14_merge_vowel_13_data/figure_dim_5/',
        '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/15_merge_pca_13/figure_dim_2/',
        '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/15_merge_pca_13/figure_dim_5/'
    ]

    method_names = [
        'GP-LVM 2',
        'GP-LVM 5',
        'PCA 2',
        'PCA 5',
    ]

    name_out_path = '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/15_merge_pca_13/figure_pca_vs_gplvm_dim_2_5.tex'

    plot_latex_for_compasison(figure_paths, method_names, name_out_path)

    pass
