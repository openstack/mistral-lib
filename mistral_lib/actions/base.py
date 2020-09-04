# Copyright 2016 - Nokia Networks.
# Copyright 2017 - Red Hat, Inc.
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

import abc

from oslo_utils import importutils

from mistral_lib import serialization
from mistral_lib.utils import inspect_utils as i_utils


class Action(serialization.MistralSerializable):
    """Action.

    Action is a means in Mistral to perform some useful work associated with
    a workflow during its execution. Every workflow task is configured with
    an action and when the task runs it eventually delegates to the action.
    When it happens task parameters get evaluated (calculating expressions,
    if any) and are treated as action parameters. So in a regular general
    purpose languages terminology action is a method declaration and task is
    a method call.

    Base action class initializer doesn't have arguments. However, concrete
    action classes may have any number of parameters defining action behavior.
    These parameters must correspond to parameters declared in action
    specification (e.g. using DSL or others).
    """

    def __init__(self):
        # NOTE(d0ugal): We need to define an empty __init__ otherwise
        # inspect.getargspec will fail in Python 2 for actions that subclass
        # but don't define their own __init__.
        pass

    @abc.abstractmethod
    def run(self, context):
        """Run action logic.

        :param context: contains contextual information of the action.
        The context includes an execution context (like execution identifier
        and workflow name) and a security context with the authorization
        details.
        :return: Result of the action. Note that for asynchronous actions
        it should always be None, however, if even it's not None it will be
        ignored by a caller.

        Result can be of two types:
        1) Any serializable value meaningful from a user perspective (such
        as string, number or dict).
        2) Instance of {mistral_lib.types.Result} which has field "data"
        for success result and field "error" for keeping so called "error
        result" like HTTP error code and similar. Using the second type
        allows to communicate a result even in case of error and hence to have
        conditions in "on-error" clause of direct workflows. Depending on
        particular action semantics one or another option may be preferable.
        In case if action failed and there's no need to communicate any error
        result this method should throw a ActionException.
        """
        pass

    def is_sync(self):
        """Returns True if the action is synchronous, otherwise False.

        :return: True if the action is synchronous and method run() returns
            final action result. Otherwise returns False which means that
            a result of method run() should be ignored and a real action
            result is supposed to be delivered in an asynchronous manner
            using public API. By default, if a concrete implementation
            doesn't override this method then the action is synchronous.
        """
        return True

    @classmethod
    def get_serialization_key(cls):
        # By default we use the same serializer key for every action
        # assuming that most action class can use the same serializer.
        return "%s.%s" % (Action.__module__, Action.__name__)


class ActionSerializer(serialization.DictBasedSerializer):
    def serialize_to_dict(self, entity):
        cls = type(entity)

        return {
            'cls': '%s.%s' % (cls.__module__, cls.__name__),
            'cls_attrs': i_utils.get_public_fields(cls),
            'data': vars(entity),
        }

    def deserialize_from_dict(self, entity_dict):
        cls_str = entity_dict['cls']

        # Rebuild action class and restore attributes.
        cls = importutils.import_class(cls_str)

        cls_attrs = entity_dict['cls_attrs']

        if cls_attrs:
            # If we have serialized class attributes it means that we need
            # to create a dynamic class.
            cls = type(cls.__name__, (cls,), cls_attrs)

        # NOTE(rakhmerov): We use this hacky was of instantiating
        # the action here because we can't use normal __init__(),
        # we don't know the parameters. And even if we find out
        # what they are the real internal state of the object is
        # what was stored as vars() method that just returns all
        # fields. So we have to bypass __init__() and set attributes
        # one by one. Of course, this is a serious limitation since
        # action creators will need to keep in mind to avoid having
        # some complex initialisation logic in __init__() that
        # does something not reflecting in an instance state.
        # However, this all applies to the case when the action
        # has to be sent to a remote executor.
        action = cls.__new__(cls)

        for k, v in entity_dict['data'].items():
            setattr(action, k, v)

        return action


# NOTE: Every action implementation can register its own serializer
# if needed, but this serializer should work for vast of majority of
# actions.
serialization.register_serializer(Action, ActionSerializer())


