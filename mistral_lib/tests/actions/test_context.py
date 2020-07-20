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

    return context.ActionContext(security_ctx, execution_ctx)


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


class TestActionContextSerializer(tests_base.TestCase):

    def test_serialization(self):
        ctx = _fake_context()

        serialiser = context.ActionContextSerializer()

        dict_ctx = serialiser.serialize_to_dict(ctx)

        self.assertEqual(dict_ctx['security'], vars(ctx.security))
        self.assertEqual(dict_ctx['execution'], vars(ctx.execution))

    def test_deserialization(self):
        ctx = _fake_context()

        serialiser = context.ActionContextSerializer()

        dict_ctx = serialiser.serialize_to_dict(ctx)
        ctx_2 = serialiser.deserialize_from_dict(dict_ctx)

        self.assertEqual(ctx.security.auth_uri, ctx_2.security.auth_uri)
        self.assertEqual(
            ctx.execution.workflow_name,
            ctx_2.execution.workflow_name
        )
