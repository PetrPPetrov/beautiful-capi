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


from Parser import TNamespace
from Helpers import get_c_name
from FileGenerator import FileGenerator, WatchdogScope, IfDefScope, IndentScope
from CapiGenerator import CapiGenerator
from FileCache import FileCache


class NamespaceGenerator(object):
    def __init__(self, namespace_object: TNamespace, parent_namespace, params):
        self.namespace_object = namespace_object
        self.parent_namespace = parent_namespace
        self.nested_namespaces = []
        self.classes = []
        self.params = params

    @property
    def name(self) -> str:
        return self.namespace_object.name

    @property
    def full_name_array(self) -> [str]:
        return self.parent_namespace + [self.name] if self.parent_namespace else [self.name]

    @property
    def full_name(self) -> str:
        return '::'.join([self.parent_namespace.full_name, self.name]) if self.parent_namespace else self.name

    @property
    def c_name(self) -> str:
        return get_c_name(self.name)

    @property
    def full_c_name(self) -> str:
        return get_c_name(self.full_name)

    @property
    def one_line_namespace_begin(self) -> str:
        return '{parent_ns}namespace {name} {{'.format(
            parent_ns=self.parent_namespace.one_line_namespace_begin + ' ' if self.parent_namespace else '',
            name=self.name)

    @property
    def one_line_namespace_end(self) -> str:
        return '{parent_ns}}}'.format(
            parent_ns=self.parent_namespace.one_line_namespace_end if self.parent_namespace else '')

    def __generate_forward_declarations_impl(self, out: FileGenerator):
        out.put_line('namespace {0}'.format(self.name))
        with IndentScope(out):
            for nested_namespace_generator in self.nested_namespaces:
                nested_namespace_generator.__generate_forward_declarations_impl()
            for class_generator in self.classes:
                class_generator.generate_forward_declaration(out)

    def __generate_forward_declarations(self, file_cache: FileCache, capi_generator: CapiGenerator):
        forward_declarations = file_cache.get_file_for_fwd(self.full_name_array)
        forward_declarations.put_begin_cpp_comments(self.params)
        with WatchdogScope(forward_declarations, self.full_c_name.upper() + '_FWD_INCLUDED'):
            with IfDefScope(forward_declarations, '__cplusplus'):
                capi_generator.main_exception_traits.generate_check_and_throw_exception_forward_declaration(
                    forward_declarations)
                self.__generate_forward_declarations_impl(forward_declarations)

    def generate(self, file_cache: FileCache, capi_generator: CapiGenerator):
        self.__generate_forward_declarations(file_cache, capi_generator)
        for nested_namespace in self.nested_namespaces:
            nested_namespace.generate(file_cache, capi_generator)
        for class_generator in self.classes:
            class_generator.generate(file_cache, capi_generator)
