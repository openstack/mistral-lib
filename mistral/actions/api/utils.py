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

# TODO(rakhmerov): Add necessary utilities used by actions.


def get_action(name):
    """Gets an instance of action that can be executed on Mistral.

    Given a name this method builds an instance of a certain action
    that can be run in a regular way using Mistral execution mechanism
    (routing to an executor etc.) by calling its run() method.

    :param name: Action name.
    """

    # TODO(rakhmerov): Implement.
    raise NotImplementedError
