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
from Parser import TClass, TLifecycle
from ParamsParser import TBeautifulCapiParams
from FileCache import FileCache
from FileGenerator import FileGenerator, IfDefScope, WatchdogScope, IndentScope, Unindent
from CapiGenerator import CapiGenerator
from NamespaceGenerator import NamespaceGenerator
from LifecycleTraits import create_lifecycle_traits
from InheritanceTraits import create_inheritance_traits
from ArgumentGenerator import ClassTypeGenerator, ArgumentGenerator
from CustomerCallbacks import generate_callbacks_on_client_side_definitions
from CustomerCallbacks import generate_callbacks_on_client_side_declarations
from LibraryCallbacks import generate_callbacks_on_library_side
from Helpers import get_c_name, get_template_name, replace_template_to_filename, get_template_tail
from Helpers import if_required_then_add_empty_line


class ClassGenerator(object):
    def __init__(self, class_object: TClass, parent_namespace: NamespaceGenerator,
                 params: TBeautifulCapiParams):
        self.class_object = class_object
        self.parent_namespace = parent_namespace
        self.base_class_generator = None
        self.base_class_as_argument_type = None
        self.derived_class_generators = []
        self.enum_generators = []
        self.constructor_generators = []
        self.method_generators = []
        self.params = params
        self.lifecycle_traits = create_lifecycle_traits(self.class_object.lifecycle, params)
        self.inheritance_traits = None
        self.file_cache = None
        self.capi_generator = None
        self.exception_code = -1
        self.callback_lifecycle_traits = None

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
    def implementation_name(self) -> str:
        return self.class_object.implementation_class_name

    @property
    def snippet_implementation_declaration(self) -> str:
        return self.lifecycle_traits.snippet_implementation_usage.format(implementation_name=self.implementation_name)

    @property
    def method_copy_or_add_ref_default_value(self) -> bool:
        return self.lifecycle_traits.method_copy_or_add_ref_default_value

    @property
    def is_callback(self) -> bool:
        return self.base_class_generator and self.base_class_generator.class_object.callbacks

    @property
    def cast_to_base(self) -> str:
        return self.full_c_name + '_cast_to_base'

    def cast_from_base(self, base_class_generator) -> str:
        return base_class_generator.full_c_name + '_cast_to_' + self.full_c_name

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

    @property
    def copy_callback_type(self) -> str:
        return self.full_c_name + '_copy_callback_type'

    @property
    def delete_callback_type(self) -> str:
        return self.full_c_name + '_delete_callback_type'

    @property
    def add_ref_callback_type(self) -> str:
        return self.full_c_name + '_add_ref_callback_type'

    @property
    def release_callback_type(self) -> str:
        return self.full_c_name + '_release_callback_type'

    def implementation_result_instructions(self, result_var: str, expression: str) -> ([str], str):
        return self.lifecycle_traits.implementation_result_instructions(self, result_var, expression)

    def __generate_enum_definitions(self, declaration_header):
        for enum_generator in self.enum_generators:
            enum_generator.generate_enum_definition(declaration_header)
        if self.enum_generators:
            declaration_header.put_line('')

    def __generate_constructor_declarations(self, declaration_header):
        for constructor_generator in self.constructor_generators:
            declaration_header.put_line('{constructor_declaration};'.format(
                constructor_declaration=constructor_generator.wrap_declaration()))
            constructor_generator.include_dependent_declaration_headers(declaration_header, self.file_cache)

    def __generate_method_declarations(self, declaration_header):
        for method_generator in self.method_generators:
            declaration_header.put_line('{method_declaration};'.format(
                method_declaration=method_generator.wrap_declaration(self.capi_generator)))
            method_generator.include_dependent_declaration_headers(declaration_header, self.file_cache)

    def __generate_class_body(self, declaration_header):
        with Unindent(declaration_header):
            declaration_header.put_line('public:')
        self.__generate_enum_definitions(declaration_header)
        self.__generate_constructor_declarations(declaration_header)
        self.__generate_method_declarations(declaration_header)
        self.inheritance_traits = create_inheritance_traits(self.class_object.requires_cast_to_base)
        declaration_header.put_line('')
        self.lifecycle_traits.generate_std_methods_declarations(declaration_header, self)
        with Unindent(declaration_header):
            declaration_header.put_line('protected:')
        self.inheritance_traits.generate_set_object_declaration(declaration_header, self)
        self.inheritance_traits.generate_pointer_declaration(declaration_header, self)

    def __generate_callback_lifecycle_traits(self):
        if self.is_callback:
            callback = self.base_class_generator.class_object.callbacks[0]
            self.callback_lifecycle_traits = create_lifecycle_traits(callback.lifecycle, self.params)
            self.callback_lifecycle_traits.create_exception_traits(callback, self.capi_generator)

    def __generate_down_cast_template_declaration(self, declaration_header):
        if self.class_object.lifecycle != TLifecycle.copy_semantic and self.derived_class_generators:
            this_class_argument_generator = ArgumentGenerator(ClassTypeGenerator(self), 'source_object')
            declaration_header.put_line('')
            declaration_header.put_line('template<typename TargetType>')
            declaration_header.put_line('inline TargetType down_cast({cast_from_ref});'.format(
                cast_from_ref=this_class_argument_generator.wrap_argument_declaration()
            ))

    def __get_all_base_classes(self) -> []:
        return self.base_class_generator.__get_all_base_classes() + [self] if self.base_class_generator else [self]

    def __generate_down_cast_template_specializations(self, declaration_header):
        if self.class_object.lifecycle != TLifecycle.copy_semantic and self.base_class_generator:
            for cur_base_class_generator in self.base_class_generator.__get_all_base_classes():
                declaration_header.put_line('')
                declaration_header.put_line(cur_base_class_generator.parent_namespace.one_line_namespace_begin)
                declaration_header.put_line('')

                base_class_argument_generator = ArgumentGenerator(
                    ClassTypeGenerator(cur_base_class_generator), 'source_object')
                declaration_header.put_line('template<>')
                declaration_header.put_line('inline {cast_to} down_cast<{cast_to}>({cast_from_ref});'.format(
                    cast_to=self.full_wrap_name,
                    cast_from_ref=base_class_argument_generator.wrap_argument_declaration()
                ))

                declaration_header.put_line('')
                declaration_header.put_line(cur_base_class_generator.parent_namespace.one_line_namespace_end)

    def __generate_class_declaration(self, declaration_header: FileGenerator):
        if self.base_class_generator:
            declaration_header.put_line('class {name}: public {base_class}'.format(
                name=self.wrap_name,
                base_class=self.base_class_generator.full_wrap_name))
            declaration_header.include_user_header(
                self.file_cache.class_header_decl(self.base_class_generator.full_name_array))
        else:
            declaration_header.put_line('class {name}'.format(name=self.wrap_name))
        with IndentScope(declaration_header, '};'):
            self.__generate_class_body(declaration_header)
        self.__generate_down_cast_template_declaration(declaration_header)
        self.__generate_callback_lifecycle_traits()
        generate_callbacks_on_client_side_declarations(declaration_header, self)

    def __generate_declaration(self):
        declaration_header = self.file_cache.get_file_for_class_decl(self.full_name_array)
        declaration_header.put_begin_cpp_comments(self.params)
        watchdog_string = '_'.join([item.upper() for item in self.full_name_array]) + '_DECLARATION_INCLUDED'
        with WatchdogScope(declaration_header, watchdog_string):
            declaration_header.put_include_files()
            declaration_header.include_user_header(self.file_cache.capi_header(self.full_name_array))
            declaration_header.include_user_header(self.file_cache.fwd_header(self.full_name_array))
            with IfDefScope(declaration_header, '__cplusplus'):
                declaration_header.put_line(self.parent_namespace.one_line_namespace_begin)
                declaration_header.put_line('')
                self.__generate_class_declaration(declaration_header)
                declaration_header.put_line('')
                declaration_header.put_line(self.parent_namespace.one_line_namespace_end)
                self.__generate_down_cast_template_specializations(declaration_header)

    def __generate_constructor_definitions(self, definition_header, first_method):
        for constructor_generator in self.constructor_generators:
            first_method = if_required_then_add_empty_line(first_method, definition_header)
            constructor_generator.generate_wrap_definition(definition_header, self.capi_generator)
            constructor_generator.include_dependent_definition_headers(definition_header, self.file_cache)
        return first_method

    def __generate_method_definitions(self, definition_header, first_method):
        for method_generator in self.method_generators:
            first_method = if_required_then_add_empty_line(first_method, definition_header)
            method_generator.generate_wrap_definition(definition_header)
            method_generator.include_dependent_definition_headers(definition_header, self.file_cache)

    def __generate_down_cast_definitions(self, definition_header):
        if self.class_object.lifecycle != TLifecycle.copy_semantic and self.base_class_generator:
            for cur_base_class_generator in self.base_class_generator.__get_all_base_classes():
                definition_header.put_line('')
                definition_header.put_line(cur_base_class_generator.parent_namespace.one_line_namespace_begin)
                definition_header.put_line('')

                base_class_argument_generator = ArgumentGenerator(
                    ClassTypeGenerator(cur_base_class_generator), 'source_object')
                definition_header.put_line('template<>')
                definition_header.put_line('inline {cast_to} down_cast<{cast_to}>({cast_from_ref})'.format(
                    cast_to=self.full_wrap_name,
                    cast_from_ref=base_class_argument_generator.wrap_argument_declaration()
                ))
                with IndentScope(definition_header):
                    this_class_as_return_type = ClassTypeGenerator(self)
                    this_class_as_return_type.copy_or_add_ref_when_c_2_wrap = True
                    casting_c_call = '{cast_from_base}({base_arg})'.format(
                        cast_from_base=self.cast_from_base(cur_base_class_generator),
                        base_arg=base_class_argument_generator.wrap_2_c())
                    instructions, return_expression = this_class_as_return_type.c_2_wrap_var('', casting_c_call)
                    definition_header.put_lines(instructions)
                    definition_header.put_return_cpp_statement(return_expression)

                definition_header.put_line('')
                definition_header.put_line(cur_base_class_generator.parent_namespace.one_line_namespace_end)

    def __generate_definition(self):
        definition_header = self.file_cache.get_file_for_class(self.full_name_array)
        definition_header.put_begin_cpp_comments(self.params)
        watchdog_string = '_'.join([item.upper() for item in self.full_name_array]) + '_DEFINITION_INCLUDED'
        with WatchdogScope(definition_header, watchdog_string):
            definition_header.put_include_files()
            definition_header.include_user_header(self.file_cache.class_header_decl(self.full_name_array))
            if self.base_class_generator:
                definition_header.include_user_header(
                    self.file_cache.class_header(self.base_class_generator.full_name_array))
            with IfDefScope(definition_header, '__cplusplus'):
                first_method = True
                first_method = self.__generate_constructor_definitions(definition_header, first_method)
                self.__generate_method_definitions(definition_header, first_method)
                definition_header.put_line('')
                self.lifecycle_traits.generate_std_methods_definitions(definition_header, self)
                definition_header.put_line('')
                self.inheritance_traits.generate_set_object_definition(definition_header, self)
                self.__generate_down_cast_definitions(definition_header)
                generate_callbacks_on_client_side_definitions(definition_header, self)

    def __generate_down_cast_c_function(self):
        if self.class_object.lifecycle != TLifecycle.copy_semantic and self.base_class_generator:
            for cur_base_class_generator in self.base_class_generator.__get_all_base_classes():
                base_class_argument_generator = ArgumentGenerator(
                    ClassTypeGenerator(cur_base_class_generator), 'source_object')
                body = FileGenerator(None)
                with IndentScope(body):
                    body.put_line('if ({base_object})'.format(base_object=base_class_argument_generator.name))
                    with IndentScope(body):
                        body.put_line('return dynamic_cast<{cast_to}*>({cast_from});'.format(
                            cast_to=self.class_object.implementation_class_name,
                            cast_from=base_class_argument_generator.c_2_implementation_to_pointer()))
                    body.put_line('else')
                    with IndentScope(body):
                        body.put_line('return 0;')
                self.capi_generator.add_c_function(
                    self.full_name_array,
                    'void*',
                    self.cast_from_base(cur_base_class_generator),
                    base_class_argument_generator.c_argument_declaration(),
                    body)

    def __generate_c_functions(self):
        for constructor_generator in self.constructor_generators:
            constructor_generator.generate_c_function(self.capi_generator)
        for method_generator in self.method_generators:
            method_generator.generate_c_function(self.capi_generator)
        self.lifecycle_traits.generate_c_functions(self)
        self.inheritance_traits.generate_c_functions(self)
        self.__generate_down_cast_c_function()
        if self.class_object.implementation_class_header_filled:
            self.capi_generator.additional_includes.include_user_header(self.class_object.implementation_class_header)

    def __generate_snippet(self):
        if self.enum_generators or self.class_object.abstract:
            snippet_file_name = os.path.join(
                self.params.internal_snippets_folder, *get_template_name(self.implementation_name).split('::'))
            snippet_file_name += replace_template_to_filename(get_template_tail(self.implementation_name)) + '.h'
            snippet_file = FileGenerator(snippet_file_name)
            snippet_file.put_begin_cpp_comments(self.params)
            for enum_generator in self.enum_generators:
                enum_generator.generate_enum_definition(snippet_file)
            if self.class_object.abstract:
                snippet_file.put_line('')
                snippet_file.put_line('virtual ~{impl_name}() {{}}'.format(
                    impl_name=get_template_name(self.implementation_name).split('::')[-1]))
                for method_generator in self.method_generators:
                    method_generator.generate_snippet(snippet_file)

    def generate_forward_declaration(self, out: FileGenerator):
        out.put_line('class {0};'.format(self.wrap_name))

    def generate(self, file_cache: FileCache, capi_generator: CapiGenerator):
        self.file_cache = file_cache
        self.capi_generator = capi_generator
        self.__generate_declaration()
        self.__generate_definition()
        self.__generate_c_functions()
        self.__generate_snippet()
        generate_callbacks_on_library_side(self, capi_generator)
