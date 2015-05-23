# -*- coding: utf-8 -*-
__author__ = 'lightrevan'

import unittest
import tempfile
import os
import re

from logic.file_parsers import *
from logic.row_parsers import *


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
        os.remove(self.fname)

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
            13 abcd
            14 a
            '''.strip()
        contents = '\n'.join([row.strip() for row in contents.split('\n')])
        f.write(contents)

class SingleLineFileParserTest(FileParserTest):
    def setUp(self):
        super(SingleLineFileParserTest, self).setUp()

        row_parser = SimpleRowParser('^\d+')
        self.tested = SingleLineFileParser(row_parser, self.fname, self.pattern)

    def test_parsing(self):
        results = [(res.timestamp, res.row) for res in self.tested]
        required_results = [(5, '5 abcd'),
                            (8, '8 abcd'),
                            (13, '13 abcd')]

        self.assertEqual(results, required_results)

class ContextFileParserTest(FileParserTest):
    def setUp(self):
        super(ContextFileParserTest, self).setUp()

        row_parser = SimpleRowParser('^\d+')
        self.tested = ContextFileParser(row_parser, self.fname, self.pattern)

if __name__ == '__main__':
    unittest.main()
