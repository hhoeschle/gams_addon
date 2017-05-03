__author__ = 'Hanspeter Hoeschle <hanspeter.hoeschle@gmail.com>'
import os
import unittest

from create_test_database import create_test_database
from gams_addon import DomainInfo


class TestDomainInfo(unittest.TestCase):
    def test_domain_info(self):
        gdx_file = os.path.join(os.getcwd(), 'test_database.gdx')
        create_test_database(gdx_file)

        di = DomainInfo(gdx_file)
        print di
        self.assertEqual(len(di.symbols), 9)
