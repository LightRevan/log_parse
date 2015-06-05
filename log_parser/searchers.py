# -*- coding: utf-8 -*-

import re
import collections


class InvalidParsing(ValueError): pass


class AbstractSearchInstance(object):
    def process_row(self, row, row_params):
        raise NotImplementedError

    @classmethod
    def can_start(cls, row, row_params):
        raise NotImplementedError

class AbstractSearcher(object):
    def __init__(self, data, state_cls):
        self.data = data
        self.output_buffer = collections.deque()
        self.states = {}
        self.state_cls = state_cls

    def __iter__(self):
        return self

    def next(self):
        while True:
            row, row_params = self.data.next()
            thread = row_params['thread']

            cur_state = self.states.get(thread, None)
            if cur_state is None:
                if self.state_cls.can_start(row, row_params):
                    cur_state = self.create_state(row, row_params)
                    self.states[thread] = cur_state
            else:
                try:
                    cur_state.process_row(row, row_params)
                except InvalidParsing:
                    del self.states[thread]

            if cur_state is not None:
                self.output_buffer.extend(cur_state.output_buffer)

            if self.output_buffer:
                return self.output_buffer.popleft()

    def create_state(self, row, row_params):
        raise NotImplementedError


class SimpleSQLSearchInstance(AbstractSearchInstance):
    sql_pattern = re.compile('delete|update.*set|insert.*into|select.*from', re.I)

    def __init__(self, param_name, found_sql):
        self.output_buffer = collections.deque()

        self.param_name = '\w*' if param_name is None else param_name
        self.found_sql = found_sql

        self.match = None
        self.param_pattern = None

    def process_row(self, row, row_params):
        if self.output_buffer:
            self.output_buffer.clear()

        if self.sql_pattern.search(row):
            self.found_sql = row
            return

        if not row_params['match']:
            return

        if self.match != row_params['match']:
            self.match = row_params['match']
            self.param_pattern = re.compile(r"{.*'%s': ?%s.*}" % (self.param_name, row_params['match']))

        if self.param_pattern.search(row):
            self.output_buffer.append(self.found_sql)
            self.output_buffer.append(row)

    @classmethod
    def can_start(cls, row, row_params):
        return cls.sql_pattern.search(row) is not None


class SimpleSQLSearcher(AbstractSearcher):
    def __init__(self, data, state_cls, param_name=None):
        super(SimpleSQLSearcher, self).__init__(data, state_cls)
        self.param_name = param_name

    def create_state(self, row, row_params):
        return self.state_cls(self.param_name, row)
