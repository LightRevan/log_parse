# -*- coding: utf-8 -*-
__author__ = 'lightrevan'

import collections

class BaseFileParser(object):
    def __init__(self, row_parser, file_name, pattern):
        self._file = open(file_name, 'r')
        self._pattern = pattern
        self._row_parser = row_parser
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

class SingleLineFileParser(BaseFileParser):
    def next(self):
        # as file stops so should we
        while True:
            self.row = self._file.next()
            if self._pattern.find(self.row):
                row_parse_result = self._row_parser.parse_row(self.row)
                self.timestamp = row_parse_result['timestamp']
                return self

class ContextFileParser(BaseFileParser):
    def __init__(self, *args, **kwargs):
        self._context_size = kwargs.pop('context_size', 100)
        self._buffer = collections.deque()

        super(ContextFileParser, self).__init__(self, *args, **kwargs)

    def next(self):
        pending_rows = 0

        while True:
            try:
                row = self._file.next()
                row_parse_result = self._row_parser.parse_row(self.row)
                timestamp = row_parse_result['timestamp']

                if self._pattern.find(self.row):
                    pending_rows = len(self._buffer) + self._context_size
                elif len(self._buffer) == self._context_size and pending_rows == 0:
                    self._buffer.popleft()

                self._buffer.append((timestamp, row))
            except StopIteration:
                if pending_rows:
                    pass  # file ended - fuck it, we have buffer
                else:
                    raise StopIteration

            if pending_rows:
                try:
                    self.timestamp, self.row = self._buffer.popleft()
                    pending_rows -= 1
                    return self
                except IndexError:
                    raise StopIteration  # buffer ended - time to go



