# -*- coding: utf-8 -*-
__author__ = 'lightrevan'

import unittest
import tempfile
import os
import re

from log_parser.file_parsers import *
from log_parser.row_parsers import *
from log_parser_tests.mocks_and_stubs import *


class SingleLineFileParserTest(unittest.TestCase):
    def setUp(self):
        data = [('1 a', {'timestamp': 1, 'match': None}),
                 ('2 b', {'timestamp': 2, 'match': None}),
                 ('3 c', {'timestamp': 3, 'match': None}),
                 ('4 d', {'timestamp': 4, 'match': None}),
                 ('5 abcd', {'timestamp': 5, 'match': 'abcd'}),
                 ('6 e', {'timestamp': 6, 'match': None}),
                 ('7 f', {'timestamp': 7, 'match': None}),
                 ('8 abcd', {'timestamp': 8, 'match': 'abcd'}),
                 ('9 a', {'timestamp': 9, 'match': None}),
                 ('10 a', {'timestamp': 10, 'match': None}),
                 ('11 a', {'timestamp': 11, 'match': None}),
                 ('12 a', {'timestamp': 12, 'match': None}),
                 ('13 a', {'timestamp': 13, 'match': None}),
                 ('14 a', {'timestamp': 14, 'match': None}),
                 ('15 a', {'timestamp': 15, 'match': None}),
                 ('16 abcd', {'timestamp': 16, 'match': 'abcd'}),
                 ('17 a', {'timestamp': 17, 'match': None})]

        self.tested = SingleLineFileParser(RowGetterStub(data))

    def test_parsing(self):
        results = [(row_params['timestamp'], row) for row, row_params in self.tested]
        required_results = [(5, '5 abcd'),
                            (8, '8 abcd'),
                            (16, '16 abcd')]

        self.assertEqual(results, required_results)


class ContextFileParserTest(unittest.TestCase):
    def setUp(self):
        data = [('1 a', {'timestamp': 1, 'match': None}),
                 ('2 b', {'timestamp': 2, 'match': None}),
                 ('3 c', {'timestamp': 3, 'match': None}),
                 ('4 d', {'timestamp': 4, 'match': None}),
                 ('5 abcd', {'timestamp': 5, 'match': 'abcd'}),
                 ('6 e', {'timestamp': 6, 'match': None}),
                 ('7 f', {'timestamp': 7, 'match': None}),
                 ('8 abcd', {'timestamp': 8, 'match': 'abcd'}),
                 ('9 a', {'timestamp': 9, 'match': None}),
                 ('10 a', {'timestamp': 10, 'match': None}),
                 ('11 a', {'timestamp': 11, 'match': None}),
                 ('12 a', {'timestamp': 12, 'match': None}),
                 ('13 a', {'timestamp': 13, 'match': None}),
                 ('14 a', {'timestamp': 14, 'match': None}),
                 ('15 a', {'timestamp': 15, 'match': None}),
                 ('16 abcd', {'timestamp': 16, 'match': 'abcd'}),
                 ('17 a', {'timestamp': 17, 'match': None}),
                 ('18 a', {'timestamp': 18, 'match': None})]

        self.tested = SimpleContextFileParser(RowGetterStub(data), context_size=3)

    def test_parsing_c1(self):
        self.tested.set_context_size(1)
        results = [(row_params['timestamp'], row) for row, row_params in self.tested]
        required_results = [(4, '4 d'),
                            (5, '5 abcd'),
                            (6, '6 e'),
                            (7, '7 f'),
                            (8, '8 abcd'),
                            (9, '9 a'),
                            (15, '15 a'),
                            (16, '16 abcd'),
                            (17, '17 a')]

        self.assertEqual(results, required_results)

    def test_parsing_c2(self):
        self.tested.set_context_size(2)
        results = [(row_params['timestamp'], row) for row, row_params in self.tested]
        required_results = [(3, '3 c'),
                            (4, '4 d'),
                            (5, '5 abcd'),
                            (6, '6 e'),
                            (7, '7 f'),
                            (8, '8 abcd'),
                            (9, '9 a'),
                            (10, '10 a'),
                            (14, '14 a'),
                            (15, '15 a'),
                            (16, '16 abcd'),
                            (17, '17 a'),
                            (18, '18 a')]

        self.assertEqual(results, required_results)

    def test_parsing_c3(self):
        results = [(row_params['timestamp'], row) for row, row_params in self.tested]
        required_results = [(2, '2 b'),
                            (3, '3 c'),
                            (4, '4 d'),
                            (5, '5 abcd'),
                            (6, '6 e'),
                            (7, '7 f'),
                            (8, '8 abcd'),
                            (9, '9 a'),
                            (10, '10 a'),
                            (11, '11 a'),
                            (13, '13 a'),
                            (14, '14 a'),
                            (15, '15 a'),
                            (16, '16 abcd'),
                            (17, '17 a'),
                            (18, '18 a')]

        self.assertEqual(results, required_results)


