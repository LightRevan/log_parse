# -*- coding: utf-8 -*-
__author__ = 'lightrevan'

import collections
import heapq
import functools


def create_file_parser(file_parser_cls, row_parser_cls, row_getter_cls, **kwargs):
    return functools.partial(file_parser_cls, row_parser_cls, row_getter_cls, **kwargs)


class BaseFileParser(object):
    def __init__(self, row_parser_cls, row_getter_cls, file_name, pattern):
        self._file = open(file_name, 'r')
        row_parser = row_parser_cls(pattern)
        self._row_getter = row_getter_cls(self._file, row_parser)

    def __del__(self):
        self._file.close()

    def __iter__(self):
        return self

    def next(self):
        raise NotImplemented


class SingleLineFileParser(BaseFileParser):
    def next(self):
        while True:
            row, row_parse_result = self._row_getter.next()
            if row_parse_result['match']:
                timestamp = row_parse_result['timestamp']
                return timestamp, row, row_parse_result


class ContextFileParser(BaseFileParser):
    def __init__(self, *args, **kwargs):
        self._context_size = kwargs.pop('context_size', 100)
        assert self._context_size > 0, 'Context cannot be zero. Use SingleLineFileParser instead'

        super(ContextFileParser, self).__init__(*args, **kwargs)

    def set_context_size(self, context_size):
        if self._context_size != context_size:
            assert context_size > 0, 'Context cannot be zero. Use SingleLineFileParser instead'

            self._context_size = context_size

class ContextCommonBufferFileParser(ContextFileParser):
    def __init__(self, *args, **kwargs):
        super(ContextCommonBufferFileParser, self).__init__(*args, **kwargs)

        self._buffer = collections.deque()
        self._pending_rows = 0
        self._file_ended = False

    def set_context_size(self, context_size):
        if self._context_size != context_size:
            assert len(self._buffer) == 0, 'Parsing is in progress, cannot change context size'
            super(ContextCommonBufferFileParser, self).set_context_size(context_size)

    def next(self):
        while True:
            try:
                row, row_params = self._row_getter.next()

                if row_params['match']:
                    self._init_output(row_params)

                self._add_to_buffer(row_params, row)
            except StopIteration:
                self._file_ended = True
                if not self._pending_rows:
                    raise StopIteration  # no more file and dont need anything else

            if len(self._buffer) > self._context_size or self._pending_rows:
                try:
                    buffered_row = self._buffer.popleft()
                    if self._pending_rows:
                        res = self._prepare_output(*buffered_row)
                        if res is not None:
                            return res
                except IndexError:
                    if self._file_ended:
                        raise StopIteration  # no more file or buffer


class SimpleContextFileParser(ContextCommonBufferFileParser):
    def _init_output(self, row_params):
        self._pending_rows = len(self._buffer) + 1 + self._context_size

    def _add_to_buffer(self, row_params, row):
        self._buffer.append((row_params['timestamp'], row, row_params))

    def _prepare_output(self, timestamp, row, row_params):
        self._pending_rows -= 1
        return timestamp, row, row_params


class ThreadContextCommonBufferFileParser(ContextCommonBufferFileParser):
    def __init__(self, *args, **kwargs):
        super(ThreadContextCommonBufferFileParser, self).__init__(*args, **kwargs)
        assert self._row_getter.row_parser.has_pattern('thread'), 'Row parser should be able to find threads'

        self._looked_up_threads = {}
        self._current_row_number = 0

    def _init_output(self, row_params):
        self._pending_rows = len(self._buffer) + 1 + self._context_size
        self._looked_up_threads[row_params['thread']] = self._current_row_number

    def _add_to_buffer(self, row_params, row):
        self._buffer.append((self._current_row_number,
                             row_params['timestamp'],
                             row_params['thread'],
                             row,
                             row_params))
        self._current_row_number += 1

    def _prepare_output(self, row_number, timestamp, thread, row, row_params):
        self._pending_rows -= 1
        thread_row_number = self._looked_up_threads.get(thread, None)
        if thread_row_number is not None and abs(thread_row_number-row_number) <= self._context_size:
            return timestamp, row, row_params
        return None


