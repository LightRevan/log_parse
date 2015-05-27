# -*- coding: utf-8 -*-
__author__ = 'lightrevan'

import re
import functools
import collections
import datetime as dt


class RowParsingError(LookupError):
    pass


def not_none_transform(match):
    if match is None:
        raise RowParsingError
    else:
        return match


def date_transform(match):
    if match is None:
        raise RowParsingError
    else:
        return dt.datetime.strptime(match, '%y-%m-%d %H:%M:%S,%f')

int_timestamp = ('^\d+', lambda x: int(not_none_transform(x)))


class AbstractRowParser(object):
    @classmethod
    def _compile_pattern(cls, pattern):
        return pattern if isinstance(pattern, re._pattern_type) else re.compile(pattern)

    def parse_row(self, row):
        raise NotImplemented

    def has_pattern(self, name):
        raise NotImplemented


class MultiPatternRowParser(AbstractRowParser):
    def __init__(self, match_pattern, **kwargs):
        assert 'timestamp' in kwargs, 'Must have timestamp pattern in row parser'

        match_pattern = match_pattern
        self._patterns = {'match': (self._compile_pattern(match_pattern), lambda x: x)}
        for name, data in kwargs.items():
            if isinstance(data, tuple):
                pattern, transform = data
            else:
                pattern = data
                transform = not_none_transform

            self._patterns[name] = (self._compile_pattern(pattern), transform)

    def parse_row(self, row):
        res = {}
        for name, data in self._patterns.items():
            pattern, transform = data
            match = pattern.search(row)
            res[name] = transform(match.group(0) if match else None)

        return res

    def has_pattern(self, name):
        return name in self._patterns


class SinglePatternRowParser(AbstractRowParser):
    def __init__(self, match_pattern, row_pattern, group_transforms=None):
        self._match_pattern = self._compile_pattern(match_pattern)
        self._row_pattern = self._compile_pattern(row_pattern)
        assert 'timestamp' in self._row_pattern.groupindex, 'Must have timestamp pattern in row parser'

        self._group_transforms = {name: not_none_transform for name in self._row_pattern.groupindex}
        if group_transforms is not None:
            self._group_transforms.update(group_transforms)

    def parse_row(self, row):
        params_match = self._row_pattern.search(row)
        match = self._match_pattern.search(row)

        res = {'match': match.group(0) if match else None}
        for name, transform in self._group_transforms.items():
            res[name] = transform(params_match.group(name) if params_match else None)

        return res

    def has_pattern(self, name):
        return name in self._row_pattern.groupindex


class SimpleRowGetter(object):
    def __init__(self, f, row_parser):
        self._f = f
        self.row_parser = row_parser

    def __iter__(self):
        return self

    def next(self):
        row = self._f.next().strip()
        return row, self.row_parser.parse_row(row)


class MergingRowGetter(SimpleRowGetter):
    def __init__(self, *args):
        super(MergingRowGetter, self).__init__(*args)

        self._next_row = None
        self._next_params = None

    def next(self):
        if self._next_row is None:
            row = self._f.next().strip()
            first_row = row
            first_row_valid = False
            while not first_row_valid:
                try:
                    params = self.row_parser.parse_row(first_row)
                    first_row_valid = True
                except RowParsingError:
                    first_row = self._f.next().strip()
                    row += '\n' + first_row
        else:
            row, params = self._next_row, self._next_params

        try:
            next_row_valid = False
            self._next_row = None
            while not next_row_valid:
                next_row = self._f.next()
                try:
                    next_params = self.row_parser.parse_row(next_row)

                    next_row_valid = True
                    self._next_row = next_row
                    self._next_params = next_params
                except RowParsingError:
                    row += '\n' + next_row
        except StopIteration:
            pass

        return row, params