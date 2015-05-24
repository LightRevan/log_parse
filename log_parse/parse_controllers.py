# -*- coding: utf-8 -*-
__author__ = 'lightrevan'

import argparse
import heapq
import functools

from file_parsers import *
from row_parsers import *


def create_file_parser(file_parser_cls, row_parser, **kwargs):
    return functools.partial(file_parser_cls, row_parser, **kwargs)


class FileParserDecorator(object):
    def __init__(self, file_parser):
        self.file_parser = file_parser
        self.timestamp = None
        self.row = None

    def __cmp__(self, other):
        if not isinstance(other, FileParserDecorator):
            raise TypeError('Trying to compare FileParserDecorator object with something else: %s' % type(other))
        return cmp(self.timestamp, other.timestamp)

    def fetch(self):
        self.timestamp, self.row = self.file_parser.next()


class BaseParseContoller(object):  # TODO: test this shit
    def __init__(self, pattern):
        self.pattern = re.compile(pattern)

    def parse(self, file_names, create_parser):
        parsers = []
        for file_name in file_names:
            file_parser = create_parser(file_name, self.pattern)
            decorator = FileParserDecorator(file_parser)
            decorator.fetch()
            parsers.append(decorator)

        heapq.heapify(parsers)
        while parsers:
            decorator = heapq.heappop(parsers)

            try:
                decorator.fetch()
                self.output(decorator.row)
                heapq.heappush(parsers, decorator)
            except StopIteration:
                pass

    def output(self, row):
        print row

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', help='regular expression, compatible with python re module')
    parser.add_argument('file_names', nargs='+')
    args = parser.parse_args()

    parser_creator = create_file_parser(SingleLineFileParser, SimpleRowParser('^\d+'))
    parser = BaseParseContoller(args.pattern)

    parser.parse(args.file_names, parser_creator)
