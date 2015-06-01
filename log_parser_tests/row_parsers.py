# -*- coding: utf-8 -*-
__author__ = 'lightrevan'

import unittest
from log_parser.row_parsers import *


class MergingGetterAbstractParserTestCase(object):
    def test_1(self):
        rows = ['1 T1 a',
                '2 T1 b',
                '3 T1 a']
        tested = self.getter_cls(iter(rows), self.row_parser)

        result = [row for row in tested]
        required_result = [('1 T1 a', {'timestamp': '1', 'thread': 'T1', 'match': 'a'}),
                           ('2 T1 b', {'timestamp': '2', 'thread': 'T1', 'match': None}),
                           ('3 T1 a', {'timestamp': '3', 'thread': 'T1', 'match': 'a'})]
        self.assertEqual(result, required_result)

    def test_2(self):
        rows = ['bbb',
                '1 T1 a',
                '2 T1 b',
                'cdf',
                '3 T1 a']
        tested = self.getter_cls(iter(rows), self.row_parser)

        result = [row for row in tested]
        required_result = [('bbb\n1 T1 a', {'timestamp': '1', 'thread': 'T1', 'match': 'a'}),
                           ('2 T1 b\ncdf', {'timestamp': '2', 'thread': 'T1', 'match': None}),
                           ('3 T1 a', {'timestamp': '3', 'thread': 'T1', 'match': 'a'})]
        self.assertEqual(result, required_result)

    def test_3(self):
        rows = ['bbb',
                '1 T1 a',
                'cdf',
                '3 T1 b']
        tested = self.getter_cls(iter(rows), self.row_parser)

        result = [row for row in tested]
        required_result = [('bbb\n1 T1 a\ncdf', {'timestamp': '1', 'thread': 'T1', 'match': 'a'}),
                           ('3 T1 b', {'timestamp': '3', 'thread': 'T1', 'match': None})]
        self.assertEqual(result, required_result)

    def test_4(self):
        rows = ['1 T1 a',
                'cdf',
                '2 T1 b',
                'cdf']
        tested = self.getter_cls(iter(rows), self.row_parser)

        result = [row for row in tested]
        required_result = [('1 T1 a\ncdf', {'timestamp': '1', 'thread': 'T1', 'match': 'a'}),
                           ('2 T1 b\ncdf', {'timestamp': '2', 'thread': 'T1', 'match': None})]
        self.assertEqual(result, required_result)

    def test_5(self):
        rows = ['1 T1 b',
                'cdf',
                'aaa']
        tested = self.getter_cls(iter(rows), self.row_parser)

        result = [row for row in tested]
        required_result = [('1 T1 b\ncdf\naaa', {'timestamp': '1', 'thread': 'T1', 'match': 'a'})]
        self.assertEqual(result, required_result)

    def test_6(self):
        rows = ['bbb',
                'aaa',
                '1 T1 b']
        tested = self.getter_cls(iter(rows), self.row_parser)

        result = [row for row in tested]
        required_result = [('bbb\naaa\n1 T1 b', {'timestamp': '1', 'thread': 'T1', 'match': 'a'})]
        self.assertEqual(result, required_result)

class MergingGetterSingleParserTestCase(unittest.TestCase, MergingGetterAbstractParserTestCase):
    def setUp(self):
        self.row_parser = SinglePatternRowParser('a', '^(?P<timestamp>\d+) (?P<thread>T\d+)')
        self.getter_cls = MergingRowGetter


class MergingGetterMultiParserTestCase(unittest.TestCase, MergingGetterAbstractParserTestCase):
    def setUp(self):
        self.row_parser = MultiPatternRowParser('a', timestamp='^\d+', thread='T\d+')
        self.getter_cls = MergingRowGetter


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
