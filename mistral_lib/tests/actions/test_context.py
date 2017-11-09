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

from mistral_lib.actions import context
from mistral_lib.tests import base as tests_base


def _fake_context():
        security_ctx = context.SecurityContext(
            auth_uri='auth_uri',
            auth_cacert='auth_cacert',
            insecure='insecure',
            service_catalog='service_catalog',
            region_name='region_name',
            is_trust_scoped='is_trust_scoped',
            redelivered='redelivered',
            expires_at='expires_at',
            trust_id='trust_id',
            is_target='is_target',
            project_id='project_id')

        execution_ctx = context.ExecutionContext(
            workflow_execution_id='workflow_execution_id',
            task_execution_id='task_execution_id',
            action_execution_id='action_execution_id',
            workflow_name='workflow_name',
            callback_url='callback_url')

        ctx = context.ActionContext(security_ctx, execution_ctx)
        return ctx


class TestActionsBase(tests_base.TestCase):

    def test_empty_context(self):

        ctx = context.ActionContext(
            context.SecurityContext(),
            context.ExecutionContext()
        )

        self.assertIsInstance(ctx.security, context.SecurityContext)
        self.assertIsInstance(ctx.execution, context.ExecutionContext)

        self.assertEqual(ctx.security.auth_uri, None)
        self.assertEqual(ctx.execution.workflow_name, None)

    def test_deprecated_properties(self):

        ctx = _fake_context()

        deprecated_properties = [
            'auth_cacert', 'auth_token', 'auth_uri', 'expires_at',
            'insecure', 'is_target', 'is_trust_scoped', 'project_id',
            'project_name', 'redelivered', 'region_name', 'service_catalog',
            'trust_id', 'user_name'
        ]

        for deprecated in deprecated_properties:
            old = getattr(ctx, deprecated)
            new = getattr(ctx.security, deprecated)
            self.assertEqual(old, new)
