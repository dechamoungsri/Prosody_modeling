
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
        'HMM single-level',
        'GPR single-level',
        'GPR multi-level',
        'GPR single-level with all phoneme in syllable-level context'
    ] 

    # data = [
    #     [114.372982,100.599306,98.040114, 96.957874, 97.554723],
    #     [114.507928,99.912882, 97.603835, 95.657073, 94.942072],
    #     [113.386412,99.993029, 96.964188, 95.821589, 95.431043],
    #     [119.107307,105.783525,103.236252,101.692948,99.986811],
    #     [114.189278,100.281695,98.817170, 97.208393, 97.994278],
    #     [114.120967,99.570886, 98.159620, 96.472509, 95.931015],
    #     [114.000816,100.175661,98.020985, 96.068554, 95.738128]
    # ]

    # data = [
    #     [32.551546,27.407554,26.091569,25.390196,24.687694],
    #     [25.563314,21.280779,20.390861,20.109760,19.762618],
    #     [25.759242,21.993198,21.106408,20.210699,19.982743],
    #     [31.899782,25.701365,24.404631,23.982139,22.718981],
    #     [25.258267,21.993315,20.924555,20.590635,20.177234],
    #     [24.123664,20.492400,19.474142,18.478059,18.148385],
    #     [24.086776,20.050424,19.011552,18.458226,17.869792]
    # ]

    data = [
        [31.6386,27.5201,27.6913,26.6993,26.0776,25.8666,25.5595,25.358,25.1389,25.2057],
        [32.740357,28.655002,26.751112,26.278152,25.334689,25.401301,24.835996,24.608334,24.071253,23.863834],
        [29.688684,26.030981,24.875974,24.107528,23.48884, 23.038487,22.707206,22.3028,21.989227,21.584317],
        [31.452989,27.708012,26.511514,25.904216,25.288778,24.589210,24.416261,23.940160,24.317282,23.407308]
    ]

    # plt.ylabel('lf0 distortion [cent]')
    plt.ylabel('Duration distortion [msec]')

    markers=['x', 'H', 'v', '.', 'o', '*', '^']

    color = ['b','g', 'g', 'r', 'r', 'r', 'r']

    x = [50, 150, 250, 350, 450, 550, 650, 750, 850, 950]

    for idx, lab in enumerate(labels):
        print len(data[idx]), len(x)
        plt.plot( x ,data[idx], marker=markers[idx], label=labels[idx], color=color[idx], markersize=10)

    plt.xticks(x)
    plt.xlabel('Training data [Utterances]')

    plt.legend(bbox_to_anchor=(-0.1, -0.1), loc='upper left', ncol=1, prop={'size':10})
    plt.tight_layout()


    plt.savefig('./gpr.eps', bbox_inches='tight')

    pass
