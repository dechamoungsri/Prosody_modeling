
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

def rbf(x, lengthscale):

    return np.exp(-1 * (abs(x)*abs(x)) / (lengthscale*lengthscale) )

    pass

if __name__ == '__main__':

    lengthscale = 1

    x = np.linspace(-lengthscale*3, lengthscale*3, 100)
    y = rbf(x, lengthscale)

    print y

    plt.plot(x, y)
    plt.savefig('./test.eps')

    pass
