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
        _, self.fname = tempfile.mkstemp()
        self.pattern = re.compile('abcd')

        with open(self.fname, 'w') as f:
            self.fill_file(f)

    def tearDown(self):
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
        f.write(contents)

class SingleLineFileParserTest(FileParserTest):
    def setUp(self):
        super(SingleLineFileParserTest, self).setUp()

        row_parser = SimpleRowParser('^\d+')
        self.tested = SingleLineFileParser(row_parser, self.fname, self.pattern)

    def test_parsing(self):
        results = []

class ContextFileParserTest(FileParserTest):
    def setUp(self):
        super(ContextFileParserTest, self).setUp()

        row_parser = SimpleRowParser('^\d+')
        self.tested = ContextFileParser(row_parser, self.fname, self.pattern)

if __name__ == '__main__':
    unittest.main()
