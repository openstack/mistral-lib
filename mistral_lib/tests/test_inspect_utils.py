# Copyright 2014 - Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import time

from mistral_lib import actions
from mistral_lib.tests import base
from mistral_lib.utils import inspect_utils as i_u


class DummyHTTPAction(actions.Action):
    def __init__(self,
                 url,
                 method="GET",
                 params=None,
                 body=None,
                 headers=None,
                 cookies=None,
                 auth=None,
                 timeout=None,
                 allow_redirects=None,
                 proxies=None,
                 verify=None):
        super(DummyHTTPAction, self).__init__()

    def run(self, context):
        return context


class DummyRunTask(object):
    def __init__(self, wf_ex, wf_spec, task_spec, ctx, triggered_by=None,
                 handles_error=False):
        pass


class ClassWithProperties(object):

    a = 1

    @property
    def prop(self):
        pass


class InspectUtilsTest(base.TestCase):
    def test_get_parameters_str(self):
        action_class = DummyHTTPAction
        parameters_str = i_u.get_arg_list_as_str(action_class.__init__)

        http_action_params = (
            'url, method="GET", params=null, body=null, '
            'headers=null, cookies=null, auth=null, '
            'timeout=null, allow_redirects=null, '
            'proxies=null, verify=null'
        )

        self.assertEqual(http_action_params, parameters_str)

    def test_get_parameters_str_all_mandatory(self):
        clazz = DummyRunTask
        parameters_str = i_u.get_arg_list_as_str(clazz.__init__)

        self.assertEqual(
            'wf_ex, wf_spec, task_spec, ctx, triggered_by=null,'
            ' handles_error=false',
            parameters_str
        )

    def test_get_parameters_str_with_function_parameter(self):

        def test_func(foo, bar=None, test_func=time.sleep):
            pass

        parameters_str = i_u.get_arg_list_as_str(test_func)

        self.assertEqual("foo, bar=null", parameters_str)

    def test_get_public_fields(self):

        attrs = i_u.get_public_fields(ClassWithProperties)

        self.assertEqual(attrs, {'a': 1})
