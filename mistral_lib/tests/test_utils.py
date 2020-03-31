# Copyright 2013 - Mirantis, Inc.
# Copyright 2017 - Nokia Networks.
# Copyright 2017 - Red Hat, Inc.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import copy

from yaql.language import utils as yaql_utils

from mistral_lib.tests import base as tests_base
from mistral_lib import utils

import testtools.matchers as ttm


LEFT = {
    'key1': {
        'key11': "val11"
    },
    'key2': 'val2'
}

RIGHT = {
    'key1': {
        'key11': "val111111",
        'key12': "val12",
        'key13': {
            'key131': 'val131'
        }
    },
    'key2': 'val2222',
    'key3': 'val3'
}


class TestUtils(tests_base.TestCase):

    def test_merge_dicts(self):
        left = copy.deepcopy(LEFT)
        right = copy.deepcopy(RIGHT)

        expected = {
            'key1': {
                'key11': "val111111",
                'key12': "val12",
                'key13': {
                    'key131': 'val131'
                }
            },
            'key2': 'val2222',
            'key3': 'val3'
        }

        utils.merge_dicts(left, right)

        self.assertDictEqual(left, expected)

    def test_merge_dicts_overwrite_false(self):
        left = copy.deepcopy(LEFT)
        right = copy.deepcopy(RIGHT)

        expected = {
            'key1': {
                'key11': "val11",
                'key12': "val12",
                'key13': {
                    'key131': 'val131'
                }
            },
            'key2': 'val2',
            'key3': 'val3'
        }

        utils.merge_dicts(left, right, overwrite=False)

        self.assertDictEqual(left, expected)

    def test_itersubclasses(self):
        class A(object):
            pass

        class B(A):
            pass

        class C(A):
            pass

        class D(C):
            pass

        self.assertEqual([B, C, D], list(utils.iter_subclasses(A)))

    def test_get_dict_from_entries(self):
        input = ['param1', {'param2': 2}]
        input_dict = utils.get_dict_from_entries(input)

        self.assertIn('param1', input_dict)
        self.assertIn('param2', input_dict)
        self.assertEqual(2, input_dict.get('param2'))
        self.assertIs(input_dict.get('param1'), utils.NotDefined)

    def test_get_input_dict_from_string(self):
        self.assertDictEqual(
            {
                'param1': utils.NotDefined,
                'param2': 2,
                'param3': 'var3'
            },
            utils.get_dict_from_string('param1, param2=2, param3="var3"')
        )

        self.assertDictEqual({}, utils.get_dict_from_string(''))

    def test_cut_string(self):
        s = 'Hello, Mistral!'

        self.assertEqual('Hello...', utils.cut_string(s, length=5))
        self.assertEqual(s, utils.cut_string(s, length=100))
        self.assertEqual(s, utils.cut_string(s, length=-1))

    def test_cut_list(self):
        list_ = ['Hello, Mistral!', 'Hello, OpenStack!']

        self.assertEqual("['Hello, M...", utils.cut_list(list_, 13))
        self.assertEqual("['Hello, Mistr...", utils.cut_list(list_, 17))
        self.assertEqual(
            "['Hello, Mistral!', 'He...",
            utils.cut_list(list_, 26))

        self.assertEqual(
            "['Hello, Mistral!', 'Hello, OpenStack!']",
            utils.cut_list(list_, 100)
        )

        self.assertEqual(
            "['Hello, Mistral!', 'Hello, OpenStack!']",
            utils.cut_list(list_, -1)
        )

        self.assertEqual("[1, 2...", utils.cut_list([1, 2, 3, 4, 5], 8))
        self.assertEqual("[1, 2,...", utils.cut_list([1, 2, 3, 4, 5], 9))
        self.assertEqual("[1, 2, 3...", utils.cut_list([1, 2, 3, 4, 5], 11))

        self.assertRaises(ValueError, utils.cut_list, (1, 2))

    def test_cut_list_with_large_dict_of_str(self):
        d = [str(i) for i in range(65535)]
        s = utils.cut(d, 65535)
        self.assertThat(len(s), ttm.Not(ttm.GreaterThan(65535)))

    def test_cut_list_with_large_dict_of_int(self):
        d = [i for i in range(65535)]
        s = utils.cut(d, 65535)
        self.assertThat(len(s), ttm.Not(ttm.GreaterThan(65535)))

    def test_cut_list_with_large_dict_of_dict(self):
        d = [{'value': str(i)} for i in range(65535)]
        s = utils.cut(d, 65535)
        self.assertThat(len(s), ttm.Not(ttm.GreaterThan(65535)))

    def test_cut_list_for_state_info(self):
        d = [{'value': 'This is a string that exceeds 35 characters'}
             for i in range(2000)]
        s = utils.cut(d, 65500)
        self.assertThat(len(s), ttm.Not(ttm.GreaterThan(65500)))

    def test_cut_dict_with_strings(self):
        d = {'key1': 'value1', 'key2': 'value2'}

        s = utils.cut_dict(d, 13)

        self.assertIn(s, ["{'key1': '...", "{'key2': '..."])

        s = utils.cut_dict(d, 15)

        self.assertIn(s, ["{'key1': 'va...", "{'key2': 'va..."])

        s = utils.cut_dict(d, 22)

        self.assertIn(
            s,
            ["{'key1': 'value1', ...", "{'key2': 'value2', ..."]
        )

        self.assertIn(
            utils.cut_dict(d, 100),
            [
                "{'key1': 'value1', 'key2': 'value2'}",
                "{'key2': 'value2', 'key1': 'value1'}"
            ]
        )

        self.assertIn(
            utils.cut_dict(d, -1),
            [
                "{'key1': 'value1', 'key2': 'value2'}",
                "{'key2': 'value2', 'key1': 'value1'}"
            ]
        )

        self.assertRaises(ValueError, utils.cut_dict, (1, 2))

    def test_cut_dict_with_digits(self):
        d = {1: 2, 3: 4}

        s = utils.cut_dict(d, 10)

        self.assertIn(s, ["{1: 2, ...", "{3: 4, ..."])

        s = utils.cut_dict(d, 11)

        self.assertIn(s, ["{1: 2, 3...", "{3: 4, 1..."])

        s = utils.cut_dict(d, 100)

        self.assertIn(s, ["{1: 2, 3: 4}", "{3: 4, 1: 2}"])

    def test_cut_dict_with_large_dict_of_str(self):
        d = {}
        for i in range(65535):
            d[str(i)] = str(i)
        s = utils.cut(d, 65535)
        self.assertThat(len(s), ttm.Not(ttm.GreaterThan(65535)))

    def test_cut_dict_with_large_dict_of_int(self):
        d = {}
        for i in range(65535):
            d[i] = i
        s = utils.cut(d, 65535)
        self.assertThat(len(s), ttm.Not(ttm.GreaterThan(65535)))

    def test_cut_dict_with_large_dict_of_dict(self):
        d = {}
        for i in range(65535):
            d[i] = {'value': str(i)}
        s = utils.cut(d, 65535)
        self.assertThat(len(s), ttm.Not(ttm.GreaterThan(65535)))

    def test_cut_dict_for_state_info(self):
        d = {}
        for i in range(2000):
            d[i] = {'value': 'This is a string that exceeds 35 characters'}
        s = utils.cut(d, 65500)
        self.assertThat(len(s), ttm.Not(ttm.GreaterThan(65500)))

    def test_mask_data(self):
        payload = {'adminPass': 'fooBarBaz'}
        expected = {'adminPass': '***'}
        self.assertEqual(expected, utils.mask_data(payload))

        payload = """adminPass='fooBarBaz'"""
        expected = """adminPass='***'"""
        self.assertEqual(expected, utils.mask_data(payload))

        payload = [{'adminPass': 'fooBarBaz'}, {"new_pass": "blah"}]
        expected = [{'adminPass': '***'}, {"new_pass": "***"}]
        self.assertEqual(expected, utils.mask_data(payload))

        payload = ["adminPass", 'fooBarBaz']
        expected = ["adminPass", 'fooBarBaz']
        self.assertEqual(expected, utils.mask_data(payload))

    def test_json_serialize_frozen_dict(self):
        data = yaql_utils.FrozenDict(a=1, b=2, c=iter([1, 2, 3]))

        json_str = utils.to_json_str(data)

        self.assertIsNotNone(json_str)

        self.assertIn('"a": 1', json_str)
        self.assertIn('"b": 2', json_str)
        self.assertIn('"c": [1, 2, 3]', json_str)

    def test_json_serialize_generator(self):
        def _list_stream(_list):
            for i in _list:
                yield i

        gen = _list_stream(
            [1, yaql_utils.FrozenDict(a=1), _list_stream([12, 15])]
        )

        self.assertEqual('[1, {"a": 1}, [12, 15]]', utils.to_json_str(gen))

    def test_json_serialize_dict_of_generators(self):
        def _f(cnt):
            for i in range(1, cnt + 1):
                yield i

        data = {'numbers': _f(3)}

        self.assertEqual('{"numbers": [1, 2, 3]}', utils.to_json_str(data))

    def test_json_serialize_range(self):
        self.assertEqual("[1, 2, 3, 4]", utils.to_json_str(range(1, 5)))

    def test_json_serialize_iterator_of_frozen_dicts(self):
        data = iter(
            [
                yaql_utils.FrozenDict(a=1, b=2, c=iter([1, 2, 3])),
                yaql_utils.FrozenDict(
                    a=11,
                    b=yaql_utils.FrozenDict(b='222'),
                    c=iter(
                        [
                            1,
                            yaql_utils.FrozenDict(
                                a=iter([4, yaql_utils.FrozenDict(a=99)])
                            )
                        ]
                    )
                )
            ]
        )

        json_str = utils.to_json_str(data)

        self.assertIsNotNone(json_str)

        # Checking the first item.
        self.assertIn('"a": 1', json_str)
        self.assertIn('"b": 2', json_str)
        self.assertIn('"c": [1, 2, 3]', json_str)

        # Checking the first item.
        self.assertIn('"a": 11', json_str)
        self.assertIn('"b": {"b": "222"}', json_str)
        self.assertIn('"c": [1, {"a": [4, {"a": 99}]}]', json_str)
