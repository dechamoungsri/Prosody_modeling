
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
            for v in ['long', 'short']:
                name = '{}_{}_{}'.format(t, v, f)

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

    # figure_paths = [
    #     '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/12c_normalization_by_preprocessing_of_11_data/figure_dim_10/',
    #     '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/08c_preprocessing_normaiize/figure_dim_10/',
    # ]

    figure_paths = [
        '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/13c_pca_normalization_by_preprocessing_of_12_data/figure_dim_10/',
        '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/09c_preprocessing_normalize/figure_dim_10/',
    ]


    method_names = [
        'With ratio',
        'Without ratio'
    ]

    comparison_name = 'ratio_features_comparison_pca'

    path = '/work/w23/decha/decha_w23/Second_Journal/Latent_space_training_result/Figure/'
    Utility.make_directory(path)

    out_file_path = '{}/{}/'.format(path, comparison_name)
    Utility.make_directory(out_file_path)

    name_out_path = '{}/{}.tex'.format(out_file_path, comparison_name)

    plot_latex_for_compasison(figure_paths, method_names, name_out_path)

    pass
