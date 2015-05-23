# -*- coding: utf-8 -*-

import argparse
import heapq

from file_parsers import *
from row_parsers import *

class BaseMultiFileParser(object):
    def __init__(self, pattern):
        self.pattern = re.compile(pattern)

    def parse(self, file_names):
        parsers = []
        for file_name in file_names:
            parser_ = BaseFileParser(file_name, self.pattern)
            parser_.next()
            parsers.append(parser_)

        heapq.heapify(parsers)
        while parsers:
            parser_ = heapq.heappop(parsers)

            try:
                parser_.next()
                self.output(parser_.row)
                heapq.heappush(parsers, parser_)
            except StopIteration:
                pass

    def output(self, row):
        print row

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', help='regular expression, compatible with python re module')
    parser.add_argument('file_names', nargs='+')

    args = parser.parse_args()

    parser = BaseMultiFileParser(args.pattern)
    parser.parse(args.file_names)




