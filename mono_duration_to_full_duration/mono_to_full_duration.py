
import sys
sys.path.append('/work/w16/decha/decha_w16/python_library/Utility/')
from tool_box.util.utility import Utility

def merge(mono_file, full_file, out_file):

    mono = Utility.read_file_line_by_line(mono_file)
    full = Utility.read_file_line_by_line(full_file)

    out = []

    for idx, m in enumerate( mono ):
        spl = m.split(' ')
        out.append( Utility.trim( '{} {} {}'.format(spl[0], spl[1], full[idx])) )

    Utility.write_to_file_line_by_line(out_file, out)

    pass

if __name__ == '__main__':

    mono_silience_remove_path = '/work/w2/decha/Data/GPR_speccom_data/mono/'

    full_path = '/work/w2/decha/Data/GPR_speccom_data/full/'

    out_path = '/work/w2/decha/Data/GPR_speccom_data/full_time_remove_silence/'

    start_set, end_set = 'a', 'z'

    for sett in Utility.char_range(start_set, end_set):
        mono_set_path = '{}/tsc/sd/{}/'.format(mono_silience_remove_path, sett)
        full_set_path = '{}/tsc/sd/{}/'.format(full_path, sett)

        out_set_path = '{}/tsc/sd/{}/'.format(out_path, sett)

        Utility.make_directory(out_set_path)

        for f in Utility.list_file(mono_set_path):
            if f.startswith('.'): continue
            mono_file = '{}/{}'.format(mono_set_path, f)
            full_file = '{}/{}'.format(full_set_path, f)
            out_file = '{}/{}'.format(out_set_path, f)
            merge(mono_file, full_file, out_file)

    pass
