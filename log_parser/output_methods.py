# -*- coding: utf-8 -*-
__author__ = 'lightrevan'

def print_output(row, row_params):
    print row


class ListOutput(object):
    def __init__(self):
        self.data = []

    def __call__(self, row, row_params):
        self.data.append(row)