# Copyright 2020 Nokia Software.
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

import abc
import copy

from mistral_lib import actions
from mistral_lib import exceptions as exc
from mistral_lib import utils


def _compare_parameters(expected_params, actual_params):
    """Compares the expected parameters with the actual parameters.

    :param expected_params: Expected dict of parameters.
    :param actual_params: Actual dict of parameters.
    :return: Tuple {missing parameter names, unexpected parameter names}
    """

    missing_params = []
    unexpected_params = copy.deepcopy(list((actual_params or {}).keys()))

    for p_name, p_value in expected_params.items():
        if p_value is utils.NotDefined and p_name not in unexpected_params:
            missing_params.append(str(p_name))

        if p_name in unexpected_params:
            unexpected_params.remove(p_name)

    return missing_params, unexpected_params


class ActionDescriptorBase(actions.ActionDescriptor, abc.ABC):
    def __init__(self, name, desc, params_spec, namespace=None,
                 project_id=None, scope=None):
        self._name = name
        self._desc = desc
        self._params_spec = params_spec
        self._namespace = namespace
        self._project_id = project_id
        self._scope = scope

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._desc

    @property
    def params_spec(self):
        return self._params_spec

    @property
    def namespace(self):
        return self._namespace

    @property
    def project_id(self):
        return self._project_id

    @property
    def scope(self):
        return self._scope

    @property
    def action_class_name(self):
        return None

    @property
    def action_class_attributes(self):
        return None

    def check_parameters(self, params):
        # Don't validate action input if action initialization
        # method contains ** argument.
        if '**' in self.params_spec:
            return

        expected_params = utils.get_dict_from_string(self.params_spec)

        actual_params = params or {}

        missing, unexpected = _compare_parameters(
            expected_params,
            actual_params
        )

        if missing or unexpected:
            msg = 'Invalid input [name=%s, class=%s'
            msg_props = [self.name, self.action_class_name]

            if missing:
                msg += ', missing=%s'
                msg_props.append(missing)

            if unexpected:
                msg += ', unexpected=%s'
                msg_props.append(unexpected)

            msg += ']'

            raise exc.ActionException(msg % tuple(msg_props))

    def post_process_result(self, result):
        return result
