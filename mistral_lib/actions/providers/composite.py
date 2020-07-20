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

from mistral_lib.actions import base


class CompositeActionProvider(base.ActionProvider):
    def __init__(self, name, delegates):
        super().__init__(name)

        self._delegates = delegates

    def find(self, action_name, namespace=None):
        for d in self._delegates:
            action_desc = d.find(action_name, namespace)

            if action_desc is not None:
                return action_desc

        return None

    def find_all(self, namespace=None, limit=None, sort_fields=None,
                 sort_dirs=None, **filters):
        # TODO(rakhmerov): Implement the algorithm that takes ordering/sorting
        # parameters into account correctly. For now, they are just passed to
        # delegates.
        res = []

        for d in self._delegates:
            action_descriptors = d.find_all(
                namespace=namespace,
                limit=limit,
                sort_fields=sort_fields,
                sort_dirs=sort_dirs,
                **filters
            )

            if action_descriptors is not None:
                res.extend(action_descriptors)

        return res

    def add_action_provider(self, action_provider):
        self._delegates.append(action_provider)
