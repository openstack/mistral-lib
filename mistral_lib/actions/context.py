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

    @property
    def auth_uri(self):
        self._deprecation_warning("auth_uri")
        return self.security.auth_uri

    @property
    def user_name(self):
        self._deprecation_warning("user_name")
        return self.security.user_name

    @property
    def auth_token(self):
        self._deprecation_warning("auth_token")
        return self.security.auth_token

    @property
    def project_name(self):
        self._deprecation_warning("project_name")
        return self.security.project_name

    @property
    def project_id(self):
        self._deprecation_warning("project_id")
        return self.security.project_id

    @property
    def insecure(self):
        self._deprecation_warning("insecure")
        return self.security.insecure


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
    def __init__(self, workflow_execution_id=None, task_id=None,
                 action_execution_id=None, workflow_name=None,
                 callback_url=None):
        self.workflow_execution_id = workflow_execution_id
        self.task_id = task_id
        self.action_execution_id = action_execution_id
        self.workflow_name = workflow_name
        self.callback_url = callback_url