class ContextFileParserTestShortFile(unittest.TestCase):
    def setUp(self):
        data = [('1 a', {'timestamp': 1, 'match': None}),
                 ('2 b', {'timestamp': 2, 'match': None}),
                 ('3 c', {'timestamp': 3, 'match': None}),
                 ('4 d', {'timestamp': 4, 'match': None}),
                 ('5 abcd', {'timestamp': 5, 'match': 'abcd'}),
                 ('6 e', {'timestamp': 6, 'match': None}),
                 ('7 f', {'timestamp': 7, 'match': None}),
                 ('8 abcd', {'timestamp': 8, 'match': 'abcd'}),
                 ('9 a', {'timestamp': 9, 'match': None}),
                 ('10 a', {'timestamp': 10, 'match': None}),
                 ('11 a', {'timestamp': 11, 'match': None}),
                 ('12 a', {'timestamp': 12, 'match': None}),
                 ('13 a', {'timestamp': 13, 'match': None}),
                 ('14 a', {'timestamp': 14, 'match': None}),
                 ('15 a', {'timestamp': 15, 'match': None}),
                 ('16 abcd', {'timestamp': 16, 'match': 'abcd'})]

        self.tested = SimpleContextFileParser(RowGetterStub(data), context_size=3)

    def test_parsing_c1(self):
        self.tested.set_context_size(1)
        results = [(row_params['timestamp'], row) for row, row_params in self.tested]
        required_results = [(4, '4 d'),
                            (5, '5 abcd'),
                            (6, '6 e'),
                            (7, '7 f'),
                            (8, '8 abcd'),
                            (9, '9 a'),
                            (15, '15 a'),
                            (16, '16 abcd')]

        self.assertEqual(results, required_results)

    def test_parsing_c2(self):
        self.tested.set_context_size(2)
        results = [(row_params['timestamp'], row) for row, row_params in self.tested]
        required_results = [(3, '3 c'),
                            (4, '4 d'),
                            (5, '5 abcd'),
                            (6, '6 e'),
                            (7, '7 f'),
                            (8, '8 abcd'),
                            (9, '9 a'),
                            (10, '10 a'),
                            (14, '14 a'),
                            (15, '15 a'),
                            (16, '16 abcd')]

        self.assertEqual(results, required_results)

    def test_parsing_c3(self):
        results = [(row_params['timestamp'], row) for row, row_params in self.tested]
        required_results = [(2, '2 b'),
                            (3, '3 c'),
                            (4, '4 d'),
                            (5, '5 abcd'),
                            (6, '6 e'),
                            (7, '7 f'),
                            (8, '8 abcd'),
                            (9, '9 a'),
                            (10, '10 a'),
                            (11, '11 a'),
                            (13, '13 a'),
                            (14, '14 a'),
                            (15, '15 a'),
                            (16, '16 abcd')]

        self.assertEqual(results, required_results)


