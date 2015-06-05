# -*- coding: utf-8 -*-

import unittest

from log_parser.searchers import *


class SQLSearcherTestCase(unittest.TestCase):
    def test_1(self):
        input = [('1 T1 asdasdsad', {'timestamp': 1, 'thread': 'T1', 'match': None}),
                 ('2 T1 asdasdsad', {'timestamp': 2, 'thread': 'T1', 'match': None}),
                 ('3 T1 SELECT * FROM trtrtr', {'timestamp': 3, 'thread': 'T1', 'match': None}),
                 ('4 T1 {\'id\': 123456}', {'timestamp': 4, 'thread': 'T1', 'match': '123456'}),
                 ('5 T1 asdasdsad', {'timestamp': 5, 'thread': 'T1', 'match': None}),
                 ('6 T1 asdasdsad', {'timestamp': 6, 'thread': 'T1', 'match': None})]
        required_result = ['3 T1 SELECT * FROM trtrtr', '4 T1 {\'id\': 123456}']

        tested = SimpleSQLSearcher(iter(input), SimpleSQLSearchInstance, 'id')
        result = [row for row in tested]

        self.assertEqual(result, required_result)

    def test_2(self):
        input = [('1 T1 asdasdsad', {'timestamp': 1, 'thread': 'T1', 'match': None}),
                 ('2 T1 asdasdsad', {'timestamp': 2, 'thread': 'T1', 'match': None}),
                 ('3 T1 SELECT * FROM trtrtr', {'timestamp': 3, 'thread': 'T1', 'match': None}),
                 ('4 T1 {\'id\': 123456}', {'timestamp': 4, 'thread': 'T1', 'match': '123456'}),
                 ('5 T1 asdasdsad', {'timestamp': 5, 'thread': 'T1', 'match': None}),
                 ('6 T1 asdasdsad', {'timestamp': 6, 'thread': 'T1', 'match': None})]
        required_result = ['3 T1 SELECT * FROM trtrtr', '4 T1 {\'id\': 123456}']

        tested = SimpleSQLSearcher(iter(input), SimpleSQLSearchInstance)
        result = [row for row in tested]

        self.assertEqual(result, required_result)

    def test_3(self):
        input = [('1 T1 SELECT * FROM trtrtr', {'timestamp': 1, 'thread': 'T1', 'match': None}),
                 ('2 T1 asdasdsad', {'timestamp': 2, 'thread': 'T1', 'match': None}),
                 ('3 T1 asdasdsad', {'timestamp': 3, 'thread': 'T1', 'match': None}),
                 ('4 T1 {\'id\': 123456}', {'timestamp': 4, 'thread': 'T1', 'match': '123456'}),
                 ('5 T1 asdasdsad', {'timestamp': 5, 'thread': 'T1', 'match': None}),
                 ('6 T1 asdasdsad', {'timestamp': 6, 'thread': 'T1', 'match': None})]
        required_result = ['1 T1 SELECT * FROM trtrtr', '4 T1 {\'id\': 123456}']

        tested = SimpleSQLSearcher(iter(input), SimpleSQLSearchInstance)
        result = [row for row in tested]

        self.assertEqual(result, required_result)

    def test_4(self):
        input = [('1 T1 asdasdsad', {'timestamp': 1, 'thread': 'T1', 'match': None}),
                 ('2 T1 asdasdsad', {'timestamp': 2, 'thread': 'T1', 'match': None}),
                 ('3 T1 {\'id\': 123456}', {'timestamp': 3, 'thread': 'T1', 'match': '123456'}),
                 ('4 T1 asdasdsad', {'timestamp': 4, 'thread': 'T1', 'match': None}),
                 ('5 T1 asdasdsad', {'timestamp': 5, 'thread': 'T1', 'match': None}),
                 ('6 T1 SELECT * FROM trtrtr', {'timestamp': 6, 'thread': 'T1', 'match': None}),]
        required_result = []

        tested = SimpleSQLSearcher(iter(input), SimpleSQLSearchInstance)
        result = [row for row in tested]

        self.assertEqual(result, required_result)

    def test_5(self):
        input = [('1 T1 SELECT * FROM trtrtr', {'timestamp': 1, 'thread': 'T1', 'match': None}),
                 ('2 T1 asdasdsad', {'timestamp': 2, 'thread': 'T1', 'match': None}),
                 ('3 T1 SELECT * FROM brbrbrr', {'timestamp': 3, 'thread': 'T1', 'match': None}),
                 ('4 T1 {\'id\': 123456}', {'timestamp': 4, 'thread': 'T1', 'match': '123456'}),
                 ('5 T1 asdasdsad', {'timestamp': 5, 'thread': 'T1', 'match': None}),
                 ('6 T1 asdasdsad', {'timestamp': 6, 'thread': 'T1', 'match': None})]
        required_result = ['3 T1 SELECT * FROM brbrbrr', '4 T1 {\'id\': 123456}']

        tested = SimpleSQLSearcher(iter(input), SimpleSQLSearchInstance)
        result = [row for row in tested]

        self.assertEqual(result, required_result)

    def test_6(self):
        input = [('1 T1 asdasdsad', {'timestamp': 1, 'thread': 'T1', 'match': None}),
                 ('2 T1 asdasdsad', {'timestamp': 2, 'thread': 'T1', 'match': None}),
                 ('3 T1 SELECT * FROM trtrtr', {'timestamp': 3, 'thread': 'T1', 'match': None}),
                 ('4 T1 {\'id\': 123456}', {'timestamp': 4, 'thread': 'T1', 'match': '123456'}),
                 ('5 T1 asdasdsad', {'timestamp': 5, 'thread': 'T1', 'match': None}),
                 ('6 T1 asdasdsad', {'timestamp': 6, 'thread': 'T1', 'match': None})]
        required_result = []

        tested = SimpleSQLSearcher(iter(input), SimpleSQLSearchInstance, 'figvam')
        result = [row for row in tested]

        self.assertEqual(result, required_result)