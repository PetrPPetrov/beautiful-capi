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


import os
from Parser import TNamespace
from Helpers import get_c_name
from FileGenerator import FileGenerator, WatchdogScope, IfDefScope, IndentScope
from CapiGenerator import CapiGenerator
from FileCache import FileCache


class NamespaceGenerator(object):
    def __init__(self, namespace_object: TNamespace, parent_namespace, params):
        self.namespace_object = namespace_object
        self.parent_namespace = parent_namespace
        self.enum_generators = []
        self.nested_namespaces = []
        self.classes = []
        self.functions = []
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
    def wrap_name(self) -> str:
        return self.name

    @property
    def full_wrap_name(self) -> str:
        return self.full_name

    @property
    def c_name(self) -> str:
        return get_c_name(self.name)

    @property
    def full_c_name(self) -> str:
        return get_c_name(self.full_name)

    @property
    def implementation_name(self) -> str:
        return self.full_name

    @property
    def one_line_namespace_begin(self) -> str:
        return '{parent_ns}namespace {name} {{'.format(
            parent_ns=self.parent_namespace.one_line_namespace_begin + ' ' if self.parent_namespace else '',
            name=self.name)

    @property
    def one_line_namespace_end(self) -> str:
        return '{parent_ns}}}'.format(
            parent_ns=self.parent_namespace.one_line_namespace_end if self.parent_namespace else '')

    def __generate_namespace_enumerators(self, namespace_header):
        if self.enum_generators:
            with IfDefScope(namespace_header, '__cplusplus'):
                namespace_header.put_line(self.one_line_namespace_begin)
                namespace_header.put_line('')
                for enum_generator in self.enum_generators:
                    enum_generator.generate_enum_definition(namespace_header)
                namespace_header.put_line('')
                namespace_header.put_line(self.one_line_namespace_end)
            namespace_header.put_line('')

    def __generate_namespace_functions(self, capi_generator, file_cache, namespace_header):
        if self.functions:
            with IfDefScope(namespace_header, '__cplusplus'):
                namespace_header.put_line(self.one_line_namespace_begin)
                namespace_header.put_line('')
                for function_generator in self.functions:
                    function_generator.generate_wrap_definition(namespace_header, capi_generator)
                    function_generator.generate_c_function(capi_generator)
                    function_generator.include_dependent_definition_headers(namespace_header, file_cache)
                    function_generator.include_dependent_implementation_headers(capi_generator)
                namespace_header.put_line('')
                namespace_header.put_line(self.one_line_namespace_end)

    def __generate_namespace_headers(self, file_cache: FileCache, capi_generator: CapiGenerator):
        namespace_header = file_cache.get_file_for_namespace(self.full_name_array)
        namespace_header.put_begin_cpp_comments(self.params)
        with WatchdogScope(namespace_header, self.full_name.upper() + '_INCLUDED'):
            self.__generate_namespace_enumerators(namespace_header)
            namespace_header.put_include_files()
            namespace_header.include_user_header(file_cache.capi_header(self.full_name_array))
            namespace_header.include_user_header(file_cache.fwd_header(self.full_name_array))
            for nested_namespace_generator in self.nested_namespaces:
                namespace_header.include_user_header(
                    file_cache.namespace_header(nested_namespace_generator.full_name_array))
                nested_namespace_generator.__generate_namespace_headers(file_cache, capi_generator)
            for class_generator in self.classes:
                namespace_header.include_user_header(
                    file_cache.class_header(class_generator.full_name_array))
            self.__generate_namespace_functions(capi_generator, file_cache, namespace_header)

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

    def __generate_snippet(self):
        if self.enum_generators:
            snippet_file_name = os.path.join(self.params.internal_snippets_folder, *self.full_name_array) + '.h'
            snippet_file = FileGenerator(snippet_file_name)
            snippet_file.put_begin_cpp_comments(self.params)
            for enum_generator in self.enum_generators:
                enum_generator.generate_enum_definition(snippet_file)

    def generate(self, file_cache: FileCache, capi_generator: CapiGenerator):
        self.__generate_namespace_headers(file_cache, capi_generator)
        self.__generate_forward_declarations(file_cache, capi_generator)
        for nested_namespace in self.nested_namespaces:
            nested_namespace.generate(file_cache, capi_generator)
        for class_generator in self.classes:
            class_generator.generate(file_cache, capi_generator)
        self.__generate_snippet()
        if self.namespace_object.implementation_header_filled:
            capi_generator.additional_includes.include_user_header(self.namespace_object.implementation_header)