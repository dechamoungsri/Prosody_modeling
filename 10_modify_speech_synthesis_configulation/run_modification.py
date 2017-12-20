
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np
import matplotlib.pyplot as plt

def dataset_modification(config_path, output_path):

    data_config_path = '{}/data.yaml'.format(config_path)

    data = Utility.yaml_load(data_config_path)

    dataset = data['subset']

    print dataset

    for i in xrange(5, 20, 4):
        
        if training_set[i-1] == 'i': 
            continue

        subset = training_set[0:i]
        # print subset
        # print len(subset), len(subset)*50

        dataset[ '{}-{}'.format(subset[0], subset[len(subset)-1]) ] = subset

    # print dataset
    # print data

    Utility.yaml_save('{}/data.yaml'.format(output_path), data)

    pass

training_set = [
    'a', 'b', 'c', 'd', 'e',
    'f', 'g', 'h', 'i', 'l',
    'm', 'o', 'p', 'r', 't',
    'u', 'v', 'w', 'x', 'y'
]

def change_exp(config_path, output_path, subset):

    exp = Utility.yaml_load( '{}/experiment.yaml'.format(config_path) )

    exp['data_set']['optim_dur'] = 'a-{}'.format(subset[len(subset)-1])
    exp['data_set']['train'] = 'a-{}'.format(subset[len(subset)-1])

    print exp

    Utility.yaml_save('{}/experiment.yaml'.format(output_path), exp)

    pass

if __name__ == '__main__':

    config_path = '/work/w23/decha/decha_w23/Second_Journal/Speech_synthesis_system/00_conventional/testrun/config/'

    for n, i in zip([250, 450, 650, 850], xrange(5, 20, 4)):

        if n == 450: continue

        n_config_path = '{}/th{}/'.format(config_path, n)
        n_dur_config_path = '{}/th{}_dur/'.format(config_path, n)

        Utility.make_directory(n_config_path)
        Utility.make_directory(n_dur_config_path)

        src = '{}/th450/'.format(config_path, n)
        src_dur = '{}/th450_dur/'.format(config_path, n)

        # for f in Utility.list_file(src):
        #     # print f
        #     Utility.copyFile('{}/{}'.format(src, f), '{}/{}'.format(n_config_path, f))
        #     Utility.copyFile('{}/{}'.format(src_dur, f), '{}/{}'.format(n_dur_config_path, f))

        print n, i, i*50

        subset = training_set[ 0: i ]
        print subset

        change_exp(src, n_config_path, subset)
        change_exp(src_dur, n_dur_config_path, subset)

    # config_path = '/work/w23/decha/decha_w23/Second_Journal/Speech_synthesis_system/00_template/testrun/config/th450/'
    # output_path = '/work/w23/decha/decha_w23/Second_Journal/Speech_synthesis_system/00_conventional/testrun/config/th450/'
    
    # config_dur_path = '/work/w23/decha/decha_w23/Second_Journal/Speech_synthesis_system/00_template/testrun/config/th450_dur/'
    # output_dur_path = '/work/w23/decha/decha_w23/Second_Journal/Speech_synthesis_system/00_conventional/testrun/config/th450_dur/'

    # dataset_modification(config_path, output_path)
    # dataset_modification(config_dur_path, output_dur_path)

    # for i in zip(xrange(5, 20, 4)):

    #     print i[0]

    #     if training_set[i[0]-1] == 'i': 
    #         continue

    #     subset = training_set[0: i[0] ]
    #     print subset

    #     # change_exp(config_path, output_path, subset)

    #     pass

    pass
