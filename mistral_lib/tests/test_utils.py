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
from mistral_lib.tests import base as tests_base
from mistral_lib import utils


class TestUtils(tests_base.TestCase):

    def test_cut_string(self):
        s = 'Hello, Mistral!'

        self.assertEqual('Hello...', utils.cut_string(s, length=5))
        self.assertEqual(s, utils.cut_string(s, length=100))

    def test_cut_list(self):
        l = ['Hello, Mistral!', 'Hello, OpenStack!']

        self.assertEqual("['Hello, M...", utils.cut_list(l, 11))
        self.assertEqual("['Hello, Mistr...", utils.cut_list(l, 15))
        self.assertEqual("['Hello, Mistral!', 'He...", utils.cut_list(l, 24))

        self.assertEqual(
            "['Hello, Mistral!', 'Hello, OpenStack!']",
            utils.cut_list(l, 100)
        )

        self.assertEqual("[1, 2...", utils.cut_list([1, 2, 3, 4, 5], 4))
        self.assertEqual("[1, 2...", utils.cut_list([1, 2, 3, 4, 5], 5))
        self.assertEqual("[1, 2, 3...", utils.cut_list([1, 2, 3, 4, 5], 6))

        self.assertRaises(ValueError, utils.cut_list, (1, 2))

    def test_cut_dict_with_strings(self):
        d = {'key1': 'value1', 'key2': 'value2'}

        s = utils.cut_dict(d, 9)

        self.assertIn(s, ["{'key1': '...", "{'key2': '..."])

        s = utils.cut_dict(d, 13)

        self.assertIn(s, ["{'key1': 'va...", "{'key2': 'va..."])

        s = utils.cut_dict(d, 19)

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

    def test_cut_dict_with_digits(self):
        d = {1: 2, 3: 4}

        s = utils.cut_dict(d, 6)

        self.assertIn(s, ["{1: 2, ...", "{3: 4, ..."])

        s = utils.cut_dict(d, 8)

        self.assertIn(s, ["{1: 2, 3...", "{3: 4, 1..."])

        s = utils.cut_dict(d, 100)

        self.assertIn(s, ["{1: 2, 3: 4}", "{3: 4, 1: 2}"])
