# Copyright 2016 - Nokia Networks.
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

# TODO(rakhmerov): Add functions to get current execution info.


def get_workflow_name():
    raise NotImplementedError


def get_workflow_execution_id():
    raise NotImplementedError


def get_task_name():
    raise NotImplementedError


def get_task_tags():
    raise NotImplementedError


def get_task_execution_id():
    raise NotImplementedError


def get_action_name():
    raise NotImplementedError


def get_action_execution_id():
    raise NotImplementedError


def get_mistral_callback_url():
    raise NotImplementedError