class ActionDescriptor(abc.ABC):
    """Provides required information about a certain type of actions.

    Action descriptor is not an action itself. It rather carries all
    important meta information about a particular action before the
    action is instantiated. In some sense it is similar to a class but
    the difference is that one type of action descriptor may support
    many different actions. This abstraction is responsible for
    validation of input parameters and instantiation of an action.

    """

    @property
    @abc.abstractmethod
    def name(self):
        """The name of the action."""
        pass

    @property
    @abc.abstractmethod
    def description(self):
        """The description of the action."""
        pass

    @property
    @abc.abstractmethod
    def params_spec(self):
        """Comma-separated string with input parameter names.

        Each parameter name can be either just a name or a string
        "param=val" where "param" is the name of the parameter
        and "val" its default value. The values are only indications
        for the user and not used in the action instantiation process.
        The string is split along the commas and then the parts along the
        equal signs. Escaping is not possible.
        """
        pass

    @property
    @abc.abstractmethod
    def namespace(self):
        """The namespace of the action.

        NOTE: Not all actions have to support namespaces.
        """
        pass

    @property
    @abc.abstractmethod
    def project_id(self):
        """The ID of the project (tenant) this action belongs to.

        If it's not specified then the action can be used within
        all projects (tenants).

        NOTE: Not all actions have to support projects(tenants).
        """
        pass

    @property
    @abc.abstractmethod
    def scope(self):
        """The scope of the action within a project (tenant).

        It makes sense only if the "project_id" property is not None.
        It should be assigned with the "public" value if the action
        is available in all projects and "private" if it's accessible
        only by users of the specified project.

        NOTE: Not all actions have to support projects(tenants).
        """
        pass

    @property
    @abc.abstractmethod
    def action_class_name(self):
        """String representation of the Python class of the action.

        Can be None in case if the action is dynamically generated with
        some kind of wrapper.
        """
        pass

    @property
    @abc.abstractmethod
    def action_class_attributes(self):
        """The attributes of the action Python class, if relevant.

        If the action has a static Python class associated with it
        and this method returns not an empty dictionary then the
        action can be instantiated from a new dynamic class
        based on the property "action_class_string" and this property
        that essentially carries public class field values.
        """
        pass

    @abc.abstractmethod
    def instantiate(self, input_dict, wf_ctx):
        """Instantiate the required action with the given parameters.

        :param input_dict: Action parameters as a dictionary where keys
            are parameter names and values are parameter values.
        :param wf_ctx: Workflow context relevant for the point when
            action is about to start.
        :return: An instance of mistral_lib.actions.Action.
        """
        pass

    @abc.abstractmethod
    def check_parameters(self, params):
        """Validate action parameters.

        The method does a preliminary check of the given actual action
        parameters and raises an exception if they don't match the
        action signature. However, a successful invocation of this
        method does not guarantee a further successful run of the
        instantiated action.

        :param params: Action parameters as a dictionary where keys
            are parameter names and values are parameter values.
        :return: None or raises an exception if the given parameters
            are not valid.
        """
        pass

    @abc.abstractmethod
    def post_process_result(self, result):
        """Converts the given action result.

        A certain action implementation may need to do an additional
        conversion of the action result by its descriptor. This approach
        allows to implement wrapper actions running asynchronously
        because in such cases, the initial action result depends on a 3rd
        party that's responsible for delivering it to Mistral. But when
        it comes to Mistral we still have a chance to apply needed
        transformations defined by this method.

        :param result: Action result.
            An instance of mistral_lib.types.Result.
        :return: Converted action result.
        """
        pass


class ActionProvider(abc.ABC):
    """Serves as a source of actions for the system.

    A concrete implementation of this interface can use its own
    way of delivering actions to the system. It can store actions
    in a database, get them over HTTP, AMQP or any other transport.
    Or it can simply provide a static collection of actions and keep
    them in memory throughout the cycle of the application.
    """

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        """The name of the action provider.

        Different action providers can use it differently.
        Some may completely ignore it, others may use it, for example,
        for searching actions in a certain way.
        """
        return self._name

    @abc.abstractmethod
    def find(self, action_name, namespace=None):
        """Finds action descriptor by name.

        :param action_name: Action name.
        :param namespace: Action namespace. None is used for the default
            namespace.
        :return: An instance of ActionDescriptor or None, if not found.
        """
        pass

    @abc.abstractmethod
    def find_all(self, namespace=None, limit=None, sort_fields=None,
                 sort_dirs=None, filters=None):
        """Finds all action descriptors for this provider.

        :param namespace: Optional. Action namespace.
        :param limit: Positive integer or None. Maximum number of action
            descriptors to return in a single result.
        :param sort_fields: Optional. A list of action descriptor fields
            that define sorting of the result set.
        :param sort_dirs: Optional. A list of sorting orders ("asc" or "desc")
            in addition to the "sort_fields" argument.
        :param filters: Optional. A dictionary describing AND-joined filters.
        :return: List of ActionDescriptor instances.
        """
        pass
