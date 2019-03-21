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


from Parser import TFunction, TNamespace, TBeautifulCapiRoot, TProlog
from ParamsParser import TBeautifulCapiParams
from FileGenerator import FileGenerator, IndentScope
from Helpers import get_c_name


def get_implementation_name(name: str, namespace_name: str, params: TBeautifulCapiParams):
    return '{0}{1}Get{2}VersionImpl'.format(params.autogen_prefix_for_internal_implementation, namespace_name, name)


def create_get_version_component_function(name: str, namespace: TNamespace, params: TBeautifulCapiParams):
    get_version_component_function = TFunction()
    get_version_component_function.name = 'Get{0}Version'.format(name)
    get_version_component_function.noexcept = True
    get_version_component_function.return_type = 'int'
    get_version_component_function.implementation_name = get_implementation_name(name, namespace.name, params)
    get_version_component_function.prologs.append(TProlog())
    return get_version_component_function


def process_namespace(namespace: TNamespace, params: TBeautifulCapiParams):
    namespace.functions.append(create_get_version_component_function('Major', namespace, params))
    namespace.functions.append(create_get_version_component_function('Minor', namespace, params))
    namespace.functions.append(create_get_version_component_function('Patch', namespace, params))


def process(root_node: TBeautifulCapiRoot, params: TBeautifulCapiParams):
    for cur_namespace in root_node.namespaces:
        process_namespace(cur_namespace, params)


def generate_get_version_component_function(out: FileGenerator, function_name: str, value):
    out.put_line('int {0}()'.format(function_name))
    with IndentScope(out):
        out.put_line('return {0};'.format(value))
    out.put_line('')


def generate_get_version_functions(
        out: FileGenerator, namespace_name: str, params: TBeautifulCapiParams, api_root: TBeautifulCapiRoot):
    generate_get_version_component_function(
        out, get_implementation_name('Major', namespace_name, params), api_root.major_version)
    generate_get_version_component_function(
        out, get_implementation_name('Minor', namespace_name, params), api_root.minor_version)
    generate_get_version_component_function(
        out, get_implementation_name('Patch', namespace_name, params), api_root.patch_version)


def generate_check_version(out: FileGenerator, namespace_name: str, shared_library_name: str):
    out.put_line('const int major_version = {ns}_get_major_version();'.format(ns=get_c_name(namespace_name)))
    out.put_line('const int minor_version = {ns}_get_minor_version();'.format(ns=get_c_name(namespace_name)))
    out.put_line('const int patch_version = {ns}_get_patch_version();'.format(ns=get_c_name(namespace_name)))
    expected_major = '{ns}_MAJOR_VERSION'.format(ns=namespace_name.upper())
    expected_minor = '{ns}_MINOR_VERSION'.format(ns=namespace_name.upper())
    expected_patch = '{ns}_PATCH_VERSION'.format(ns=namespace_name.upper())
    major_compare = 'major_version != {expected_major}'.format(expected_major=expected_major)
    minor_compare = 'minor_version != {expected_minor}'.format(expected_minor=expected_minor)
    patch_compare = 'patch_version != {expected_patch}'.format(expected_patch=expected_patch)
    out.put_line('if ({major} || {minor} || {patch})'.format(
        major=major_compare, minor=minor_compare, patch=patch_compare))
    with IndentScope(out):
        out.put_line('std::stringstream error_message;')
        if shared_library_name:
            out.put_line('error_message << "Incorrect version of " << {0} << " library. ";'.format(
                shared_library_name
            ))
        else:
            out.put_line('error_message << "Incorrect version of library. ";')
        out.put_line(
            'error_message << "Expected version is " << {0} << "." << {1} << "." << {2} << ". ";'.format(
                expected_major, expected_minor, expected_patch))
        out.put_line(
            'error_message << "Found version is " << {0} << "." << {1} << "." << {2} << ".";'.format(
                'major_version', 'minor_version', 'patch_version'
            ))
        out.put_line('throw std::runtime_error(error_message.str());')
