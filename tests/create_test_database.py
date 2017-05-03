__author__ = 'Hanspeter Hoeschle <hanspeter.hoeschle@gmail.com>'

import gams


def create_test_database(gdx_file):
    ws = gams.GamsWorkspace()
    db = ws.add_database('test_database')

    # SETS
    set_int = db.add_set('I', 1, 'set with integer values')
    for i in range(10):
        set_int.add_record('{0:d}'.format(i + 1))

    set_subset_i = db.add_set_dc('SubI', [set_int], 'subset of I')
    for i in range(5):
        set_subset_i.add_record('{0:d}'.format(i + 1))

    set_str = db.add_set('S', 1, 'set with string values')
    for s in range(10):
        set_str.add_record('s{0:03d}'.format(s + 1))

    set_subset_s = db.add_set_dc('SubS', [set_str], 'subset of S')
    for s in range(5):
        set_subset_s.add_record('s{0:03d}'.format(s + 1))

    set_subset_si = db.add_set_dc('SubSI', [set_str, set_int], 'subset of S and I')
    for s in range(5):
        for i in range(5):
            set_subset_si.add_record(('s{0:03d}'.format(s + 1), '{0:d}'.format(i + 1)))

    set_subset_s_empty = db.add_set_dc('SubSEmpty', [set_str], 'subset of S')

    # Parameters
    set_param_s = db.add_parameter_dc('Param_S', [set_str], 'Test parameter with set S')
    for idx, s in enumerate(range(10)):
        set_param_s.add_record('s{0:03d}'.format(s + 1)).value = 10.5 - idx

    set_param_s_s = db.add_parameter_dc('Param_S_S', [set_str, set_str], 'Test parameter with sets S,S')
    set_param_s_i = db.add_parameter_dc('Param_S_I', [set_str, set_int], 'Test parameter with sets S,I')

    db.export(gdx_file)
