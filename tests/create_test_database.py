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



    db.export(gdx_file)
