# -*- coding: utf-8 -*-

import argparse
import re, heapq

class BaseFileParser(object):
    def __init__(self, file_name, pattern):
        self.file = open(file_name, 'r')
        self.pattern = pattern
        self.timestamp = None
        self.row = None

    def __del__(self):
        self.file.close()

    def __cmp__(self, other):
        if not isinstance(other, BaseFileParser):
            raise TypeError('Trying to compare FileParser object with something else: %s' % type(other))
        return cmp(self.timestamp, other.timestamp)

    def fetch_next_row(self):
        return False

class BaseMultiFileParser(object):
    def __init__(self, pattern):
        self.pattern = re.compile(pattern)

    def parse(self, file_names):
        parsers = []
        for file_name in file_names:
            parser = BaseFileParser(file_name, self.pattern)
            parser.fetch_next_row()
            parsers.append(parser)

        heapq.heapify(parsers)
        while parsers:
            parser = heapq.heappop(parsers)

            if parser.fetch_next_row():
                self.output(parser.row)
                heapq.heappush(parsers, parser)

    def output(self, row):
        print row

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('pattern', help='regular expression, compatible with python re module')
    parser.add_argument('file_names', nargs='+')

    args = parser.parse_args()


