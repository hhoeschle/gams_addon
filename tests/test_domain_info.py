__author__ = 'Hanspeter Hoeschle <hanspeter.hoeschle@gmail.com>'
import unittest
import os

from gams_addon import DomainInfo

from create_test_database import create_test_database


class TestDomainInfo(unittest.TestCase):
    def test_domain_info(self):
        gdx_file = os.path.join(os.getcwd(), 'tests', 'test_database.gdx')
        create_test_database(gdx_file)

        di = DomainInfo(gdx_file)
        print di
        self.assertEqual(len(di.symbols), 5)
