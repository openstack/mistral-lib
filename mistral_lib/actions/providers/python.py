# Copyright 2020 Nokia Software.
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

from mistral_lib.actions.providers import base
from mistral_lib.utils import inspect_utils as i_utils


class PythonActionDescriptor(base.ActionDescriptorBase):
    def __init__(self, name, action_cls, action_cls_attrs=None, namespace=None,
                 project_id=None, scope=None):
        super(PythonActionDescriptor, self).__init__(
            name,
            i_utils.get_docstring(action_cls),
            i_utils.get_arg_list_as_str(action_cls.__init__),
            namespace,
            project_id,
            scope
        )

        self._action_cls = action_cls
        self._action_cls_attrs = action_cls_attrs

    def __repr__(self):
        return 'Python action [name=%s, cls=%s]' % (
            self.name,
            self._action_cls
        )

    def instantiate(self, params, wf_ctx):
        if not self._action_cls_attrs:
            # No need to create new dynamic type.
            return self._action_cls(**params)

        dynamic_cls = type(
            self._action_cls.__name__,
            (self._action_cls,),
            self._action_cls_attrs
        )

        return dynamic_cls(**params)

    @property
    def action_class(self):
        return self._action_cls

    @property
    def action_class_name(self):
        return "{}.{}".format(
            self._action_cls.__module__,
            self._action_cls.__name__
        )

    @property
    def action_class_attributes(self):
        return self._action_cls_attrs
