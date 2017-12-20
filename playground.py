import re
import os

host_name = 'epsilon'

local_dir          = re.sub(r'/works?/(?:mint|w\d+)',
                                    '/works/{}'.format(host_name),
                                    os.path.abspath('/work/w23/decha/'))

print local_dir