class ThreadCommonBufferParserTest(unittest.TestCase):
    def setUp(self):
        data = [('1 T1 a', {'timestamp': 1, 'match': None, 'thread': 'T1'}),
                 ('2 T1 b', {'timestamp': 2, 'match': None, 'thread': 'T1'}),
                 ('3 T2 c', {'timestamp': 3, 'match': None, 'thread': 'T2'}),
                 ('4 T2 d', {'timestamp': 4, 'match': None, 'thread': 'T2'}),
                 ('5 T1 abcd', {'timestamp': 5, 'match': 'abcd', 'thread': 'T1'}),
                 ('6 T1 e', {'timestamp': 6, 'match': None, 'thread': 'T1'}),
                 ('7 T2 f', {'timestamp': 7, 'match': None, 'thread': 'T2'}),
                 ('8 T2 a', {'timestamp': 8, 'match': None, 'thread': 'T2'}),
                 ('9 T2 a', {'timestamp': 9, 'match': None, 'thread': 'T2'}),
                 ('10 T1 a', {'timestamp': 10, 'match': None, 'thread': 'T1'}),
                 ('11 T2 abcd', {'timestamp': 11, 'match': 'abcd', 'thread': 'T2'})]

        self.tested = ThreadContextCommonBufferFileParser(RowGetterStub(data), context_size=3)

    def test_parsing_c3(self):
        self.tested.set_context_size(3)
        results = [(row_params['timestamp'], row) for row, row_params in self.tested]
        required_results = [(2, '2 T1 b'),
                            (5, '5 T1 abcd'),
                            (6, '6 T1 e'),
                            (8, '8 T2 a'),
                            (9, '9 T2 a'),
                            (11, '11 T2 abcd')]

        self.assertEqual(results, required_results)

    def test_parsing_c4(self):
        self.tested.set_context_size(4)
        results = [(row_params['timestamp'], row) for row, row_params in self.tested]
        required_results = [(1, '1 T1 a'),
                            (2, '2 T1 b'),
                            (5, '5 T1 abcd'),
                            (6, '6 T1 e'),
                            (7, '7 T2 f'),
                            (8, '8 T2 a'),
                            (9, '9 T2 a'),
                            (11, '11 T2 abcd')]

        self.assertEqual(results, required_results)

    def test_parsing_c5(self):
        self.tested.set_context_size(5)
        results = [(row_params['timestamp'], row) for row, row_params in self.tested]
        required_results = [(1, '1 T1 a'),
                            (2, '2 T1 b'),
                            (5, '5 T1 abcd'),
                            (6, '6 T1 e'),
                            (7, '7 T2 f'),
                            (8, '8 T2 a'),
                            (9, '9 T2 a'),
                            (10, '10 T1 a'),
                            (11, '11 T2 abcd')]

        self.assertEqual(results, required_results)


class ThreadCommonBufferParserTestThickMatches(unittest.TestCase):
    def setUp(self):
        data = [('1 T1 a', {'timestamp': 1, 'match': None, 'thread': 'T1'}),
                ('2 T1 b', {'timestamp': 2, 'match': None, 'thread': 'T1'}),
                ('3 T1 c', {'timestamp': 3, 'match': None, 'thread': 'T1'}),
                ('4 T1 d', {'timestamp': 4, 'match': None, 'thread': 'T1'}),
                ('5 T1 abcd', {'timestamp': 5, 'match': 'abcd', 'thread': 'T1'}),
                ('6 T1 e', {'timestamp': 6, 'match': None, 'thread': 'T1'}),
                ('7 T1 abcd', {'timestamp': 7, 'match': 'abcd', 'thread': 'T1'}),
                ('8 T2 a', {'timestamp': 8, 'match': None, 'thread': 'T2'}),
                ('9 T2 a', {'timestamp': 9, 'match': None, 'thread': 'T2'}),
                ('10 T1 a', {'timestamp': 10, 'match': None, 'thread': 'T1'}),
                ('11 T2 abcd', {'timestamp': 11, 'match': 'abcd', 'thread': 'T2'})]

        self.tested = ThreadContextCommonBufferFileParser(RowGetterStub(data), context_size=3)

    def test_parsing_c3(self):
        self.tested.set_context_size(3)
        results = [(row_params['timestamp'], row) for row, row_params in self.tested]
        required_results = [(2, '2 T1 b'),
                            (3, '3 T1 c'),
                            (4, '4 T1 d'),
                            (5, '5 T1 abcd'),
                            (6, '6 T1 e'),
                            (7, '7 T1 abcd'),
                            (8, '8 T2 a'),
                            (9, '9 T2 a'),
                            (10, '10 T1 a'),
                            (11, '11 T2 abcd')]

        self.assertEqual(results, required_results)

    def test_parsing_c4(self):
        self.tested.set_context_size(4)
        results = [(row_params['timestamp'], row) for row, row_params in self.tested]
        required_results = [(1, '1 T1 a'),
                            (2, '2 T1 b'),
                            (3, '3 T1 c'),
                            (4, '4 T1 d'),
                            (5, '5 T1 abcd'),
                            (6, '6 T1 e'),
                            (7, '7 T1 abcd'),
                            (8, '8 T2 a'),
                            (9, '9 T2 a'),
                            (10, '10 T1 a'),
                            (11, '11 T2 abcd')]

        self.assertEqual(results, required_results)

    def test_parsing_c5(self):
        self.tested.set_context_size(5)
        results = [(row_params['timestamp'], row) for row, row_params in self.tested]
        required_results = [(1, '1 T1 a'),
                            (2, '2 T1 b'),
                            (3, '3 T1 c'),
                            (4, '4 T1 d'),
                            (5, '5 T1 abcd'),
                            (6, '6 T1 e'),
                            (7, '7 T1 abcd'),
                            (8, '8 T2 a'),
                            (9, '9 T2 a'),
                            (10, '10 T1 a'),
                            (11, '11 T2 abcd')]

        self.assertEqual(results, required_results)



