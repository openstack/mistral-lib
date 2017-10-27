# Copyright 2017 Red Hat, Inc.
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
from mistral_lib import actions
from mistral_lib.actions import context
from mistral_lib.tests import base as tests_base


class TestAction(actions.Action):

    def run(self, context):
        return context


class TestActionsBase(tests_base.TestCase):

    def test_run_empty_context(self):
        ctx = context.ActionContext()
        action = TestAction()
        result = action.run(ctx)
        assert result == ctx
