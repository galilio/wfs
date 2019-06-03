import unittest

class LoadTest(unittest.TestCase):
    def test_loader(self):
        from bayes.wfs.core import loader
        loader.load_datasource()

if __name__ == '__main__':
    unittest.main()