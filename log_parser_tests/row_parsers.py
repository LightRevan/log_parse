# -*- coding: utf-8 -*-
__author__ = 'lightrevan'

import unittest
from log_parser.row_parsers import *

# TODO: add full test for all combinations of row parsers and row getters
# TODO: add tests for match not in first row


class MergingGetterSingleParserTestCase(unittest.TestCase):
    def setUp(self):
        self.row_parser = SinglePatternRowParser('a', '^(?P<timestamp>\d+) (?P<thread>T\d+)')

    def test_1(self):
        rows = ['1 T1 a',
                '2 T1 b',
                '3 T1 a']
        tested = MergingRowGetter(iter(rows), self.row_parser)

        result = [row for row in tested]
        required_result = [('1 T1 a', {'timestamp': '1', 'thread': 'T1', 'match': 'a'}),
                           ('2 T1 b', {'timestamp': '2', 'thread': 'T1', 'match': None}),
                           ('3 T1 a', {'timestamp': '3', 'thread': 'T1', 'match': 'a'})]
        self.assertEqual(result, required_result)

    def test_2(self):
        rows = ['bbb',
                '1 T1 a',
                '2 T1 a',
                'cdf',
                '3 T1 a']
        tested = MergingRowGetter(iter(rows), self.row_parser)

        result = [row for row, _ in tested]
        self.assertEqual(result, ['bbb\n1 T1 a', '2 T1 a\ncdf', '3 T1 a'])

    def test_3(self):
        rows = ['bbb',
                '1 T1 a',
                'cdf',
                '3 T1 a']
        tested = MergingRowGetter(iter(rows), self.row_parser)

        result = [row for row, _ in tested]
        self.assertEqual(result, ['bbb\n1 T1 a\ncdf', '3 T1 a'])

    def test_4(self):
        rows = ['1 T1 a',
                'cdf',
                '2 T1 b',
                'acdf']
        tested = MergingRowGetter(iter(rows), self.row_parser)

        result = [row for row, _ in tested]
        self.assertEqual(result, ['1 T1 a\ncdf', '2 T1 b\nacdf'])

class MergingGetterMultiParserTestCase(unittest.TestCase):
    def setUp(self):
        self.row_parser = MultiPatternRowParser('a', timestamp='^\d+', thread='T\d+')

    def test_1(self):
        rows = ['1 T1 a',
                '2 T1 b',
                '3 T1 a']
        tested = MergingRowGetter(iter(rows), self.row_parser)

        result = [row for row in tested]
        required_result = [('1 T1 a', {'timestamp': '1', 'thread': 'T1', 'match': 'a'}),
                           ('2 T1 b', {'timestamp': '2', 'thread': 'T1', 'match': None}),
                           ('3 T1 a', {'timestamp': '3', 'thread': 'T1', 'match': 'a'})]
        self.assertEqual(result, required_result)

    def test_2(self):
        rows = ['1 T1 a',
                '2 T1 a',
                'cdf',
                '3 T1 a']
        tested = MergingRowGetter(iter(rows), self.row_parser)

        result = [row for row, _ in tested]
        self.assertEqual(result, ['1 T1 a', '2 T1 a\ncdf', '3 T1 a'])


class SinglePatternParserTestCase(unittest.TestCase):
    def setUp(self):
        self.tested = SinglePatternRowParser('a', '^(?P<timestamp>\d+) (?P<thread>T\d+)')

    def test_1(self):
        result = self.tested.parse_row('1 T1 a')
        required_result = {'match': 'a',
                           'timestamp': '1',
                           'thread': 'T1'}
        self.assertEqual(result, required_result)

    def test_2(self):
        result = self.tested.parse_row('1 T1 b')
        required_result = {'match': None,
                           'timestamp': '1',
                           'thread': 'T1'}
        self.assertEqual(result, required_result)

    def test_3(self):
        with self.assertRaises(RowParsingError):
            self.tested.parse_row('abc')


class MultiPatternParserTestCase(unittest.TestCase):
    def setUp(self):
        self.tested = MultiPatternRowParser('a', timestamp='^\d+', thread='T\d+')

    def test_1(self):
        result = self.tested.parse_row('1 T1 a')
        required_result = {'match': 'a',
                           'timestamp': '1',
                           'thread': 'T1'}
        self.assertEqual(result, required_result)

    def test_2(self):
        result = self.tested.parse_row('1 T1 b')
        required_result = {'match': None,
                           'timestamp': '1',
                           'thread': 'T1'}
        self.assertEqual(result, required_result)

    def test_3(self):
        with self.assertRaises(RowParsingError):
            self.tested.parse_row('abc')


if __name__ == '__main__':
    unittest.main()
