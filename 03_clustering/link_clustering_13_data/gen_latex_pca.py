
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

def gen_latex(name_path, n_clusters, n_neighbor, name):

    count = 0

    for c in n_clusters:

        tex_file.append('\\begin{figure}[t]')

        for n in n_neighbor:
            title = 'param_n_cluster_{}_n_neighbors_{}x'.format(c, n)

            tex_file.append('\\begin{{minipage}}[b]{{{}\\textwidth}}'.format( 1.0/float(len(n_neighbor)) - 0.01 ))
            tex_file.append('\\centering')
            tex_file.append('\\includegraphics[width=\\textwidth]{{{}/{}.eps}}'.format(name_path, title))
            tex_file.append('\\end{minipage}')

        tex_file.append('\\caption{{{}}}'.format(name.replace('_', '\_')) )
        tex_file.append('\\end{figure}')

        count = count + 1
        if count == 4:
            tex_file.append('\\clearpage')
            count = 0

    pass

if __name__ == '__main__':

    n_clusters = xrange(2, 6)
    n_neighbor = [0.025, 0.05, 0.075, 0.1, 0.2]

    # base_path = '/work/w23/decha/decha_w23/Second_Journal/Unsupervised_learning_result/15_Agglomerative_clustering/'

    base_path = '/work/w23/decha/decha_w23/Second_Journal/Unsupervised_learning_result/15_Agglomerative_clustering_pca/'

    tex_file = []
    tex_file.append('\\documentclass{article}')
    tex_file.append('\\usepackage{geometry}')
    tex_file.append('\\usepackage[usenames, dvipsnames]{color}')
    tex_file.append('\\geometry{margin=1cm}')
    tex_file.append('\\usepackage[english]{babel}')
    tex_file.append('\\usepackage{graphicx}')
    tex_file.append('\\begin{document}')

    for t in xrange(5):
        for f in ['nasal', 'no', 'non-nasal']:
            # for v in ['long', 'short']:
            name = '{}_{}'.format(t, f)
            name_path = '{}/{}/'.format(base_path, name)

            if Utility.is_dir_exists(name_path):
                print name
                gen_latex(name_path, n_clusters, n_neighbor, name)
               
    tex_file.append('\\end{document}')
    Utility.write_to_file_line_by_line('{}/all.tex'.format(base_path), tex_file)

    pass
