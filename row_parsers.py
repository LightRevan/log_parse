# -*- coding: utf-8 -*-

import re

class SimpleRowParser(object):
    def __init__(self, timestamp_pattern):
        self.timestamp_pattern = re.compile(timestamp_pattern)

    def parse_row(self, row):
        return {'timestamp': int(self.timestamp_pattern.search(row).group(0))}
