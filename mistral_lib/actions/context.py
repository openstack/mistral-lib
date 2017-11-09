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

import warnings


class ActionContext(object):

    def __init__(self, security_ctx=None, execution_ctx=None):
        self.security = security_ctx
        self.execution = execution_ctx

    def _deprecation_warning(self, name):
        warnings.warn(
            "context.{0} is deprecated from the context passed to actions. "
            "Please use context.security.{0}. It will be removed in a future "
            "release.", DeprecationWarning
        )

    def __getattribute__(self, name):
        deprecated = [
            "auth_cacert", "auth_token", "auth_uri", "expires_at", "insecure",
            "is_target", "is_trust_scoped", "project_id", "project_name",
            "redelivered", "region_name", "service_catalog", "trust_id",
            "user_name"
        ]
        if name in deprecated:
            self._deprecation_warning(name)
            return getattr(self.security, name)
        return super(ActionContext, self).__getattribute__(name)


class SecurityContext(object):
    def __init__(self, auth_uri=None, auth_cacert=None, insecure=None,
                 service_catalog=None, region_name=None, is_trust_scoped=None,
                 redelivered=None, expires_at=None, trust_id=None,
                 is_target=None, project_id=None, project_name=None,
                 user_name=None, auth_token=None):
        self.auth_uri = auth_uri
        self.auth_cacert = auth_cacert
        self.insecure = insecure
        self.service_catalog = service_catalog
        self.region_name = region_name
        self.is_trust_scoped = is_trust_scoped
        self.redelivered = redelivered
        self.expires_at = expires_at
        self.trust_id = trust_id
        self.is_target = is_target
        self.project_id = project_id
        self.project_name = project_name
        self.user_name = user_name
        self.auth_token = auth_token


class ExecutionContext(object):
    def __init__(self, workflow_execution_id=None, task_execution_id=None,
                 action_execution_id=None, workflow_name=None,
                 callback_url=None, task_id=None):
        self.workflow_execution_id = workflow_execution_id
        self.task_execution_id = task_execution_id
        self.action_execution_id = action_execution_id
        self.workflow_name = workflow_name
        self.callback_url = callback_url

        if task_id is not None:
            self.task_execution_id = task_id
            self._deprecate_task_id_warning()

    def _deprecate_task_id_warning(self):
        warnings.warn(
            "context.execution.task_id was deprecated in the Queens cycle. "
            "Please use context.execution.task_execution_id. It will be "
            "removed in a future release.", DeprecationWarning
        )

    @property
    def task_id(self):
        self._deprecate_task_id_warning()
        return self.task_execution_id
