
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.font_manager import FontProperties

fontP = FontProperties()
fontP.set_size('small')
# legend([plot1], "title", prop = fontP)

if __name__ == '__main__':

    labels = [ 
        'A: Baseline (No stress)',
        'B: 2-Level stress by manual labeling',
        'C: 2-Level stress by unsupervised labeling (Linkage clustering)',
        'D: 3-Level stress by semi-supervised (SVM with weight) onto observed data ',
        'E: 3-Level stress by semi-supervised (SVM) onto Latent variable',
        'F-1: 3-Level stress by semi-supervised (SVM with class weight) onto Latent variable + Linear kernel for stress context ',
        'F-2: 3-Level stress by semi-supervised (SVM with class weight) onto Latent variable + SE kernel for stress context'
    ] 

    data = [
        [114.372982,100.599306,98.040114, 96.957874, 97.554723],
        [114.507928,99.912882, 97.603835, 95.657073, 94.942072],
        [113.386412,99.993029, 96.964188, 95.821589, 95.431043],
        [119.107307,105.783525,103.236252,101.692948,99.986811],
        [114.189278,100.281695,98.817170, 97.208393, 97.994278],
        [114.120967,99.570886, 98.159620, 96.472509, 95.931015],
        [114.000816,100.175661,98.020985, 96.068554, 95.738128]
    ]

    # data = [
    #     [32.551546,27.407554,26.091569,25.390196,24.687694],
    #     [25.563314,21.280779,20.390861,20.109760,19.762618],
    #     [25.759242,21.993198,21.106408,20.210699,19.982743],
    #     [31.899782,25.701365,24.404631,23.982139,22.718981],
    #     [25.258267,21.993315,20.924555,20.590635,20.177234],
    #     [24.123664,20.492400,19.474142,18.478059,18.148385],
    #     [24.086776,20.050424,19.011552,18.458226,17.869792]
    # ]

    plt.ylabel('lf0 distortion [cent]')
    # plt.ylabel('Duration distortion [msec]')

    markers=['x', 'H', 'v', '.', 'o', '*', '^']

    color = ['b','g', 'g', 'black', 'r', 'r', 'r']

    x = [50, 250, 450, 650, 850]

    for idx, lab in enumerate(labels):
        plt.plot( x ,data[idx], marker=markers[idx], label=labels[idx], color=color[idx], markersize=10)

    plt.xticks(x)
    plt.xlabel('Training data [Utterances]')

    plt.legend(bbox_to_anchor=(-0.1, -0.1), loc='upper left', ncol=1, prop={'size':10})
    plt.tight_layout()


    plt.savefig('./lf0.eps', bbox_inches='tight')

    pass
