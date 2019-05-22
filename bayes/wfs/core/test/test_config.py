from bayes.wfs.core import Configuration
import unittest

from os import environ
from os.path import join, dirname, join

class TestConfiguration(unittest.TestCase):
    def setUp(self):
        environ['TEST_PASSWORD'] = 'test_password'
        return super().setUp()

    def test_load_config(self):
        cfg = Configuration(path = join(dirname(__file__), 'config.yaml'))
        self.assertEqual(cfg.get('postgresql.username'), 'test')
        self.assertEqual(cfg.get('postgresql.password'), 'test_password')
        self.assertEqual(cfg.get('postgresql.databases'), ['test1', 'test2', 'test3'])

if __name__ == '__main__':
    unittest.main()