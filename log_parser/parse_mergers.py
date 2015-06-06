# -*- coding: utf-8 -*-
__author__ = 'lightrevan'

import argparse
import heapq

from file_parsers import *
from row_parsers import *


class FileParserDecorator(object):
    def __init__(self, file_parser):
        self.file_parser = file_parser
        self.timestamp = None
        self.row = None
        self.row_params = None

    def __cmp__(self, other):
        if not isinstance(other, FileParserDecorator):
            raise TypeError('Trying to compare FileParserDecorator object with something else: %s' % type(other))
        return cmp(self.timestamp, other.timestamp)

    def fetch(self):
        self.row, self.row_params = self.file_parser.next()
        self.timestamp = self.row_params['timestamp']

class BaseParseOutputMerger(object):
    def __init__(self, pattern):
        self.pattern = re.compile(pattern)

    def parse(self, files, file_parser_cls, row_parser_cls, row_getter_cls):
        parsers = []
        for f in files:
            row_parser = row_parser_cls(self.pattern)
            row_getter = row_getter_cls(f, row_parser)
            file_parser = file_parser_cls(row_getter)

            decorator = FileParserDecorator(file_parser)
            decorator.fetch()
            parsers.append(decorator)

        heapq.heapify(parsers)
        while parsers:
            decorator = heapq.heappop(parsers)

            try:
                yield self.output(decorator.row, decorator.row_params)
                decorator.fetch()
                heapq.heappush(parsers, decorator)
            except StopIteration:
                pass

    def output(self, row, row_params):
        # TODO: need to save information about what file produced what row
        # TODO: to separate by threads AND files later
        return (row, row_params)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', help='regular expression, compatible with python re module')
    parser.add_argument('file_names', nargs='+')
    args = parser.parse_args()

    row_pattern = '^(?P<timestamp>[0-9\-]{8} [0-9:,]+) (?P<thread>(?:P\d+ )?T\d+)'
    transforms = {'timestamp': date_transform}
    row_parser_creator = functools.partial(SinglePatternRowParser, row_pattern=row_pattern, group_transforms=transforms)
    row_getter_creator = MergingRowGetter
    file_parser_creator = functools.partial(MultiThreadBlobbingContextFileParser, context_size=100)

    parser = BaseParseOutputMerger(args.pattern)

    for row, row_params in parser.parse(args.file_names, file_parser_creator, row_parser_creator, row_getter_creator):
        print row