class SingleThreadParserTest(unittest.TestCase):
    def setUp(self):
        data = [('1 T1 a', {'timestamp': 1, 'match': None, 'thread': 'T1'}),
                 ('2 T1 b', {'timestamp': 2, 'match': None, 'thread': 'T1'}),
                 ('4 T2 d', {'timestamp': 4, 'match': None, 'thread': 'T2'}),
                 ('5 T1 abcd', {'timestamp': 5, 'match': 'abcd', 'thread': 'T1'}),
                 ('6 T1 e', {'timestamp': 6, 'match': None, 'thread': 'T1'}),
                 ('7 T2 f', {'timestamp': 7, 'match': None, 'thread': 'T2'}),
                 ('7 T3 a', {'timestamp': 7, 'match': None, 'thread': 'T3'}),
                 ('7 T3 a', {'timestamp': 7, 'match': None, 'thread': 'T3'}),
                 ('7 T3 a', {'timestamp': 7, 'match': None, 'thread': 'T3'}),
                 ('8 T2 a', {'timestamp': 8, 'match': None, 'thread': 'T2'}),
                 ('9 T2 a', {'timestamp': 9, 'match': None, 'thread': 'T2'}),
                 ('10 T1 a', {'timestamp': 10, 'match': None, 'thread': 'T1'}),
                 ('11 T2 abcd', {'timestamp': 11, 'match': 'abcd', 'thread': 'T2'}),
                 ('12 T1 abcd', {'timestamp': 12, 'match': 'abcd', 'thread': 'T1'}),
                 ('13 T1 a', {'timestamp': 13, 'match': None, 'thread': 'T1'}),
                 ('14 T1 a', {'timestamp': 14, 'match': None, 'thread': 'T1'})]

        self.tested = SingleThreadContextFileParser(RowGetterStub(data), context_size=3)

    def test_parsing_c1(self):
        self.tested.set_context_size(1)
        results = [(row_params['timestamp'], row) for row, row_params in self.tested]
        required_results = [(5, '5 T1 abcd'),
                            (6, '6 T1 e'),
                            (10, '10 T1 a'),
                            (12, '12 T1 abcd'),
                            (13, '13 T1 a')]

        self.assertEqual(results, required_results)

    def test_parsing_c2(self):
        self.tested.set_context_size(2)
        results = [(row_params['timestamp'], row) for row, row_params in self.tested]
        required_results = [(2, '2 T1 b'),
                            (5, '5 T1 abcd'),
                            (6, '6 T1 e'),
                            (10, '10 T1 a'),
                            (12, '12 T1 abcd'),
                            (13, '13 T1 a'),
                            (14, '14 T1 a')]

        self.assertEqual(results, required_results)

    def test_parsing_c3(self):
        self.tested.set_context_size(3)
        results = [(row_params['timestamp'], row) for row, row_params in self.tested]
        required_results = [(1, '1 T1 a'),
                            (2, '2 T1 b'),
                            (5, '5 T1 abcd'),
                            (6, '6 T1 e'),
                            (10, '10 T1 a'),
                            (12, '12 T1 abcd'),
                            (13, '13 T1 a'),
                            (14, '14 T1 a')]

        self.assertEqual(results, required_results)


