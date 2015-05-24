# -*- coding: utf-8 -*-
__author__ = 'lightrevan'

import re


class SimpleRowParser(object):
    def __init__(self, timestamp_pattern):
        self.timestamp_pattern = re.compile(timestamp_pattern)

    def parse_row(self, row):
        return {'timestamp': int(self.timestamp_pattern.search(row).group(0))}


class ThreadRowParser(object):
    def __init__(self, timestamp_pattern, thread_pattern):
        self.timestamp_pattern = re.compile(timestamp_pattern)
        self.thread_pattern = re.compile(thread_pattern)

    def parse_row(self, row):
        return {'timestamp': int(self.timestamp_pattern.search(row).group(0)),
                'thread': self.thread_pattern.search(row).group(0)}


class SimpleRowGetter(object):
    def __init__(self, f, row_parser):
        self._f = f
        self._row_parser = row_parser

    def __iter__(self):
        return self

    def next(self):
        row = self._f.next().strip()
        return row, self._row_parser.parse_row(row)


class MergingRowGetter(SimpleRowGetter):
    def __init__(self, *args):
        super(MergingRowGetter, self).__init__(*args)

        self._next_row = None
        self._next_params = None

    def next(self):
        if self._next_row is None:
            row = self._f.next().strip()
            params = self._row_parser.parse_row(row)
        else:
            row, params = self._next_row, self._next_params

        try:
            next_row_valid = False
            self._next_row = None
            while not next_row_valid:
                next_row = self._f.next()
                try:
                    next_params = self._row_parser.parse_row(next_row)

                    next_row_valid = True
                    self._next_row = next_row
                    self._next_params = next_params
                except AttributeError:
                    row += '\n' + next_row
        except StopIteration:
            pass

        return row, params