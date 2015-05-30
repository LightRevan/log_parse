# -*- coding: utf-8 -*-
__author__ = 'lightrevan'

class RowParserStub(object):
    def has_pattern(self, something):
        return True

class RowGetterStub(object):
    def __init__(self, data, row_parser_cls=RowParserStub):
        self.data = iter(data)
        self.row_parser = row_parser_cls()

    def next(self):
        return self.data.next()

def create_row_parser_stub(*args):
    pass

def create_row_getter_stub(file, *args):
    return file

def create_file_parser_stub(file):
    return iter(file)