class SingleThreadContextFileParser(ContextCommonBufferFileParser):
    def __init__(self, *args, **kwargs):
        self._thread = kwargs.pop('thread', None)

        super(SingleThreadContextFileParser, self).__init__(*args, **kwargs)
        assert self._row_getter.row_parser.has_pattern('thread'), 'Row parser should be able to find threads'

    def _init_output(self, row_params):
        if self._thread is None or row_params['thread'] == self._thread:
            self._thread = row_params['thread']

            valid_rows_num = 0
            for _, thread, _, _ in self._buffer:
                if thread == self._thread:
                    valid_rows_num += 1

            self._pending_rows = valid_rows_num + 1 + self._context_size

    def _add_to_buffer(self, row_params, row):
        if self._thread is None or row_params['thread'] == self._thread:
            self._buffer.append((row_params['timestamp'],
                                 row_params['thread'],
                                 row,
                                 row_params))

    def _prepare_output(self, timestamp, thread, row, row_params):
        if thread == self._thread:
            self._pending_rows -= 1
            return timestamp, row, row_params
        return None


class ThreadBuffer(object):
    def __init__(self, context_size):
        self.timestamp = None
        self._pending_rows = 0
        self._context_size = context_size
        self._buffer = collections.deque()

    def init_output(self):
        self._pending_rows = len(self._buffer) + 1 + self._context_size

    def output_ready(self):
        return len(self._buffer) and self._pending_rows

    def push(self, timestamp, row, row_params):
        if self.timestamp is None:
            self.timestamp = timestamp

        self._buffer.append((timestamp, row, row_params))
        if not self._pending_rows and len(self._buffer) > self._context_size:
            self._buffer.popleft()

    def pop(self):
        buffer_elem = self._buffer.popleft()

        self.timestamp = self._buffer[0][0] if len(self._buffer) else None
        self._pending_rows -= 1

        return buffer_elem

    def __cmp__(self, other):
        if not isinstance(other, ThreadBuffer):
            raise TypeError('Trying to compare ThreadBuffer object with something else: %s' % type(other))
        return cmp(self.timestamp, other.timestamp)


class MultiThreadContextFileParser(ContextFileParser):
    def __init__(self, *args, **kwargs):
        super(MultiThreadContextFileParser, self).__init__(*args, **kwargs)
        assert self._row_getter.row_parser.has_pattern('thread'), 'Row parser should be able to find threads'

        self._thread_buffers = {}
        self._buffer_heap = []
        self._file_ended = False

    def set_context_size(self, context_size):
        if self._context_size != context_size:
            assert not self._thread_buffers, 'Parsing is in progress, cannot change context size'
            super(MultiThreadContextFileParser, self).set_context_size(context_size)

    def _process_buffer(self, thread_buffer, was_not_ready, is_ready):
        if is_ready and was_not_ready:
            heapq.heappush(self._buffer_heap, thread_buffer)

    def _process_file_end(self):
        if not len(self._buffer_heap):
            raise StopIteration

    def _prepare_output(self):
        res = None
        if len(self._buffer_heap):
            thread_buffer = heapq.heappop(self._buffer_heap)
            res = thread_buffer.pop()
            if thread_buffer.output_ready():
                heapq.heappush(self._buffer_heap, thread_buffer)
        elif self._file_ended:
            raise StopIteration

        return res or None

    def next(self):
        while True:
            try:
                row, row_params = self._row_getter.next()
                thread = row_params['thread']

                thread_buffer = self._thread_buffers.get(thread)
                if not thread_buffer:
                    thread_buffer = ThreadBuffer(self._context_size)
                    self._thread_buffers[thread] = thread_buffer

                was_not_ready = not thread_buffer.output_ready()
                if row_params['match']:
                    thread_buffer.init_output()
                thread_buffer.push(row_params['timestamp'], row, row_params)
                is_ready = thread_buffer.output_ready()

                self._process_buffer(thread_buffer, was_not_ready, is_ready)
            except StopIteration:
                self._file_ended = True
                self._process_file_end()

            res = self._prepare_output()
            if res is not None:
                return res


class MultiThreadBlobbingContextFileParser(MultiThreadContextFileParser):
    def __init__(self, *args, **kwargs):
        super(MultiThreadBlobbingContextFileParser, self).__init__(*args, **kwargs)

        self._current_buffer = None

    def _process_buffer(self, thread_buffer, was_not_ready, is_ready):
        if thread_buffer is not self._current_buffer and is_ready and was_not_ready:
            heapq.heappush(self._buffer_heap, thread_buffer)

    def _process_file_end(self):
        if not len(self._buffer_heap) and not self._current_buffer:
            raise StopIteration

    def _prepare_output(self):
        res = None

        if self._current_buffer:
            res = self._current_buffer.pop()
            if not self._current_buffer.output_ready():
                self._current_buffer = None
        elif len(self._buffer_heap):
            thread_buffer = heapq.heappop(self._buffer_heap)
            res = thread_buffer.pop()
            if thread_buffer.output_ready():
                self._current_buffer = thread_buffer
        elif self._file_ended:
            raise StopIteration

        return res or None
