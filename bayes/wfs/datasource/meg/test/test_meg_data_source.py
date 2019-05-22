import unittest

from bayes.wfs.datasource.meg import *
from bayes.wfs.core import Configuration
from bayes.wfs.core.exceptions import *
from os.path import dirname, join

class TestMegDataSource(unittest.TestCase):
    def test_config_exception(self):
        cfg = Configuration(join(dirname(__file__), 'config-exception.yaml'))
        self.assertRaises(MissingConfigError, MegDataSource, cfg)

    def test_config_db(self):
        cfg = Configuration(join(dirname(__file__), 'config.yaml'))
        print(cfg.get('MegDataSource.db'))
    
    def test_get_capabilities(self):
        cfg = Configuration(join(dirname(__file__), 'config.yaml'))
        megdata = MegDataSource(cfg = cfg)
        self.assertRaises(FormatNotSupportedException, megdata.get_capabilities, '2.0.0', 'ALL', None, ['test'])
        self.assertRaises(VersionNegotiationFailed, megdata.get_capabilities, '2.0.1', 'ALL', None, None)

        caps = megdata.get_capabilities('2.0.0', ['ServiceIdentification'], None, None)
        self.assertEqual(caps.version, '2.0.0')
        self.assertIsNone(caps.service_provider)
        self.assertEqual(caps.service_identification.description.title, 'BayesBA Meg GIS')
        self.assertIsNone(caps.operations_metadata)

        caps = megdata.get_capabilities('2.0.0', ['ServiceIdentification', 'ServiceProvider'], None, None)
        self.assertEqual(caps.version, '2.0.0')
        self.assertEqual(caps.service_provider.provider_name, 'BayesBa')
        self.assertEqual(caps.service_identification.description.title, 'BayesBA Meg GIS')
        self.assertIsNone(caps.contents)
        self.assertIsNone(caps.operations_metadata)

        caps = megdata.get_capabilities('2.0.0', ['ServiceIdentification', 'ServiceProvider', 'Contents'], None, None)
        self.assertEqual(caps.version, '2.0.0')
        self.assertEqual(caps.service_provider.provider_name, 'BayesBa')
        self.assertEqual(caps.service_identification.description.title, 'BayesBA Meg GIS')
        self.assertIsNone(caps.operations_metadata)

    def test_describe_feature_type(self):
        cfg = Configuration(join(dirname(__file__), 'config.yaml'))
        megdata = MegDataSource(cfg = cfg)
        caps = megdata.get_capabilities('2.0.0', 'ALL', None, None)
        feature = caps.contents[0]
        ft = megdata.describe_feature_type([feature.name])[feature.name]
        self.assertEqual(ft, feature)

        self.assertRaises(InvalidTypeName, megdata.describe_feature_type, ['test'])

    def test_get_feature(self):
        cfg = Configuration(join(dirname(__file__), 'config.yaml'))
        megdata = MegDataSource(cfg = cfg)

        self.assertRaises(AliasesMissmatch, megdata.get_feature, ['test1', 'test2'], [])
        self.assertRaises(InvalidTypeName, megdata.get_feature, ['test1', 'test2'])
        megdata.get_feature(['public.gis_block'])
        megdata.get_feature(['public.gis_block'], ['a'])

        self.assertRaises(ProjectionFailed, megdata.get_feature, ['public.gis_block'], projection = [['a']])
        self.assertRaises(NoSuchProperty, megdata.get_feature, ['public.gis_block'], projection = ['a'])

        megdata.get_feature(['public.gis_block'], ['a'], ['geom', 'tags', 'show'])

if __name__ == '__main__':
    unittest.main()