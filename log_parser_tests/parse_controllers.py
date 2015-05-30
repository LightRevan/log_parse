# -*- coding: utf-8 -*-
__author__ = 'lightrevan'

import unittest
from mocks_and_stubs import *

from log_parser.parse_controllers import *
from log_parser.output_methods import *
# TODO: implement moar test cases


class BaseParseContollerSimpleTestCase(unittest.TestCase):
    def setUp(self):
        conc = lambda r: (str(r[0]) + r[1], {'timestamp': r[0]})
        self.files = [map(conc, zip(range(1, 16, 3), ['a']*5)),
                      map(conc, zip(range(2, 16, 3), ['a']*5)),
                      map(conc, zip(range(3, 16, 3), ['a']*5))]

        pattern = re.compile('a')
        self.output = ListOutput()
        self.tested = BaseParseContoller(pattern, self.output)

    def test_1(self):
        conc = lambda r: str(r[0]) + r[1]
        req_res = map(conc, zip(range(1, 16), ['a']*15))

        self.tested.parse(self.files, create_file_parser_stub, create_row_parser_stub, create_row_getter_stub)
        self.assertEqual(self.output.data, req_res)


if __name__ == '__main__':
    unittest.main()
