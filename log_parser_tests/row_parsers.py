# -*- coding: utf-8 -*-
__author__ = 'lightrevan'

import unittest
from log_parser.row_parsers import *

# TODO: add full test for all combinations of row parsers and row getters
# TODO: add tests for match not in first row


class MergingRowGetterTestCase(unittest.TestCase):
    def test_1(self):
        row_parser = MultiPatternRowParser('.*', timestamp='^\d+')
        rows = ['2 a',
                'cdf']
        tested = MergingRowGetter(iter(rows), row_parser)

        result = [row for row, _ in tested]
        self.assertEqual(result, ['2 a\ncdf'])

    def test_2(self):
        row_parser = MultiPatternRowParser('.*', timestamp='^\d+')
        rows = ['1 a',
                '2 a',
                'cdf',
                '3 a']
        tested = MergingRowGetter(iter(rows), row_parser)

        result = [row for row, _ in tested]
        self.assertEqual(result, ['1 a', '2 a\ncdf', '3 a'])


class SinglePatternParserTestCase(unittest.TestCase):
    def test_1(self):
        tested = SinglePatternRowParser('a', '^(?P<timestamp>\d+) (?P<thread>T\d+)')
        result = tested.parse_row('1 T1 a')
        required_result = {'match': 'a',
                           'timestamp': '1',
                           'thread': 'T1'}
        self.assertEqual(result, required_result)

    def test_2(self):
        row_parser = SinglePatternRowParser('a', '^(?P<timestamp>\d+) (?P<thread>T\d+)')
        rows = ['bbb',
                '1 T1 a',
                '2 T1 a',
                'cdf',
                '3 T1 a']
        tested = MergingRowGetter(iter(rows), row_parser)

        result = [row for row, _ in tested]
        self.assertEqual(result, ['bbb\n1 T1 a', '2 T1 a\ncdf', '3 T1 a'])

    def test_3(self):
        row_parser = SinglePatternRowParser('a', '^(?P<timestamp>\d+) (?P<thread>T\d+)')
        rows = ['bbb',
                '1 T1 a',
                'cdf',
                '3 T1 a']
        tested = MergingRowGetter(iter(rows), row_parser)

        result = [row for row, _ in tested]
        self.assertEqual(result, ['bbb\n1 T1 a\ncdf', '3 T1 a'])

    def test_4(self):
        row_parser = SinglePatternRowParser('a', '^(?P<timestamp>\d+) (?P<thread>T\d+)')
        rows = ['1 T1 a',
                'cdf',
                '2 T1 b',
                'acdf']
        tested = MergingRowGetter(iter(rows), row_parser)

        result = [row for row, _ in tested]
        self.assertEqual(result, ['1 T1 a\ncdf', '2 T1 b\nacdf'])


if __name__ == '__main__':
    unittest.main()
