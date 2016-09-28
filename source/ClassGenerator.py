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


from Parser import TClass
from ParamsParser import TBeautifulCapiParams
from FileCache import FileCache
from FileGenerator import FileGenerator, IfDefScope, IndentScope, Unindent
from CapiGenerator import CapiGenerator
from NamespaceGenerator import NamespaceGenerator
from LifecycleTraits import create_lifecycle_traits
from InheritanceTraits import create_inheritance_traits
from Helpers import get_c_name


class ClassGenerator(object):
    def __init__(self, class_object: TClass, parent_namespace: NamespaceGenerator,
                 params: TBeautifulCapiParams):
        self.class_object = class_object
        self.parent_namespace = parent_namespace
        self.base_class_generator = None
        self.derived_class_generators = []
        self.constructor_generators = []
        self.method_generators = []
        self.params = params
        self.lifecycle_traits = create_lifecycle_traits(self.class_object.lifecycle, params)
        self.inheritance_traits = None
        self.file_cache = None
        self.capi_generator = None
        self.exception_code = -1

    @property
    def name(self) -> str:
        return self.class_object.name

    @property
    def full_name(self) -> str:
        return '::'.join([self.parent_namespace.full_name, self.name]) if self.parent_namespace else self.name

    @property
    def full_name_array(self) -> [str]:
        return self.parent_namespace.full_name_array + [self.name] if self.parent_namespace else [self.name]

    @property
    def wrap_name(self) -> str:
        return self.name + self.lifecycle_traits.suffix

    @property
    def full_wrap_name(self) -> str:
        return '::'.join([self.parent_namespace.full_name, self.wrap_name]) if self.parent_namespace else self.wrap_name

    @property
    def c_name(self) -> str:
        return get_c_name(self.name)

    @property
    def full_c_name(self) -> str:
        return get_c_name(self.full_name)

    @property
    def cast_to_base(self) -> str:
        return self.full_c_name + '_cast_to_base'

    @property
    def copy_method(self) -> str:
        return self.full_c_name + '_copy'

    @property
    def delete_method(self) -> str:
        return self.full_c_name + '_delete'

    @property
    def add_ref_method(self) -> str:
        return self.full_c_name + '_add_ref'

    @property
    def release_method(self) -> str:
        return self.full_c_name + '_release'

    def implementation_result_instructions(self, result_var: str, expression: str) -> ([str], str):
        return self.lifecycle_traits.implementation_result_instructions(self, result_var, expression)

    def __generate_declaration_body(self, declaration_header: FileGenerator):
        declaration_header.put_line('class {name}'.format(name=self.wrap_name))
        with IndentScope(declaration_header, '};'):
            with Unindent(declaration_header):
                declaration_header.put_line('public:')
            for constructor_generator in self.constructor_generators:
                declaration_header.put_line('{constructor_declaration};'.format(
                    constructor_declaration=constructor_generator.wrap_declaration()))
                constructor_generator.include_dependent_declaration_headers(declaration_header, self.file_cache)
            for method_generator in self.method_generators:
                declaration_header.put_line('{method_declaration};'.format(
                    method_declaration=method_generator.wrap_declaration()))
                method_generator.include_dependent_declaration_headers(declaration_header, self.file_cache)
            self.inheritance_traits = create_inheritance_traits(self.class_object.requires_cast_to_base)
            declaration_header.put_line('')
            self.lifecycle_traits.generate_std_methods_declarations(declaration_header, self)
            with Unindent(declaration_header):
                declaration_header.put_line('protected:')
            self.inheritance_traits.generate_set_object_declaration(declaration_header, self)
            self.inheritance_traits.generate_pointer_declaration(declaration_header, self)

    def __generate_declaration(self):
        declaration_header = self.file_cache.get_file_for_class_decl(self.full_name_array)
        declaration_header.put_begin_cpp_comments(self.params)
        watchdog_string = '_'.join([item.upper() for item in self.full_name_array]) + '_DECLARATION_INCLUDED'
        with IfDefScope(declaration_header, watchdog_string):
            declaration_header.put_include_files()
            declaration_header.include_user_header(self.file_cache.capi_header(self.full_name_array))
            declaration_header.include_user_header(self.file_cache.fwd_header(self.full_name_array))
            with IfDefScope(declaration_header, '__cplusplus'):
                declaration_header.put_line(self.parent_namespace.one_line_namespace_begin)
                declaration_header.put_line('')
                self.__generate_declaration_body(declaration_header)
                declaration_header.put_line('')
                declaration_header.put_line(self.parent_namespace.one_line_namespace_end)

    def __generate_definition(self):
        definition_header = self.file_cache.get_file_for_class(self.full_name_array)
        definition_header.put_begin_cpp_comments(self.params)
        watchdog_string = '_'.join([item.upper() for item in self.full_name_array]) + '_DEFINITION_INCLUDED'
        with IfDefScope(definition_header, watchdog_string):
            definition_header.put_include_files()
            definition_header.include_user_header(self.file_cache.class_header_decl(self.full_name_array))
            with IfDefScope(definition_header, '__cplusplus'):
                first_method = True
                for constructor_generator in self.constructor_generators:
                    if first_method:
                        first_method = False
                    else:
                        definition_header.put_line('')
                    constructor_generator.generate_wrap_definition(definition_header, self.capi_generator)
                    constructor_generator.include_dependent_definition_headers(definition_header, self.file_cache)
                for method_generator in self.method_generators:
                    if first_method:
                        first_method = False
                    else:
                        definition_header.put_line('')
                    method_generator.generate_wrap_definition(definition_header, self.capi_generator)
                    method_generator.include_dependent_definition_headers(definition_header, self.file_cache)
                definition_header.put_line('')
                self.lifecycle_traits.generate_std_methods_definitions(definition_header, self)
                definition_header.put_line('')
                self.inheritance_traits.generate_set_object_definition(definition_header, self)

    def __generate_c_functions(self):
        for constructor_generator in self.constructor_generators:
            constructor_generator.generate_c_function(self.capi_generator)
        for method_generator in self.method_generators:
            method_generator.generate_c_function(self.capi_generator)
        self.lifecycle_traits.generate_c_functions(self)
        self.inheritance_traits.generate_c_functions(self)

    def generate_forward_declaration(self, out: FileGenerator):
        out.put_line('class {0};'.format(self.wrap_name))

    def generate(self, file_cache: FileCache, capi_generator: CapiGenerator):
        self.file_cache = file_cache
        self.capi_generator = capi_generator
        if self.class_object.implementation_class_header_filled:
            self.capi_generator.additional_includes.include_user_header(self.class_object.implementation_class_header)
        self.__generate_declaration()
        self.__generate_definition()
        self.__generate_c_functions()