class MultiThreadParserTest(unittest.TestCase):
    def setUp(self):
        data = [('1 T1 a', {'timestamp': 1, 'match': None, 'thread': 'T1'}),
                 ('2 T1 b', {'timestamp': 2, 'match': None, 'thread': 'T1'}),
                 ('3 T2 c', {'timestamp': 3, 'match': None, 'thread': 'T2'}),
                 ('4 T2 d', {'timestamp': 4, 'match': None, 'thread': 'T2'}),
                 ('5 T1 abcd', {'timestamp': 5, 'match': 'abcd', 'thread': 'T1'}),
                 ('6 T2 abcd', {'timestamp': 6, 'match': 'abcd', 'thread': 'T2'}),
                 ('7 T3 a', {'timestamp': 7, 'match': None, 'thread': 'T3'}),
                 ('7 T3 a', {'timestamp': 7, 'match': None, 'thread': 'T3'}),
                 ('7 T3 a', {'timestamp': 7, 'match': None, 'thread': 'T3'}),
                 ('7 T2 f', {'timestamp': 7, 'match': None, 'thread': 'T2'}),
                 ('8 T2 a', {'timestamp': 8, 'match': None, 'thread': 'T2'}),
                 ('9 T2 a', {'timestamp': 9, 'match': None, 'thread': 'T2'}),
                 ('10 T1 a', {'timestamp': 10, 'match': None, 'thread': 'T1'}),
                 ('11 T2 abcd', {'timestamp': 11, 'match': 'abcd', 'thread': 'T2'})]

        self.tested = MultiThreadContextFileParser(RowGetterStub(data), context_size=3)

    def test_parsing_c1(self):
        self.tested.set_context_size(1)
        results = [(row_params['timestamp'], row) for row, row_params in self.tested]
        required_results = [(2, '2 T1 b'),
                            (4, '4 T2 d'),
                            (5, '5 T1 abcd'),
                            (6, '6 T2 abcd'),
                            (7, '7 T2 f'),
                            (10, '10 T1 a'),
                            (9, '9 T2 a'),
                            (11, '11 T2 abcd')]

        self.assertEqual(results, required_results)

    def test_parsing_c2(self):
        self.tested.set_context_size(2)
        results = [(row_params['timestamp'], row) for row, row_params in self.tested]
        required_results = [(1, '1 T1 a'),
                            (2, '2 T1 b'),
                            (3, '3 T2 c'),
                            (4, '4 T2 d'),
                            (5, '5 T1 abcd'),
                            (6, '6 T2 abcd'),
                            (7, '7 T2 f'),
                            (8, '8 T2 a'),
                            (10, '10 T1 a'),
                            (9, '9 T2 a'),
                            (11, '11 T2 abcd')]

        self.assertEqual(results, required_results)

    def test_parsing_c3(self):
        self.tested.set_context_size(3)
        results = [(row_params['timestamp'], row) for row, row_params in self.tested]
        required_results = [(1, '1 T1 a'),
                            (2, '2 T1 b'),
                            (3, '3 T2 c'),
                            (4, '4 T2 d'),
                            (5, '5 T1 abcd'),
                            (6, '6 T2 abcd'),
                            (7, '7 T2 f'),
                            (8, '8 T2 a'),
                            (9, '9 T2 a'),
                            (10, '10 T1 a'),
                            (11, '11 T2 abcd')]

        self.assertEqual(results, required_results)

    def test_parsing_c4(self):
        self.tested.set_context_size(4)
        results = [(row_params['timestamp'], row) for row, row_params in self.tested]
        required_results = [(1, '1 T1 a'),
                            (2, '2 T1 b'),
                            (3, '3 T2 c'),
                            (4, '4 T2 d'),
                            (5, '5 T1 abcd'),
                            (6, '6 T2 abcd'),
                            (7, '7 T2 f'),
                            (8, '8 T2 a'),
                            (9, '9 T2 a'),
                            (10, '10 T1 a'),
                            (11, '11 T2 abcd')]

        self.assertEqual(results, required_results)

    def test_parsing_c5(self):
        self.tested.set_context_size(5)
        results = [(row_params['timestamp'], row) for row, row_params in self.tested]
        required_results = [(1, '1 T1 a'),
                            (2, '2 T1 b'),
                            (3, '3 T2 c'),
                            (4, '4 T2 d'),
                            (5, '5 T1 abcd'),
                            (6, '6 T2 abcd'),
                            (7, '7 T2 f'),
                            (8, '8 T2 a'),
                            (9, '9 T2 a'),
                            (10, '10 T1 a'),
                            (11, '11 T2 abcd')]

        self.assertEqual(results, required_results)


