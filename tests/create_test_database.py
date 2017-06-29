__author__ = 'Hanspeter Hoeschle <hanspeter.hoeschle@gmail.com>'

import gams


def create_test_database(gdx_file):
    ws = gams.GamsWorkspace()
    db = ws.add_database('test_database')

    # Sets
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

    set_empty = db.add_set('E', 1, 'Empty set')
    set_empty.clear()

    set_multi_i = db.add_set('M_I', 2, 'set with integer values')
    for i in range(10):
        for ii in range(10):
            idx = ('{0:d}'.format(i + 1), '{0:d}'.format(ii + 1))
            set_multi_i.add_record(idx)

    set_multi_s = db.add_set('M_S', 2, 'set with string values')
    for i in range(10):
        for ii in range(10):
            idx = ('s{0:03d}'.format(i + 1), 's{0:03d}'.format(ii + 1))
            set_multi_s.add_record(idx)

    set_multi_mixed = db.add_set('M_M', 2, 'set with mixed values')
    for i in range(10):
        for ii in range(10):
            idx = ('s{0:03d}'.format(i + 1), '{0:d}'.format(ii + 1))
            set_multi_mixed.add_record(idx)

    set_max = db.add_set('MAX', 20, 'set with highest possible dimension')
    for t in range(1, 11):
        idx = list(['{0:d}'.format(i + t) for i in range(20)])
        set_max.add_record(idx)

    # Parameters
    # Scalar
    s = db.add_parameter('Scalar_P1', 0, 'Test scalar parameter')
    s.add_record().value = 10
    s = db.add_parameter('Scalar_P2', 0, 'Test scalar parameter')
    s.add_record().value = 10.0


    param_s = db.add_parameter_dc('Param_S', [set_str], 'Test parameter with set S')
    for idx, s in enumerate(range(10)):
        param_s.add_record('s{0:03d}'.format(s + 1)).value = 10.5 - idx

    set_param_s_s = db.add_parameter_dc('Param_S_S', [set_str, set_str], 'Test parameter with sets S,S')
    set_param_s_i = db.add_parameter_dc('Param_S_I', [set_str, set_int], 'Test parameter with sets S,I')

    # Variables
    # Scalar
    s = db.add_variable('Scalar_V1', 0, gams.VarType.Positive, "Test Scalar variable")
    s_r = s.add_record()
    s_r.level = 10
    s_r.lower = 0
    s_r.upper = 1000
    s_r.marginal = 2
    # s.add_record().level = 10



    db.export(gdx_file)
