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
