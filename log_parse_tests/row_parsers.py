# -*- coding: utf-8 -*-
__author__ = 'lightrevan'

import unittest
from log_parse.row_parsers import *


class MergingRowGetterTestCase(unittest.TestCase):
    def test_1(self):
        row_parser = UniversalRowParser('.*', timestamp='^\d+')
        rows = ['2 a',
                'cdf']
        tested = MergingRowGetter(iter(rows), row_parser)

        result = [row for row, _ in tested]
        self.assertEqual(result, ['2 a\ncdf'])

    def test_2(self):
        row_parser = UniversalRowParser('.*', timestamp='^\d+')
        rows = ['1 a',
                '2 a',
                'cdf',
                '3 a']
        tested = MergingRowGetter(iter(rows), row_parser)

        result = [row for row, _ in tested]
        self.assertEqual(result, ['1 a', '2 a\ncdf', '3 a'])


class SinglePatternThreadParserTestCase(unittest.TestCase):
    def test_1(self):
        tested = SinglePatternThreadParser('a', '^(\d+) (T\d+)')
        result = tested.parse_row('1 T1 a')
        required_result = {'match': 'a',
                           'timestamp': '1',
                           'thread': 'T1'}
        self.assertEqual(result, required_result)


if __name__ == '__main__':
    unittest.main()