class MultiThreadBlobParserTest(unittest.TestCase):
    def setUp(self):
        data = [('1 T1 a', {'timestamp': 1, 'match': None, 'thread': 'T1'}),
                 ('2 T1 b', {'timestamp': 2, 'match': None, 'thread': 'T1'}),
                 ('3 T2 c', {'timestamp': 3, 'match': None, 'thread': 'T2'}),
                 ('4 T2 d', {'timestamp': 4, 'match': None, 'thread': 'T2'}),
                 ('5 T1 abcd', {'timestamp': 5, 'match': 'abcd', 'thread': 'T1'}),
                 ('6 T2 abcd', {'timestamp': 6, 'match': 'abcd', 'thread': 'T2'}),
                 ('7 T3 a', {'timestamp': 7, 'match': None, 'thread': 'T3'}),
                 ('7 T3 a', {'timestamp': 7, 'match': None, 'thread': 'T3'}),
                 ('7 T3 a', {'timestamp': 7, 'match': None, 'thread': 'T3'}),
                 ('7 T2 f', {'timestamp': 7, 'match': None, 'thread': 'T2'}),
                 ('8 T2 a', {'timestamp': 8, 'match': None, 'thread': 'T2'}),
                 ('9 T2 a', {'timestamp': 9, 'match': None, 'thread': 'T2'}),
                 ('10 T1 a', {'timestamp': 10, 'match': None, 'thread': 'T1'}),
                 ('11 T2 abcd', {'timestamp': 11, 'match': 'abcd', 'thread': 'T2'})]

        self.tested = MultiThreadBlobbingContextFileParser(RowGetterStub(data), context_size=3)

    def test_parsing_c1(self):
        self.tested.set_context_size(1)
        results = [(row_params['timestamp'], row) for row, row_params in self.tested]
        required_results = [(2, '2 T1 b'),
                            (5, '5 T1 abcd'),
                            (4, '4 T2 d'),
                            (6, '6 T2 abcd'),
                            (7, '7 T2 f'),
                            (10, '10 T1 a'),
                            (9, '9 T2 a'),
                            (11, '11 T2 abcd')]

        self.assertEqual(results, required_results)

    def test_parsing_c2(self):
        self.tested.set_context_size(2)
        results = [(row_params['timestamp'], row) for row, row_params in self.tested]
        required_results = [(1, '1 T1 a'),
                            (2, '2 T1 b'),
                            (5, '5 T1 abcd'),
                            (3, '3 T2 c'),
                            (4, '4 T2 d'),
                            (6, '6 T2 abcd'),
                            (7, '7 T2 f'),
                            (8, '8 T2 a'),
                            (10, '10 T1 a'),
                            (9, '9 T2 a'),
                            (11, '11 T2 abcd')]

        self.assertEqual(results, required_results)

    def test_parsing_c3(self):
        self.tested.set_context_size(3)
        results = [(row_params['timestamp'], row) for row, row_params in self.tested]
        required_results = [(1, '1 T1 a'),
                            (2, '2 T1 b'),
                            (5, '5 T1 abcd'),
                            (3, '3 T2 c'),
                            (4, '4 T2 d'),
                            (6, '6 T2 abcd'),
                            (7, '7 T2 f'),
                            (8, '8 T2 a'),
                            (9, '9 T2 a'),
                            (10, '10 T1 a'),
                            (11, '11 T2 abcd')]

        self.assertEqual(results, required_results)

    def test_parsing_c4(self):
        self.tested.set_context_size(4)
        results = [(row_params['timestamp'], row) for row, row_params in self.tested]
        required_results = [(1, '1 T1 a'),
                            (2, '2 T1 b'),
                            (5, '5 T1 abcd'),
                            (3, '3 T2 c'),
                            (4, '4 T2 d'),
                            (6, '6 T2 abcd'),
                            (7, '7 T2 f'),
                            (8, '8 T2 a'),
                            (9, '9 T2 a'),
                            (10, '10 T1 a'),
                            (11, '11 T2 abcd')]

        self.assertEqual(results, required_results)

    def test_parsing_c5(self):
        self.tested.set_context_size(5)
        results = [(row_params['timestamp'], row) for row, row_params in self.tested]
        required_results = [(1, '1 T1 a'),
                            (2, '2 T1 b'),
                            (5, '5 T1 abcd'),
                            (3, '3 T2 c'),
                            (4, '4 T2 d'),
                            (6, '6 T2 abcd'),
                            (7, '7 T2 f'),
                            (8, '8 T2 a'),
                            (9, '9 T2 a'),
                            (10, '10 T1 a'),
                            (11, '11 T2 abcd')]

        self.assertEqual(results, required_results)


if __name__ == '__main__':
    unittest.main()
