__author__ = 'Hanspeter Hoeschle <hanspeter.hoeschle@gmail.com>'
import os
import unittest

import gams_addon as ga
from create_test_database import create_test_database


class TestGdxToDf(unittest.TestCase):
    def test_read_out_sets(self):
        gdx_file = os.path.join(os.getcwd(), 'test_database.gdx')
        create_test_database(gdx_file)

        df_s = ga.gdx_to_df(gdx_file, 'S')
        self.assertEqual(len(df_s), 10)

        df_subs = ga.gdx_to_df(gdx_file, 'SubS')
        self.assertEqual(len(df_subs), 10)
        self.assertEqual(len(df_subs[df_subs['SubS']]), 5)

        df_i = ga.gdx_to_df(gdx_file, 'I')
        self.assertEqual(len(df_i), 10)

        df_subi = ga.gdx_to_df(gdx_file, 'SubI')
        self.assertEqual(len(df_subi), 10)
        self.assertEqual(len(df_subi[df_subi['SubI']]), 5)

        df_subsi = ga.gdx_to_df(gdx_file, 'SubSI')
        self.assertEqual(len(df_subsi), 100)
        self.assertEqual(len(df_subsi[df_subsi['SubSI']]), 25)

        df_subs_empty = ga.gdx_to_df(gdx_file, 'SubSEmpty')
        self.assertEqual(len(df_subs_empty), 10)
        self.assertEqual(len(df_subs_empty[df_subs_empty['SubSEmpty']]), 0)

    def test_read_out_parameters(self):
        gdx_file = os.path.join(os.getcwd(), 'test_database.gdx')
        create_test_database(gdx_file)

        df_param_s = ga.gdx_to_df(gdx_file, 'Param_S')
        self.assertEqual(len(df_param_s), 10)
        self.assertEqual(sum(df_param_s['Param_S']), 60.)
        self.assertEqual(df_param_s.index.names, ['S'])
        self.assertEqual(df_param_s.columns, ['Param_S'])

        df_param_s_s = ga.gdx_to_df(gdx_file, 'Param_S_S')
        self.assertEqual(len(df_param_s_s), 100)
        self.assertEqual(sum(df_param_s_s['Param_S_S']), 0)
        self.assertEqual(df_param_s_s.index.names, ['S', 'SS'])
        self.assertEqual(df_param_s_s.columns, ['Param_S_S'])

        df_param_s_i = ga.gdx_to_df(gdx_file, 'Param_S_I')
        self.assertEqual(len(df_param_s_i), 100)
        self.assertEqual(sum(df_param_s_i['Param_S_I']), 0)
        self.assertEqual(df_param_s_i.index.names, ['S', 'I'])
        self.assertEqual(df_param_s_i.columns, ['Param_S_I'])
