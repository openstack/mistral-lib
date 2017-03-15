# Copyright 2013 - Mirantis, Inc.
# Copyright 2017 - Nokia Networks.
# Copyright 2017 - Red Hat, Inc.
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


def cut_dict(d, length=100):
    """Truncates string representation of a dictionary for a given length.

    :param d: dictionary to truncate
    :param length: amount of characters to truncate to
    :return: string containing given length of characters from the dictionary
    """
    if not isinstance(d, dict):
        raise ValueError("A dictionary is expected, got: %s" % type(d))

    res = "{"

    idx = 0

    for key, value in d.items():
        k = str(key)
        v = str(value)

        # Processing key.
        new_len = len(res) + len(k)

        is_str = isinstance(key, str)

        if is_str:
            new_len += 2

        if new_len >= length:
            res += "'%s..." % k[:length - new_len] if is_str else "%s..." % k

            break
        else:
            res += "'%s'" % k if is_str else k
            res += ": "

        # Processing value.
        new_len = len(res) + len(v)

        is_str = isinstance(value, str)

        if is_str:
            new_len += 2

        if new_len >= length:
            res += "'%s..." % v[:length - new_len] if is_str else "%s..." % v

            break
        else:
            res += "'%s'" % v if is_str else v
            res += ', ' if idx < len(d) - 1 else '}'

        if len(res) >= length:
            res += '...'

            break

        idx += 1

    return res


def cut_list(l, length=100):
    """Truncates string representation of a list for a given length.

    :param l: list to truncate
    :param length: amount of characters to truncate to
    :return: string containing given length of characters from the list
    """
    if not isinstance(l, list):
        raise ValueError("A list is expected, got: %s" % type(l))

    res = '['

    for idx, item in enumerate(l):
        s = str(item)

        new_len = len(res) + len(s)

        is_str = isinstance(item, str)

        if is_str:
            new_len += 2

        if new_len >= length:
            res += "'%s..." % s[:length - new_len] if is_str else "%s..." % s

            break
        else:
            res += "'%s'" % s if is_str else s
            res += ', ' if idx < len(l) - 1 else ']'

    return res


def cut_string(s, length=100):
    """Truncates a string for a given length.

    :param s: string to truncate
    :param length: amount of characters to truncate to
    :return: string containing given length of characters
    """
    if len(s) > length:
        return "%s..." % s[:length]

    return s


def cut(data, length=100):
    """Truncates string representation of data for a given length.

    :param data: a dictionary, list or string to truncate
    :param length: amount of characters to truncate to
    :return: string containing given length of characters
    """
    if not data:
        return data

    if isinstance(data, list):
        return cut_list(data, length=length)

    if isinstance(data, dict):
        return cut_dict(data, length=length)

    return cut_string(str(data), length=length)
