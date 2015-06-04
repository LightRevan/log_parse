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


date_transform = lambda match: dt.datetime.strptime(not_none_transform(match), '%y-%m-%d %H:%M:%S,%f')
int_timestamp = ('^\d+', lambda x: int(not_none_transform(x)))


class AbstractRowParser(object):
    @classmethod
    def _compile_pattern(cls, pattern):
        return pattern if isinstance(pattern, re._pattern_type) else re.compile(pattern)

    def parse_row(self, row):
        raise NotImplementedError

    def check_match(self, row):
        raise NotImplementedError

    def has_pattern(self, name):
        raise NotImplementedError


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

    def check_match(self, row):
        pattern, transform = self._patterns['match']
        match = pattern.search(row)
        return transform(match.group(0) if match else None)

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

    def check_match(self, row):
        match = self._match_pattern.search(row)
        return match.group(0) if match else None

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
            row, params = '', None
            searching_next = False
        else:
            row, params = self._next_row, self._next_params
            self._next_row = None
            searching_next = True

        need_recheck = False
        row_valid = False
        try:
            parse_row = self._f.next().strip(' \n')
            while not row_valid:
                try:
                    parse_params = self.row_parser.parse_row(parse_row)
                    if searching_next:
                        self._next_row = parse_row
                        self._next_params = parse_params
                        row_valid = True
                    else:
                        row += ('\n' if row else '') + parse_row
                        params = parse_params
                        parse_row = self._f.next().strip(' \n')
                        searching_next = True
                except RowParsingError:
                    row += ('\n' if row else '') + parse_row
                    parse_row = self._f.next().strip(' \n')
                    need_recheck = True
        except StopIteration as e:
            if self._next_row is None and not row:
                raise e
        finally:
            if need_recheck:
                params['match'] = self.row_parser.check_match(row)

        return row, params