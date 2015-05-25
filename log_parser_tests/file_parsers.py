# -*- coding: utf-8 -*-
__author__ = 'lightrevan'

import unittest
import tempfile
import os
import re

from log_parser.file_parsers import *
from log_parser.row_parsers import *


class FileParserTest(unittest.TestCase):
    def setUp(self):
        fd, self.fname = tempfile.mkstemp()
        os.close(fd)

        self.pattern = re.compile('abcd')
        self.tested = None

        with open(self.fname, 'w') as f:
            self.fill_file(f)

    def tearDown(self):
        del self.tested
        os.remove(self.fname)  # TODO: for some weird reason fails when test fails


class SingleLineFileParserTest(FileParserTest):
    def setUp(self):
        super(SingleLineFileParserTest, self).setUp()

        row_parser_cls = functools.partial(MultiPatternRowParser, timestamp=int_timestamp)
        row_getter_cls = SimpleRowGetter
        self.tested = SingleLineFileParser(row_parser_cls, row_getter_cls, self.fname, self.pattern)

    def fill_file(self, f):
        contents = '''
            1 a
            2 b
            3 c
            4 d
            5 abcd
            6 e
            7 f
            8 abcd
            9 a
            10 a
            11 a
            12 a
            13 a
            14 a
            15 a
            16 abcd
            17 a
            '''.strip()
        contents = '\n'.join([row.strip() for row in contents.split('\n')])
        f.write(contents)

    def test_parsing(self):
        results = [(row_params['timestamp'], row) for row, row_params in self.tested]
        required_results = [(5, '5 abcd'),
                            (8, '8 abcd'),
                            (16, '16 abcd')]

        self.assertEqual(results, required_results)


class ContextFileParserTest(FileParserTest):
    def setUp(self):
        super(ContextFileParserTest, self).setUp()

        row_parser_cls = functools.partial(MultiPatternRowParser, timestamp=int_timestamp)
        row_getter_cls = SimpleRowGetter
        self.tested = SimpleContextFileParser(row_parser_cls, row_getter_cls, self.fname, self.pattern, context_size=3)

    def fill_file(self, f):
        contents = '''
            1 a
            2 b
            3 c
            4 d
            5 abcd
            6 e
            7 f
            8 abcd
            9 a
            10 a
            11 a
            12 a
            13 a
            14 a
            15 a
            16 abcd
            17 a
            18 a
            '''.strip()
        contents = '\n'.join([row.strip() for row in contents.split('\n')])
        f.write(contents)

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


class ContextFileParserTestShortFile(ContextFileParserTest):
    def fill_file(self, f):
        contents = '''
            1 a
            2 b
            3 c
            4 d
            5 abcd
            6 e
            7 f
            8 abcd
            9 a
            10 a
            11 a
            12 a
            13 a
            14 a
            15 a
            16 abcd'''.strip()
        contents = '\n'.join([row.strip() for row in contents.split('\n')])
        f.write(contents)

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


class ThreadCommonBufferParserTest(FileParserTest):
    def setUp(self):
        super(ThreadCommonBufferParserTest, self).setUp()

        row_parser_cls = functools.partial(MultiPatternRowParser, timestamp=int_timestamp, thread='T\d+')
        row_getter_cls = SimpleRowGetter
        self.tested = ThreadContextCommonBufferFileParser(row_parser_cls, row_getter_cls, self.fname, self.pattern, context_size=3)

    def fill_file(self, f):
        contents = '''
            1 T1 a
            2 T1 b
            3 T2 c
            4 T2 d
            5 T1 abcd
            6 T1 e
            7 T2 f
            8 T2 a
            9 T2 a
            10 T1 a
            11 T2 abcd
            '''.strip()
        contents = '\n'.join([row.strip() for row in contents.split('\n')])
        f.write(contents)

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


class SingleThreadParserTest(FileParserTest):
    def setUp(self):
        super(SingleThreadParserTest, self).setUp()

        row_parser_cls = functools.partial(MultiPatternRowParser, timestamp=int_timestamp, thread='T\d+')
        row_getter_cls = SimpleRowGetter
        self.tested = SingleThreadContextFileParser(row_parser_cls, row_getter_cls, self.fname, self.pattern, context_size=3)

    def fill_file(self, f):
        contents = '''
            1 T1 a
            2 T1 b
            4 T2 d
            5 T1 abcd
            6 T1 e
            7 T2 f
            7 T3 a
            7 T3 a
            7 T3 a
            8 T2 a
            9 T2 a
            10 T1 a
            11 T2 abcd
            12 T1 abcd
            13 T1 a
            14 T1 a
            '''.strip()
        contents = '\n'.join([row.strip() for row in contents.split('\n')])
        f.write(contents)

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


class MultiThreadParserTest(FileParserTest):
    def setUp(self):
        super(MultiThreadParserTest, self).setUp()

        row_parser_cls = functools.partial(MultiPatternRowParser, timestamp=int_timestamp, thread='T\d+')
        row_getter_cls = SimpleRowGetter
        self.tested = MultiThreadContextFileParser(row_parser_cls, row_getter_cls, self.fname, self.pattern, context_size=3)

    def fill_file(self, f):
        contents = '''
            1 T1 a
            2 T1 b
            3 T2 c
            4 T2 d
            5 T1 abcd
            6 T2 abcd
            7 T3 a
            7 T3 a
            7 T3 a
            7 T2 f
            8 T2 a
            9 T2 a
            10 T1 a
            11 T2 abcd
            '''.strip()
        contents = '\n'.join([row.strip() for row in contents.split('\n')])
        f.write(contents)

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


class MultiThreadBlobParserTest(FileParserTest):
    def setUp(self):
        super(MultiThreadBlobParserTest, self).setUp()

        row_parser_cls = functools.partial(MultiPatternRowParser, timestamp=int_timestamp, thread='T\d+')
        row_getter_cls = SimpleRowGetter
        self.tested = MultiThreadBlobbingContextFileParser(row_parser_cls, row_getter_cls, self.fname, self.pattern, context_size=3)

    def fill_file(self, f):
        contents = '''
            1 T1 a
            2 T1 b
            3 T2 c
            4 T2 d
            5 T1 abcd
            6 T2 abcd
            7 T3 a
            7 T3 a
            7 T3 a
            7 T2 f
            8 T2 a
            9 T2 a
            10 T1 a
            11 T2 abcd
            '''.strip()
        contents = '\n'.join([row.strip() for row in contents.split('\n')])
        f.write(contents)

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
