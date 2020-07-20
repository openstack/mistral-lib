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

from mistral_lib import actions
from mistral_lib.actions.providers import python
from mistral_lib.tests import base as tests_base


class HelloAction(actions.Action):
    """I help with testing."""

    def __init__(self, f_name, l_name):
        super(HelloAction, self).__init__()

        self._f_name = f_name
        self._l_name = l_name

    def run(self, context):
        return 'Hello %s %s!' % (self._f_name, self._l_name)


class TestActionProvider(actions.ActionProvider):
    def __init__(self, name):
        super(TestActionProvider, self).__init__(name)

        self.action_descs = {}

    def add_action_descriptor(self, action_desc):
        self.action_descs[action_desc.name] = action_desc

    def find(self, action_name, namespace=None):
        return self.action_descs.get(action_name)

    def find_all(self, namespace=None, limit=None, sort_fields=None,
                 sort_dirs=None, **filters):
        return self.action_descs.values()


class TestActionProviders(tests_base.TestCase):
    def test_python_action_descriptor(self):
        action_desc = python.PythonActionDescriptor('test_action', HelloAction)

        # Check descriptor attributes.
        self.assertEqual('test_action', action_desc.name)
        self.assertEqual(HelloAction, action_desc.action_class)
        self.assertEqual(
            HelloAction.__module__ + '.' + HelloAction.__name__,
            action_desc.action_class_name
        )
        self.assertIsNone(action_desc.action_class_attributes)
        self.assertEqual('I help with testing.', action_desc.description)
        self.assertEqual('f_name, l_name', action_desc.params_spec)

        # Instantiate the action and check how it works.
        action = action_desc.instantiate(
            {'f_name': 'Jhon', 'l_name': 'Doe'},
            {}
        )

        res = action.run(None)

        self.assertEqual('Hello Jhon Doe!', res)

    def test_composite_action_provider(self):
        # Check empty provider.
        composite_provider = actions.CompositeActionProvider('test', [])

        self.assertEqual(0, len(composite_provider.find_all()))

        # Add two test providers.
        provider1 = TestActionProvider('provider1')

        action_desc1 = python.PythonActionDescriptor('action1', HelloAction)
        action_desc2 = python.PythonActionDescriptor('action2', HelloAction)
        action_desc3 = python.PythonActionDescriptor('action3', HelloAction)
        action_desc4 = python.PythonActionDescriptor('action4', HelloAction)

        provider1.add_action_descriptor(action_desc1)
        provider1.add_action_descriptor(action_desc2)

        provider2 = TestActionProvider('provider2')

        provider2.add_action_descriptor(action_desc3)
        provider2.add_action_descriptor(action_desc4)

        composite_provider = actions.CompositeActionProvider(
            'test',
            [provider1, provider2]
        )

        self.assertEqual(4, len(composite_provider.find_all()))

        self.assertEqual(action_desc1, composite_provider.find('action1'))
        self.assertEqual(action_desc2, composite_provider.find('action2'))
        self.assertEqual(action_desc3, composite_provider.find('action3'))
        self.assertEqual(action_desc4, composite_provider.find('action4'))
