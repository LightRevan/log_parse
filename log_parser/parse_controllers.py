# -*- coding: utf-8 -*-
__author__ = 'lightrevan'

import argparse
import heapq

from file_parsers import *
from row_parsers import *
from output_methods import *


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

class BaseParseContoller(object):  # TODO: test this shit
    def __init__(self, pattern, output_method=print_output):
        self.pattern = re.compile(pattern)
        self.output_method = output_method

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
                self.output(decorator.row, decorator.row_params)
                decorator.fetch()
                heapq.heappush(parsers, decorator)
            except StopIteration:
                pass

    def output(self, row, row_params):
        self.output_method(row, row_params)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', help='regular expression, compatible with python re module')
    parser.add_argument('file_names', nargs='+')
    args = parser.parse_args()

    row_pattern = '^(?P<timestamp>[0-9\-]{8} [0-9:,]+) (?P<thread>(?:P\d+ )?T\d+)'
    transforms = {'timestamp': date_transform}
    row_parser_creator = functools.partial(SinglePatternRowParser, row_pattern=row_pattern, group_transforms=transforms)
    file_parser_creator = create_file_parser(row_parser_creator, MergingRowGetter)

    parser = BaseParseContoller(args.pattern)

    parser.parse(args.file_names, file_parser_creator)
