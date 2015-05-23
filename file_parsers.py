# -*- coding: utf-8 -*-

import re

class BaseFileParser(object):
    def __init__(self, file_name, pattern, row_parser):
        self.file = open(file_name, 'r')
        self.pattern = pattern
        self.row_parser = row_parser
        self.timestamp = None
        self.row = None

    def __del__(self):
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
        # as file fail so should we
        self.row = self.file.next()
        if self.pattern.find(self.row):
            self.parse_row()
            return self

    def parse_row(self):
        self.timestamp = int(self.timestamp_pattern.search(self.row).group(0))

class BufferedFileParser(BaseFileParser):
    def __init__(self, *args):
        super(BufferedFileParser, self).__init__(self, *args)
        self._buffered_rows = []

    def next(self):
        pass

    def parse_row(self):
        pass