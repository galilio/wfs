import unittest
from bayes.geojson import leaflet
from bayes.wfs.datasource.meg import *
from bayes.wfs.core import Configuration
from bayes.wfs.core.exceptions import *
from bayes.wfs.core.filter import *
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

        self.assertRaises(ProjectionFailed, megdata.get_feature, ['public.gis_block'], projection = [['a']])
        self.assertRaises(NoSuchProperty, megdata.get_feature, ['public.gis_block'], projection = ['a'])

        # megdata.get_feature(['public.gis_block'], ['a'], ['geom', 'tags', 'show'])

    def test_get_feature_filter(self):
        cfg = Configuration(join(dirname(__file__), 'config.yaml'))
        megdata = MegDataSource(cfg = cfg)

        eq_filter = EqualTo(ValueRef('public.gis_block/id'), Literal(660000625))
        megdata.get_feature(['public.gis_block'], ['a'], ['id', 'district_id', 'city_id'], filter = eq_filter, fetch_data = False)

        eq_filter = EqualTo(Literal('23432'), Literal(441500))
        megdata.get_feature(['public.gis_block'], ['a'], ['id', 'district_id', 'city_id'], filter = eq_filter, fetch_data = False)

        eq_filter = And([EqualTo(ValueRef('public.gis_block/city_id'), Literal(441500)),
            EqualTo(ValueRef('public.gis_block/id'), Literal(660000625))])
        megdata.get_feature(['public.gis_block'], ['a'], ['id', 'district_id', 'city_id'], filter = eq_filter, fetch_data = False)

        eq_filter = Or([EqualTo(ValueRef('public.gis_block/id'), Literal(660000624)),
            EqualTo(ValueRef('public.gis_block/id'), Literal(660000625))])
        megdata.get_feature(['public.gis_block'], ['a'], ['id', 'district_id', 'city_id'], filter = eq_filter, fetch_data = False)

        eq_filter = And([Or([EqualTo(ValueRef('public.gis_block/id'), Literal(660000624)),
            EqualTo(ValueRef('public.gis_block/id'), Literal(660000625))]),
            Not(EqualTo(ValueRef('public.gis_block/id'), Literal(660000625)))])
        megdata.get_feature(['public.gis_block'], ['a'], ['id', 'district_id', 'city_id'], filter = eq_filter, fetch_data = False)

        eq_filter = NotEqualTo(ValueRef('public.gis_block/id'), Literal(660000624))
        megdata.get_feature(['public.gis_block'], ['a'], ['id', 'district_id', 'city_id'], filter = eq_filter, fetch_data = False)

        eq_filter = NotEqualTo(ValueRef('public.gis_block/id'), Literal(660000624))
        megdata.get_feature(['public.gis_block'], ['a'], ['id', 'district_id', 'city_id'], filter = eq_filter, fetch_data = False)

        eq_filter = LessThan(ValueRef('public.gis_block/id'), Literal(660000624))
        megdata.get_feature(['public.gis_block'], ['a'], ['id', 'district_id', 'city_id'], filter = eq_filter, fetch_data = False)

        eq_filter = GreaterThan(ValueRef('public.gis_block/id'), Literal(660000624))
        megdata.get_feature(['public.gis_block'], ['a'], ['id', 'district_id', 'city_id'], filter = eq_filter, fetch_data = False)

        eq_filter = LessThanOrEqualTo(ValueRef('public.gis_block/id'), Literal(660000624))
        megdata.get_feature(['public.gis_block'], ['a'], ['id', 'district_id', 'city_id'], filter = eq_filter, fetch_data = False)

        eq_filter = GreaterThanOrEqualTo(ValueRef('public.gis_block/id'), Literal(660000624))
        megdata.get_feature(['public.gis_block'], ['a'], ['id', 'district_id', 'city_id'], filter = eq_filter, fetch_data = False)

        eq_filter = Like(ValueRef('public.gis_block/tags'), Literal(''))
        megdata.get_feature(['public.gis_block'], ['a'], ['id', 'district_id', 'city_id'], filter = eq_filter, fetch_data = False)

        eq_filter = Null(ValueRef('public.gis_block/id'))
        megdata.get_feature(['public.gis_block'], ['a'], ['id', 'district_id', 'city_id'], filter = eq_filter, fetch_data = False)

        eq_filter = Not(Null(ValueRef('public.gis_block/id')))
        megdata.get_feature(['public.gis_block'], ['a'], ['id', 'district_id', 'city_id'], filter = eq_filter, fetch_data = False)

        eq_filter = Not(LessThan(ValueRef('public.gis_block/id'), Literal(660000625)))
        megdata.get_feature(['public.gis_block'], ['a'], ['id', 'district_id', 'city_id'], filter = eq_filter, fetch_data = False)

        eq_filter = LessThan(Literal(660000624), Literal(660000625))
        megdata.get_feature(['public.gis_block'], ['a'], ['id', 'district_id', 'city_id'], filter = eq_filter, fetch_data = False)

        polygon = Wkt('SRID=4326;POLYGON((73.502355 3.83703,73.502355 53.563624,135.09567 53.563624,135.09567 3.83703,73.502355 3.83703))')
        eq_filter = ST_Equals(ValueRef('public.gis_block/geom'), polygon)
        megdata.get_feature(['public.gis_block'], ['a'], ['id', 'district_id', 'city_id'], filter = eq_filter, fetch_data = False)

        eq_filter = ST_Disjoint(ValueRef('public.gis_block/geom'), polygon)
        megdata.get_feature(['public.gis_block'], ['a'], ['id', 'district_id', 'city_id'], filter = eq_filter, fetch_data = False)

        eq_filter = ST_Touches(ValueRef('public.gis_block/geom'), polygon)
        megdata.get_feature(['public.gis_block'], ['a'], ['id', 'district_id', 'city_id'], filter = eq_filter, fetch_data = False)

        eq_filter = ST_Within(ValueRef('public.gis_block/geom'), polygon)
        megdata.get_feature(['public.gis_block'], ['a'], ['id', 'district_id', 'city_id'], filter = eq_filter, fetch_data = False)

        eq_filter = ST_Overlaps(ValueRef('public.gis_block/geom'), polygon)
        megdata.get_feature(['public.gis_block'], ['a'], ['id', 'district_id', 'city_id'], filter = eq_filter, fetch_data = False)

        eq_filter = ST_Crosses(ValueRef('public.gis_block/geom'), polygon)
        megdata.get_feature(['public.gis_block'], ['a'], ['id', 'district_id', 'city_id'], filter = eq_filter, fetch_data = False)

        eq_filter = ST_Intersects(ValueRef('public.gis_block/geom'), polygon)
        megdata.get_feature(['public.gis_block'], ['a'], ['id', 'district_id', 'city_id'], filter = eq_filter, fetch_data = False)

        eq_filter = ST_Contains(ValueRef('public.gis_block/geom'), polygon)
        megdata.get_feature(['public.gis_block'], ['a'], ['id', 'district_id', 'city_id'], filter = eq_filter, fetch_data = False)

        eq_filter = ST_DWithin(ValueRef('public.gis_block/geom'), polygon, Literal(100))
        megdata.get_feature(['public.gis_block'], ['a'], ['id', 'district_id', 'city_id'], filter = eq_filter, fetch_data = False)

        eq_filter = ST_Contains(ValueRef('public.city_boundary/boundary'), polygon)
        megdata.get_feature(['public.gis_block', 'public.city_boundary'], projection = [['id', 'geom'], ['id', 'boundary']], filter = eq_filter, fetch_data = False)
    
    def test_pack_feature(self):
        cfg = Configuration(join(dirname(__file__), 'config.yaml'))
        megdata = MegDataSource(cfg = cfg)
        eq_filter = NotEqualTo(ValueRef('public.gis_block/id'), Literal(660000625))
        data = megdata.get_feature(['public.gis_block'], ['a'], ['id', 'geom', 'district_id', 'city_id'], filter = eq_filter)
        leaflet.map(data, 'output.html')

    def test_function(self):
        cfg = Configuration(join(dirname(__file__), 'config.yaml'))
        megdata = MegDataSource(cfg = cfg)

        # abs, degress, acos, exp, asin, floor, sign, atan
        # log, sin, atn2, log10, sqrt, ceiling, pi, square,
        # cos, power, tan, cot, radians
        f = Function('abs', [Literal(-1)])
        print(megdata.get_feature(['public.gis_block'], None, [f]))

        f = Function('degrees', [Literal(-1)])
        print(megdata.get_feature(['public.gis_block'], None, [f]))

        f = Function('acos', [Literal(-1)])
        print(megdata.get_feature(['public.gis_block'], None, [f]))

        f = Function('exp', [Literal(-1)])
        print(megdata.get_feature(['public.gis_block'], None, [f]))

        f = Function('asin', [Literal(-1)])
        print(megdata.get_feature(['public.gis_block'], None, [f]))

        f = Function('floor', [Literal(-1)])
        print(megdata.get_feature(['public.gis_block'], None, [f]))

        f = Function('sign', [Literal(-1)])
        print(megdata.get_feature(['public.gis_block'], None, [f]))

        f = Function('atan', [Literal(-1)])
        print(megdata.get_feature(['public.gis_block'], None, [f]))

        f = Function('log', [Literal(1)])
        print(megdata.get_feature(['public.gis_block'], None, [f]))

        f = Function('sin', [Literal(-1)])
        print(megdata.get_feature(['public.gis_block'], None, [f]))

        f = Function('sqrt', [Literal(1)])
        print(megdata.get_feature(['public.gis_block'], None, [f]))

        f = Function('ceiling', [Literal(-1)])
        print(megdata.get_feature(['public.gis_block'], None, [f]))

        f = Function('cos', [Literal(-1)])
        print(megdata.get_feature(['public.gis_block'], None, [f]))

        f = Function('power', [Literal(-1), Literal(2)])
        print(megdata.get_feature(['public.gis_block'], None, [f]))

        f = Function('tan', [Literal(-1)])
        print(megdata.get_feature(['public.gis_block'], None, [f]))

        f = Function('cot', [Literal(-1)])
        print(megdata.get_feature(['public.gis_block'], None, [f]))

        f = Function('radians', [Literal(-1)])
        print('radians', megdata.get_feature(['public.gis_block'], None, [f]))

    def test_function_in_where(self):
        cfg = Configuration(join(dirname(__file__), 'config.yaml'))
        megdata = MegDataSource(cfg = cfg)

        f = EqualTo(ValueRef('public.gis_block/id'), Function('radians', [Literal(-1)]))
        print(megdata.get_feature(['public.gis_block'], None, filter = f, fetch_data = False))
    
    def test_sort_by(self):
        cfg = Configuration(join(dirname(__file__), 'config.yaml'))
        megdata = MegDataSource(cfg = cfg)
        f = EqualTo(ValueRef('public.gis_block/id'), Function('radians', [Literal(-1)]))
        print('sort_by', megdata.get_feature(['public.gis_block'], None, filter = f, sort_by = ValueRef('public.gis_block/id'), fetch_data = False))
        print('sort_by', megdata.get_feature(['public.gis_block'], None, filter = f, sort_by = (ValueRef('public.gis_block/id'), 'desc'), fetch_data = False))
        print('sort_by', megdata.get_feature(['public.gis_block'], None, filter = f, sort_by = [(ValueRef('public.gis_block/id'), 'desc'), ValueRef('public.gis_block/geom')], fetch_data = False))

    def test_paginate(self):
        cfg = Configuration(join(dirname(__file__), 'config.yaml'))
        megdata = MegDataSource(cfg = cfg)

        f = Or([EqualTo(ValueRef('public.gis_block/id'), Literal(660000625)),
            EqualTo(ValueRef('public.gis_block/id'), Literal(660000624))])

        print('paginate', megdata.get_feature(['public.gis_block'], None, page_count = 20, filter = f))

if __name__ == '__main__':
    unittest.main()