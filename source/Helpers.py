#!/usr/bin/env python
#
# Beautiful Capi generates beautiful C API wrappers for your C++ classes
# Copyright (C) 2015 Petr Petrovich Petrov
#
# This file is part of Beautiful Capi.
#
# Beautiful Capi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Beautiful Capi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Beautiful Capi.  If not, see <http://www.gnu.org/licenses/>.
#


def get_arguments_list_for_declaration(arguments):
    return ', '.join(['{0} {1}'.format(argument.m_type, argument.m_name) for argument in arguments])


def get_arguments_list_for_wrap_declaration(arguments):
    result = get_arguments_list_for_declaration(arguments)
    return 'void* object_pointer' + (', {0}'.format(result) if result else '')


def get_arguments_list_for_constructor_call(arguments):
    return ', '.join(['{0}'.format(argument.m_name) for argument in arguments])


def get_arguments_list_for_c_call(arguments):
    result = get_arguments_list_for_constructor_call(arguments)
    return ', {0}'.format(result) if result else ''


def get_c_function_name(full_qualified_method_name):
    parsed_name = full_qualified_method_name.split('::')
    return '_'.join(parsed_name)


def get_cpp_type(type_name):
    if not type_name:
        return 'void'
    return type_name


def pascal_to_stl(pascal_name):
    return ''.join(['_' + symbol.lower() if symbol.isupper() else symbol for symbol in pascal_name])


class NamespaceScope(object):
    def __init__(self, cur_namespace_path, cur_namespace):
        self.cur_namespace_path = cur_namespace_path
        self.cur_namespace = cur_namespace

    def __enter__(self):
        self.cur_namespace_path.append(self.cur_namespace)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cur_namespace_path.pop()
