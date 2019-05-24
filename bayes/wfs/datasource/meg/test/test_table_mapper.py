import unittest

from bayes.wfs.datasource.meg.filter import TableMapper, TableNotFound

class TestTableMapper(unittest.TestCase):
    def test_table_mapper(self):
        mapper = TableMapper(
            ['a', 'b', 'c', 'd'],
            ['table1', 'table2', 'table3', 'table4'],
            ['t1', 't2', 't3', 't4']
        )

        self.assertEqual(mapper.get_table('table1'), 'a')
        self.assertEqual(mapper.get_table('table2'), 'b')
        self.assertEqual(mapper.get_table('table3'), 'c')
        self.assertEqual(mapper.get_table('table4'), 'd')
        self.assertEqual(mapper.get_table('t1'), 'a')
        self.assertEqual(mapper.get_table('t2'), 'b')
        self.assertEqual(mapper.get_table('t3'), 'c')
        self.assertEqual(mapper.get_table('t4'), 'd')

        self.assertRaises(TableNotFound, mapper.get_table, 'table6')
        self.assertRaises(TableNotFound, mapper.get_table, 't6')

        mapper = TableMapper(
            ['1'], ['table1'], ['t1']
        )
        self.assertEqual(mapper.get_table(None), '1')
        self.assertEqual(mapper.get_table('table1'), '1')
        self.assertEqual(mapper.get_table('t1'), '1')


if __name__ == '__main__':
    unittest.main()