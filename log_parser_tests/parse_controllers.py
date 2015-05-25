# -*- coding: utf-8 -*-
__author__ = 'lightrevan'

import unittest
import tempfile
import os

from log_parser.parse_controllers import *
from log_parser.output_methods import *


class BaseParseContollerTestCase(unittest.TestCase):
    def setUp(self):
        self.fnames = []

        conc = lambda r: str(r[0]) + r[1]

        fd, fname = tempfile.mkstemp()
        os.close(fd)
        with open(fname, 'w') as f:
            f.write('\n'.join(map(conc, zip(range(1, 16, 3), ['a']*5))))
        self.fnames.append(fname)

        fd, fname = tempfile.mkstemp()
        os.close(fd)
        with open(fname, 'w') as f:
            f.write('\n'.join(map(conc, zip(range(2, 16, 3), ['a']*5))))
        self.fnames.append(fname)

        fd, fname = tempfile.mkstemp()
        os.close(fd)
        with open(fname, 'w') as f:
            f.write('\n'.join(map(conc, zip(range(3, 16, 3), ['a']*5))))
        self.fnames.append(fname)

        pattern = re.compile('a')
        self.output = ListOutput()
        self.tested = BaseParseContoller(pattern, self.output)

    def tearDown(self):
        del self.tested
        for fname in self.fnames:
            os.remove(fname)

    def test_1(self):
        conc = lambda r: str(r[0]) + r[1]
        req_res = map(conc, zip(range(1, 16), ['a']*15))

        row_parser_creator = functools.partial(MultiPatternRowParser, timestamp=int_timestamp)
        file_parser_creator = create_file_parser(SingleLineFileParser, row_parser_creator, SimpleRowGetter)

        self.tested.parse(self.fnames, file_parser_creator)
        self.assertEqual(self.output.data, req_res)


if __name__ == '__main__':
    unittest.main()
