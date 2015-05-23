# -*- coding: utf-8 -*-
__author__ = 'lightrevan'

import collections
from row_parsers import *


class BaseFileParser(object):
    def __init__(self, row_parser, file_name, pattern):
        self._file = open(file_name, 'r')
        self._pattern = pattern
        self._row_parser = row_parser
        self.timestamp = None
        self.row = None

    def __del__(self):
        self._file.close()

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
            self.row = self._file.next().strip()
            if self._pattern.search(self.row):
                row_parse_result = self._row_parser.parse_row(self.row)
                self.timestamp = row_parse_result['timestamp']
                return self

class ContextCommonBufferFileParser(BaseFileParser):
    def __init__(self, *args, **kwargs):
        self._context_size = kwargs.pop('context_size', 100)
        assert self._context_size > 0, 'Context cannot be zero. Use SingleLineFileParser instead'

        super(ContextCommonBufferFileParser, self).__init__(*args, **kwargs)

        self._buffer = collections.deque()
        self._pending_rows = 0

    def set_context_size(self, context_size):
        if self._context_size != context_size:
            assert len(self._buffer) == 0, 'Parsing is in progress, cannot change context size'
            assert context_size > 0, 'Context cannot be zero. Use SingleLineFileParser instead'

            self._context_size = context_size

    def next(self):
        while True:
            try:
                row = self._file.next().strip()
                row_params = self._row_parser.parse_row(row)

                if self._pattern.search(row):
                    self._init_output(row_params)
                elif len(self._buffer) == self._context_size and self._pending_rows == 0:
                    self._buffer.popleft()

                self._add_to_buffer(row_params, row)
            except StopIteration:
                if self._pending_rows:
                    pass  # file ended - fuck it, we have buffer
                else:
                    raise StopIteration

            if self._pending_rows:
                try:
                    if self._output():
                        return self
                except IndexError:
                    raise StopIteration  # buffer ended - time to go


class SimpleContextFileParser(ContextCommonBufferFileParser):
    def _init_output(self, row_params):
        self._pending_rows = len(self._buffer) + 1 + self._context_size

    def _add_to_buffer(self, row_params, row):
        self._buffer.append((row_params['timestamp'], row))

    def _output(self):
        self.timestamp, self.row = self._buffer.popleft()
        self._pending_rows -= 1

        return True


class ThreadContextCommonBufferFileParser(ContextCommonBufferFileParser):
    def __init__(self, *args, **kwargs):
        super(ThreadContextCommonBufferFileParser, self).__init__(*args, **kwargs)
        assert isinstance(self._row_parser, ThreadRowParser), 'Row parser should be ThreadRowParser'

        self._looked_up_threads = set()

    def _init_output(self, row_params):
        self._pending_rows = len(self._buffer) + 1 + self._context_size
        self._looked_up_threads.add(row_params['thread'])

    def _add_to_buffer(self, row_params, row):
        self._buffer.append((row_params['timestamp'],
                             row_params['thread'],
                             row))

    def _output(self):
        self.timestamp, thread, self.row = self._buffer.popleft()
        self._pending_rows -= 1
        if thread in self._looked_up_threads:
            return self
