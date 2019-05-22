import unittest

from bayes.wfs.core import filter
from bayes.wfs.core.filter import *

class TestFilter(unittest.TestCase):

    def setUp(self):
        self.fes = {
            '@xmlns:fes': 'http://www.opengis.net/fes/2.0',
            '@xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            '@xsi:schemaLocation': 'http://www.opengis.net/fes/2.0 filterAll.xsd',
            'fes:And': {
                'fes:Or': [
                    {
                        'fes:PropertyIsEqualTo': [
                            {'fes:ValueReference': 'FIELD1', 'fes:Literal': None},
                            {'fes:ValueReference': 'FIELD2', 'fes:Literal': None}
                        ]
                    }
                ],
                'fes:PropertyIsEqualTo': [
                    {'fes:ValueReference': 'STATUS', 'fes:Literal': None},
                    {'fes:ValueReference': 'STATUS1', 'fes:Literal': None}
                ]
            }
        }
        return super().setUp()

    def test_parse_fes(self):
        filter.parse_fes('fes:And', self.fes['fes:And'])

    def test_value_ref(self):
        value_ref = {
            'fes:ValueReference': 'test'
        }
        self.assertIsInstance(filter.parse_fes('fes:ValueReference', value_ref['fes:ValueReference']), ValueRef)

    def test_value_ref(self):
        value_ref = {
            'fes:Literal': 1
        }
        out = filter.parse_fes('fes:Literal', value_ref['fes:Literal'])
        self.assertIsInstance(out, Literal)
        self.assertEqual(out.val, 1)

    def test_function(self):
        value_ref_except = {
            'fes:Function': {
                'params': {
                    'fes:ValueReference': 'PROPB',
                    'fes:Literal': 100
                }
            }
        }

        value_ref = {
            'fes:Function': {
                "name": 'Add',
                'params': {
                    'fes:ValueReference': 'PROPB',
                    'fes:Literal': 100
                }
            }
        }
        out = filter.parse_fes('fes:Function', value_ref['fes:Function'])
        self.assertIsInstance(out, Function)
        self.assertEqual(out.func, 'Add')
        self.assertRaises(InvalidFilter, filter.parse_fes, 'fes:Function', value_ref_except['fes:Function'])

        self.assertIsInstance(out.args[0], ValueRef)
        self.assertIsInstance(out.args[1], Literal)

    def test_not(self):
        value_ref = {
            'fes:Literal': True,
            'fes:Literal2': True,
        }
        out = filter.parse_fes('fes:Not', {
            'fes:Literal': True,
        })
        self.assertIsInstance(out, Not)
        self.assertEqual(out.item.val, True)

        self.assertRaises(InvalidFilter, filter.parse_fes, 'fes:Not', {
            'fes:ValueReference': 'PROPB',
            'fes:Literal': True,
        })
    
    def test_equal_to(self):
        value_ref = [{'fes:ValueReference': 'test/id', 'fes:Literal': True}]
        self.assertRaises(InvalidFilter, filter.parse_fes, 'fes:PropertyIsEqualTo', {
            'fes:Literal': True,
        })

        out = filter.parse_fes('fes:PropertyIsEqualTo', value_ref)
        self.assertIsInstance(out, EqualTo)
        self.assertEqual(out.val1.name, 'id')
        self.assertEqual(out.val2.val, True)

    def test_not_equal_to(self):
        value_ref = [{'fes:ValueReference': 'test/id', 'fes:Literal': True}]
        self.assertRaises(InvalidFilter, filter.parse_fes, 'fes:PropertyIsNotEqualTo', {
            'fes:Literal': True,
        })

        out = filter.parse_fes('fes:PropertyIsNotEqualTo', value_ref)
        self.assertIsInstance(out, NotEqualTo)
        self.assertEqual(out.val1.name, 'id')
        self.assertEqual(out.val2.val, True)

    def test_null(self):
        value_ref = {'fes:ValueReference': 'test/id'}
        self.assertRaises(InvalidFilter, filter.parse_fes, 'fes:PropertyIsNull', {
            'fes:Literal': True,
            'fes:xxx': False
        })

        out = filter.parse_fes('fes:PropertyIsNull', value_ref)
        self.assertIsInstance(out, Null)
        self.assertEqual(out.item.name, 'id')

    def test_between(self):
        value_ref = {'fes:ValueReference': 'Test', 
            'fes:LowerBoundary': {
                'fes:Literal': 10
            },
            'fes:UpperBoundary': {
                'fes:Literal': 20
            }
        }
        out = filter.parse_fes('fes:PropertyIsBetween', value_ref)
        self.assertIsInstance(out, Between)
        self.assertEqual(out.lower.val, 10)
        self.assertEqual(out.upper.val, 20)

    def test_spatial(self):
        value_ref = [{'fes:ValueReference': 'Test'},
                {'fes:ValueReference': 'Test2'}]

        out = filter.parse_fes('fes:Equals', value_ref)
        self.assertIsInstance(out, ST_Equals)
        self.assertEqual(out.geom1.name, 'Test')
        self.assertEqual(out.geom2.name, 'Test2')

    def test_dwithin(self):
        value_ref = {
            'fes:Distance': {'fes:ValueReference': 'Test'},
            'fes:Geoms': [{'fes:ValueReference': 'Test'},
                {'fes:ValueReference': 'Test2'}]
        }

        out = filter.parse_fes('fes:DWithin', value_ref)
        self.assertIsInstance(out, ST_DWithin)
        self.assertEqual(out.geom1.name, 'Test')
        self.assertEqual(out.geom2.name, 'Test2')
        self.assertEqual(out.distance.name, 'Test')

if __name__ == '__main__':
    unittest.main()