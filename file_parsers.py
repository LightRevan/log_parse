# -*- coding: utf-8 -*-

import re

class BaseFileParser(object):
    def __init__(self, row_parser, file_name, pattern):
        self.file = open(file_name, 'r')
        self.pattern = pattern
        self.row_parser = row_parser
        self.timestamp = None
        self.row = None

    def __del__(self):
        # TODO: test that it really works
        self.file.close()

    def __cmp__(self, other):
        if not isinstance(other, BaseFileParser):
            raise TypeError('Trying to compare FileParser object with something else: %s' % type(other))
        return cmp(self.timestamp, other.timestamp)

    def __iter__(self):
        return self

    def next(self):
        raise StopIteration

class SimpleFileParser(BaseFileParser):
    def next(self):
        # as file stops so should we
        while True:
            self.row = self.file.next()
            if self.pattern.find(self.row):
                row_parse_result = self.row_parser.parse_row(self.row)
                self.timestamp = row_parse_result['timestamp']
                return self

class BufferedFileParser(BaseFileParser):
    def __init__(self, *args):
        super(BufferedFileParser, self).__init__(self, *args)
        self._buffered_rows = []

    def next(self):
        pass
