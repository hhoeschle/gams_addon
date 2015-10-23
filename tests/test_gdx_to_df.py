__author__ = 'Hanspeter Hoeschle <hanspeter.hoeschle@gmail.com>'
import unittest
import os

from gams_addon import gdx_to_df
from create_test_database import create_test_database


class TestGdxToDf(unittest.TestCase):
    def test_read_out_sets(self):
        gdx_file = os.path.join(os.getcwd(), 'tests', 'test_database.gdx')
        create_test_database(gdx_file)

        df_s = gdx_to_df(gdx_file, 'S')
        self.assertEqual(len(df_s), 10)

        df_subs = gdx_to_df(gdx_file, 'SubS')
        self.assertEqual(len(df_subs), 10)
        self.assertEqual(len(df_subs[df_subs['SubS']]), 5)

        df_i = gdx_to_df(gdx_file, 'I')
        self.assertEqual(len(df_i), 10)

        df_subi = gdx_to_df(gdx_file, 'SubI')
        self.assertEqual(len(df_subi), 10)
        self.assertEqual(len(df_subi[df_subi['SubI']]), 5)

        df_subsi = gdx_to_df(gdx_file, 'SubSI')
        self.assertEqual(len(df_subsi), 100)
        self.assertEqual(len(df_subsi[df_subsi['SubSI']]), 25)
