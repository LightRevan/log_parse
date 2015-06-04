# -*- coding: utf-8 -*-

import re
import collections


class AbstractQuery(object):
    def __init__(self, data):
        self.data = data
        self.buffer = collections.deque()

    def __iter__(self):
        return self

    def next(self):
        while not len(self.buffer):
            self.process_row(*self.data.next())

        return self.buffer.popleft()

    def process_row(self, row, row_params):
        raise NotImplementedError


class SimpleSQLQuery(AbstractQuery):
    def __init__(self, data, param_name=None):
        super(SimpleSQLQuery, self).__init__(data)

        self.sql_pattern = re.compile('delete|update.*set|insert.*into|select.*from', re.I)
        self.param_name = '\w*' if param_name is None else param_name

        self.found_sql = {}
        self.match = None
        self.param_pattern = None

    def process_row(self, row, row_params):
        if self.found_sql.get(row_params['thread'], None):
            if not row_params['match']:
                return None

            if self.match != row_params['match']:
                self.match = row_params['match']
                self.param_pattern = re.compile(r"{.*'%s': ?%s.*}" % (self.param_name, row_params['match']))

            if self.param_pattern.search(row):
                self.buffer.append(self.found_sql[row_params['thread']])
                self.buffer.append(row)

                return self.buffer
        else:
            if self.sql_pattern.search(row):
                self.found_sql[row_params['thread']] = row

        return None