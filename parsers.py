# -*- coding: utf-8 -*-

import re

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

    def parse_row(self):
        pass

class SimpleFileParser(BaseFileParser):
    def __init__(self, *args):
        super(SimpleFileParser, self).__init__(self, *args)
        self.timestamp_pattern = re.compile('^\d+')

    def fetch_next_row(self):
        try:
            while True:
                self.row = self.file.next()
                if self.pattern.find(self.row):
                    self.parse_row()
                    return True
        except StopIteration:
            return False

    def parse_row(self):
        self.timestamp = int(self.timestamp_pattern.search(self.row).group(0))

class BufferedFileParser(BaseFileParser):
    def __init__(self, *args):
        super(BufferedFileParser, self).__init__(self, *args)
        self._buffered_rows = []

