__author__ = 'Hanspeter Hoeschle <hanspeter.hoeschle@gmail.com>'
import os
import unittest

import gams_addon as ga
from create_test_database import create_test_database


class TestGdxToDf(unittest.TestCase):
    def test_read_out_sets(self):
        gdx_file = os.path.join(os.getcwd(), 'test_database.gdx')
        create_test_database(gdx_file)

        domain_info = ga.DomainInfo(gdx_file)

        df = ga.gdx_to_df(gdx_file, 'S', domain_info)
        self.assertEqual(len(df), 10)
        self.assertEqual(df.index.nlevels, 1)
        self.assertEqual(df.columns.values, ["S"])
        self.assertEqual(df.index.name, "S")

        df = ga.gdx_to_df(gdx_file, 'SubS', domain_info)
        self.assertEqual(len(df), 10)
        self.assertEqual(len(df[df['SubS']]), 5)
        self.assertEqual(df.index.nlevels, 1)
        self.assertEqual(df.columns.values, ["SubS"])
        self.assertEqual(df.index.name, "S")

        df = ga.gdx_to_df(gdx_file, 'I')
        self.assertEqual(len(df), 10)
        self.assertEqual(df.index.nlevels, 1)
        self.assertEqual(df.columns.values, ["I"])
        self.assertEqual(df.index.name, "I")

        df = ga.gdx_to_df(gdx_file, 'SubI', domain_info)
        self.assertEqual(len(df), 10)
        self.assertEqual(len(df[df['SubI']]), 5)
        self.assertEqual(df.index.nlevels, 1)
        self.assertEqual(df.columns.values, ["SubI"])
        self.assertEqual(df.index.name, "I")

        df = ga.gdx_to_df(gdx_file, 'SubSI', domain_info)
        self.assertEqual(len(df), 100)
        self.assertEqual(len(df[df['SubSI']]), 25)
        self.assertEqual(df.index.nlevels, 2)
        self.assertEqual(df.columns.values, ["SubSI"])
        self.assertEqual(df.index.names, ["S", "I"])

        df = ga.gdx_to_df(gdx_file, 'E', domain_info)
        self.assertTrue(df.empty)

        df = ga.gdx_to_df(gdx_file, 'M_I')
        self.assertEqual(len(df), 100)
        self.assertEqual(df.index.nlevels, 2)
        self.assertEqual(df.columns.values, ["M_I"])
        self.assertEqual(df.index.names, ["Dim1", "Dim2"])

        df = ga.gdx_to_df(gdx_file, 'M_S')
        self.assertEqual(len(df), 100)
        self.assertEqual(df.index.nlevels, 2)
        self.assertEqual(df.columns.values, ["M_S"])
        self.assertEqual(df.index.names, ["Dim1", "Dim2"])

        df = ga.gdx_to_df(gdx_file, 'M_M')
        self.assertEqual(len(df), 100)
        self.assertEqual(df.index.nlevels, 2)
        self.assertEqual(df.columns.values, ["M_M"])
        self.assertEqual(df.index.names, ["Dim1", "Dim2"])

        df = ga.gdx_to_df(gdx_file, 'MAX')
        self.assertEqual(len(df), 10)
        self.assertEqual(df.index.nlevels, 20)
        self.assertEqual(df.columns.values, ["MAX"])
        self.assertEqual(df.index.names, ["Dim%d" % d for d in range(1, 21)])

    def test_read_out_parameters(self):
        gdx_file = os.path.join(os.getcwd(), 'test_database.gdx')
        create_test_database(gdx_file)

        domain_info = ga.DomainInfo(gdx_file)

        df = ga.gdx_to_df(gdx_file, 'Scalar_P1', domain_info)
        self.assertEqual(df, 10)
        self.assertEqual(type(df), float)

        df = ga.gdx_to_df(gdx_file, 'Scalar_P2', domain_info)
        self.assertEqual(df, 10)
        self.assertEqual(type(df), float)

        df_param_s = ga.gdx_to_df(gdx_file, 'Param_S', domain_info)
        self.assertEqual(len(df_param_s), 10)
        self.assertEqual(sum(df_param_s['Param_S']), 60.)
        self.assertEqual(df_param_s.index.names, ['S'])
        self.assertEqual(df_param_s.columns, ['Param_S'])

        df_param_s_s = ga.gdx_to_df(gdx_file, 'Param_S_S', domain_info)
        self.assertEqual(len(df_param_s_s), 100)
        self.assertEqual(sum(df_param_s_s['Param_S_S']), 0)
        self.assertEqual(df_param_s_s.index.names, ['S', 'SS'])
        self.assertEqual(df_param_s_s.columns, ['Param_S_S'])

        df_param_s_i = ga.gdx_to_df(gdx_file, 'Param_S_I', domain_info)
        self.assertEqual(len(df_param_s_i), 100)
        self.assertEqual(sum(df_param_s_i['Param_S_I']), 0)
        self.assertEqual(df_param_s_i.index.names, ['S', 'I'])
        self.assertEqual(df_param_s_i.columns, ['Param_S_I'])

    def test_read_out_variables(self):
        gdx_file = os.path.join(os.getcwd(), 'test_database.gdx')
        create_test_database(gdx_file)

        domain_info = ga.DomainInfo(gdx_file)

        df = ga.gdx_to_df(gdx_file, 'Scalar_V1', domain_info=domain_info)
        self.assertEqual(df, 10)
        self.assertEqual(type(df), float)

        df = ga.gdx_to_df(gdx_file, 'Scalar_V1', domain_info=domain_info, gams_type="lo")
        self.assertEqual(df, 0)
        self.assertEqual(type(df), float)
