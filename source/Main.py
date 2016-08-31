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

import argparse
import os
from xml.dom.minidom import parse
from Helpers import NamespaceScope
import Helpers
from Constants import Constants
from DownCast import generate_down_casts_for_namespace
from PreprocessClasses import pre_process_beautiful_capi_root
from LifecycleTraits import CreateLifecycleTraits
from InheritanceTraits import CreateInheritanceTraits
from CfunctionTraits import CreateLoaderTraits
from ExceptionTraits import CreateExceptionTraits
from FileTraits import CreateFileTraits
from FileGenerator import WatchdogScope
from FileGenerator import IfDefScope
from CapiFwd import process_capi
from CapiFwd import process_fwd
from CapiFwd import generate_forward_holder
from Callback import generate_callback_classes
from Callback import generate_custom_callbacks
from Callback import generate_callbacks_implementations
import FileGenerator
import Parser
import ParamsParser
from ParseRoot import parse_root


class CapiGenerator(object):
    def __init__(self,
                 input_filename,
                 input_params_filename,
                 output_folder,
                 output_wrap_file_name,
                 internal_snippets_folder):
        self.input_xml = input_filename
        self.input_params = parse(input_params_filename)
        self.output_folder = output_folder
        self.output_wrap_file_name = output_wrap_file_name
        self.internal_snippets_folder = internal_snippets_folder
        self.api_description = None
        self.params_description = None
        self.output_header = None
        self.output_source = None
        self.cur_namespace_path = []
        self.loader_traits = None
        self.file_traits = None
        self.lifecycle_traits = None
        self.inheritance_traits = None
        self.exception_traits = None
        self.api_defines_generated = False
        self.extra_info = {}
        self.exception_class_2_code = {}
        self.c_enums = FileGenerator.FileGenerator(None)
        self.internal_snippet = None
        self.callback_typedefs = FileGenerator.FileGenerator(None)
        self.callback_2_class = {}
        self.callbacks_implementations = FileGenerator.FileGenerator(None)

    def generate(self):
        self.params_description = ParamsParser.load(self.input_params)
        self.api_description = parse_root(self.input_xml)
        self.params_description.autogen_prefix = self.params_description.autogen_prefix.format(project_name =
            self.api_description.project_name)

        generate_callback_classes(self.api_description, self)
        pre_process_beautiful_capi_root(self.api_description, self)
        with CreateLoaderTraits(self):
            with CreateFileTraits(self):
                with CreateExceptionTraits(Parser.TConstructor(), None, self):
                    self.exception_traits.generate_codes()
                    generate_forward_holder(self)
                    generate_custom_callbacks(self.api_description, self)
                    self.output_source = FileGenerator.FileGenerator(self.output_wrap_file_name)
                    self.output_source.put_begin_cpp_comments(self.params_description)
                    for namespace in self.api_description.namespaces:
                        self.__process_namespace(namespace)
                    generate_callbacks_implementations(self.api_description, self)
                    self.exception_traits.generate_check_and_throw_exception_header()

    def get_namespace_id(self):
        return '_'.join(self.cur_namespace_path)

    def __process_namespace(self, namespace):
        with NamespaceScope(self.cur_namespace_path, namespace):
            self.__process_namespace_header(namespace)

            for nested_namespace in namespace.namespaces:
                self.__process_namespace(nested_namespace)

            for cur_class in namespace.classes:
                self.__process_class(cur_class)

    def __process_namespace_header(self, namespace):
        self.output_header = self.file_traits.get_file_for_namespace(self.cur_namespace_path)
        self.output_header.put_begin_cpp_comments(self.params_description)

        with WatchdogScope(self.output_header, '{0}_INCLUDED'.format(self.get_namespace_id().upper())):

            if namespace.enumerations:
                self.internal_snippet = FileGenerator.FileGenerator(
                    os.path.join(self.internal_snippets_folder, *self.cur_namespace_path) + '.h')
                self.internal_snippet.put_begin_cpp_comments(self.params_description)
                with IfDefScope(self.output_header, '__cplusplus'):
                    for cur_namespace in self.cur_namespace_path:
                        self.output_header.put_line('namespace {0} {{ '.format(cur_namespace), '')
                    self.output_header.put_line('')
                    self.output_header.put_line('')

                    for enum in namespace.enumerations:
                        self.__generate_enumeration_namespace(enum)

                    for cur_namespace in self.cur_namespace_path:
                        self.output_header.put_line('}', '')
                self.internal_snippet = None
                self.output_header.put_line('')
                self.output_header.put_line('')

            self.output_header.put_include_files()
            self.output_header.put_line('')
            process_capi(self)
            process_fwd(self, namespace)
            self.loader_traits.add_impl_header(namespace.implementation_header)

            for cur_namespace in namespace.namespaces:
                with NamespaceScope(self.cur_namespace_path, cur_namespace):
                    self.output_header.include_user_header(self.file_traits.namespace_header(self.cur_namespace_path))

            for cur_class in namespace.classes:
                self.output_header.include_user_header(self.file_traits.class_header(cur_class))

            if len(self.cur_namespace_path) == 1:
                self.exception_traits.include_check_and_throw_exception_header()

            with IfDefScope(self.output_header, '__cplusplus'):
                for cur_namespace in self.cur_namespace_path:
                    self.output_header.put_line('namespace {0} {{ '.format(cur_namespace), '')

                self.output_header.put_line('')
                self.output_header.put_line('')

                if namespace.functions:
                    for function in namespace.functions:
                        self.__process_function(function)

                if len(self.cur_namespace_path) == 1:
                    generate_down_casts_for_namespace(self.output_header, namespace, self)

                for cur_namespace in self.cur_namespace_path:
                    self.output_header.put_line('}', '')
                self.output_header.put_line('')

    def __process_class(self, cur_class):
        if cur_class.internal_interface or cur_class.enumerations:
            self.internal_snippet = FileGenerator.FileGenerator(
                os.path.join(self.internal_snippets_folder, *cur_class.implementation_class_name.split('::')) + '.h')
            self.internal_snippet.put_begin_cpp_comments(self.params_description)
        self.output_header = self.file_traits.get_file_for_class(self.cur_namespace_path, cur_class)
        with NamespaceScope(self.cur_namespace_path, cur_class):
            with CreateLifecycleTraits(cur_class, self):
                with CreateInheritanceTraits(cur_class, self):
                    self.output_header.put_begin_cpp_comments(self.params_description)
                    with WatchdogScope(self.output_header, '{0}_INCLUDED'.format(self.get_namespace_id().upper())):
                        self.output_header.put_include_files()
                        self.output_header.include_user_header(self.file_traits.capi_header(self.cur_namespace_path))
                        self.output_header.include_user_header(self.file_traits.fwd_header(self.cur_namespace_path))
                        for include_info in cur_class.include_headers:
                            self.output_header.include_header(include_info.file, include_info.system)
                        if cur_class.base:
                            extra_info_entry = self.extra_info[cur_class]
                            self.output_header.include_user_header(
                                self.file_traits.class_header(extra_info_entry.base_class_object))
                        self.__include_additional_capi_and_fwd(cur_class)
                        self.output_header.put_line('')
                        with IfDefScope(self.output_header, '__cplusplus'):
                            for cur_namespace in self.cur_namespace_path[:-1]:
                                self.output_header.put_line('namespace {0} {{ '.format(cur_namespace), '')
                            self.output_header.put_line('')
                            self.output_header.put_line('')

                            self.__generate_class(cur_class)
                            self.output_header.put_line('')

                            self.__generate_internal_class(cur_class)

                            for cur_namespace in self.cur_namespace_path[:-1]:
                                self.output_header.put_line('}', '')
                            self.output_header.put_line('')
        self.internal_snippet = None

    def __include_additional_capi_and_fwd(self, cur_class):
        additional_namespaces = {}
        for constructor in cur_class.constructors:
            self.__include_additional_capi_and_fwd_function(constructor, additional_namespaces)
        for method in cur_class.methods:
            self.__include_additional_capi_and_fwd_method(method, additional_namespaces)
        for additional_namespace in additional_namespaces.keys():
            if additional_namespace != self.cur_namespace_path[0]:
                self.file_traits.include_capi_header([additional_namespace])
                self.file_traits.include_fwd_header([additional_namespace])

    def __include_additional_capi_and_fwd_check_type(self, type_name, additional_namespaces):
        if self.__is_class_type(type_name):
            additional_namespaces.update({type_name.split('::')[0]: True})

    def __include_additional_capi_and_fwd_function(self, function, additional_namespaces):
        for argument in function.arguments:
            self.__include_additional_capi_and_fwd_check_type(argument.type_name, additional_namespaces)

    def __include_additional_capi_and_fwd_method(self, method, additional_namespaces):
        self.__include_additional_capi_and_fwd_function(method, additional_namespaces)
        if self.__is_class_type(method.return_type):
            self.__include_additional_capi_and_fwd_check_type(method.return_type, additional_namespaces)

    def __generate_class(self, cur_class):
        self.loader_traits.add_impl_header(cur_class.implementation_class_header)
        Helpers.output_code_blocks(self.output_header, cur_class.code_before_class_definitions)
        self.output_header.put_line('class {0}{1}'.format(
            cur_class.name + self.lifecycle_traits.get_suffix(),
            ' : public ' + cur_class.base + self.lifecycle_traits.get_suffix() if cur_class.base else ''
        ))
        with FileGenerator.IndentScope(self.output_header, '};'):
            with FileGenerator.Unindent(self.output_header):
                self.output_header.put_line('protected:')
            self.inheritance_traits.generate_pointer_declaration()
            self.inheritance_traits.generate_set_object()
            with FileGenerator.Unindent(self.output_header):
                self.output_header.put_line('public:')
            for enumeration in cur_class.enumerations:
                self.__generate_enumeration_internal_class(enumeration)
                if not cur_class.internal_interface:
                    self.__generate_enumeration_internal_class_only(enumeration)
            Helpers.output_code_blocks(self.output_header, cur_class.code_after_publics)
            self.lifecycle_traits.generate_copy_constructor()
            self.lifecycle_traits.generate_std_methods()
            self.lifecycle_traits.generate_assignment_operator()
            for constructor in cur_class.constructors:
                self.inheritance_traits.generate_constructor(constructor)
            self.lifecycle_traits.generate_destructor()
            self.lifecycle_traits.generate_delete_method()
            for method in cur_class.methods:
                self.__generate_method(method, cur_class)
        Helpers.output_code_blocks(self.output_header, cur_class.code_after_class_definitions, True)

    def __generate_internal_class(self, cur_class):
        if self.internal_snippet and cur_class.internal_interface:
            impl_class_short_name = cur_class.implementation_class_name.split('::')[-1]
            for enumeration in cur_class.enumerations:
                self.__generate_enumeration_internal_class_only(enumeration)
            self.internal_snippet.put_line('virtual ~{0}() {{}}'.format(impl_class_short_name))
            for cur_method in cur_class.methods:
                method_declaration = 'virtual {return_type} {method_name}({arguments}){const} = 0;'.format(
                    return_type=self.get_original_type(cur_method.return_type),
                    method_name=cur_method.name,
                    arguments=', '.join(self.get_original_argument_pairs(cur_method.arguments)),
                    const=' const' if cur_method.const else ''
                )
                self.internal_snippet.put_line(method_declaration)

    def __generate_method(self, method, cur_class):
        with CreateExceptionTraits(method, cur_class, self):
            with NamespaceScope(self.cur_namespace_path, method):
                self.output_header.put_line('{return_type} {method_name}({arguments}){const}'.format(
                    return_type=self.get_wrapped_return_type(method.return_type),
                    method_name=method.name,
                    arguments=', '.join(self.get_wrapped_argument_pairs(method.arguments)),
                    const=' const' if method.const else ''
                ))
                with FileGenerator.IndentScope(self.output_header):
                    self.exception_traits.generate_c_call(
                        self.get_namespace_id().lower(),
                        '{c_function}({arguments})',
                        False
                    )
                c_function_declaration = '{return_type} {{convention}} {c_function}({arguments})'.format(
                    return_type=self.get_c_type(method.return_type),
                    c_function=self.get_namespace_id().lower(),
                    arguments=', '.join(self.exception_traits.get_c_argument_pairs())
                )
                self.loader_traits.add_c_function_declaration(c_function_declaration)
                with FileGenerator.IndentScope(self.output_source):
                    self.output_source.put_line(
                        '{const}{self_type}* self = static_cast<{self_type}*>(object_pointer);'.format(
                            const='const ' if method.const else '',
                            self_type=cur_class.implementation_class_name
                    ))
                    method_call = '{0}->{1}({2})'.format(
                        Helpers.get_self(cur_class),
                        method.name,
                        ', '.join(self.get_c_to_original_arguments(method.arguments))
                    )
                    method_call = self.make_c_return(method.return_type, method_call)
                    self.exception_traits.generate_implementation_call(method_call, method.return_type)
                self.output_source.put_line('')

    def __generate_enumeration_impl(
            self,
            enumeration: Parser.TEnumeration,
            file_object: FileGenerator.FileGenerator,
            c_mode
    ):
        with NamespaceScope(self.cur_namespace_path, enumeration):
            if c_mode:
                enum_c_name = Helpers.pascal_to_stl(self.get_namespace_id())
                self.c_enums.put_line('enum {0}'.format(enum_c_name))
            else:
                file_object.put_line('enum {enum.name}'.format(enum=enumeration))
            with FileGenerator.IndentScope(file_object, '};'):
                for item in enumeration.items:
                    if item.value_filled:
                        file_object.put_line('{item.name} = {item.value},'.format(item=item))
                    else:
                        file_object.put_line('{item.name},'.format(item=item))

    def __generate_enumeration_namespace(self, enumeration: Parser.TEnumeration):
        self.__generate_enumeration_impl(enumeration, self.output_header, False)
        self.__generate_enumeration_impl(enumeration, self.internal_snippet, False)
        #self.__generate_enumeration_impl(enumeration, self.c_enums, True)
        self.output_header.put_line('')
        #self.c_enums.put_line('')

    def __generate_enumeration_internal_class(self, enumeration: Parser.TEnumeration):
        self.__generate_enumeration_impl(enumeration, self.output_header, False)
        #self.__generate_enumeration_impl(enumeration, self.c_enums, True)
        #self.c_enums.put_line('')

    def __generate_enumeration_internal_class_only(self, enumeration: Parser.TEnumeration):
            self.__generate_enumeration_impl(enumeration, self.internal_snippet, False)

    def __process_function(self, function):
        with CreateExceptionTraits(function, None, self):
            self.loader_traits.add_impl_header(function.implementation_header)
            self.output_header.put_line('inline {return_type} {function_name}({arguments})'.format(
                return_type=self.get_wrapped_return_type(function.return_type),
                function_name=function.name,
                arguments=', '.join(self.get_wrapped_argument_pairs(function.arguments))))
            c_function_name = self.get_namespace_id().lower() + Helpers.pascal_to_stl(function.name)
            with FileGenerator.IndentScope(self.output_header):
                self.exception_traits.generate_c_call(
                    c_function_name,
                    '{c_function}({arguments})',
                    True
                )
            self.output_header.put_line('')
            c_function_declaration = '{return_type} {{convention}} {c_function}({arguments})'.format(
                return_type=self.get_c_type(function.return_type),
                c_function=c_function_name,
                arguments=', '.join(self.exception_traits.get_c_argument_pairs_for_function())
            )
            self.loader_traits.add_c_function_declaration(c_function_declaration)
            with FileGenerator.IndentScope(self.output_source):
                method_call = '{function_name}({arguments})'.format(
                    function_name=function.name
                    if not function.implementation_name else function.implementation_name,
                    arguments=', '.join(self.get_c_to_original_arguments(function.arguments))
                )
                method_call = self.make_c_return(function.return_type, method_call)
                self.exception_traits.generate_implementation_call(method_call, function.return_type)
            self.output_source.put_line('')

    def __process_source_begin(self):
        self.output_source.put_copyright_header(self.params_description.copyright_header)
        self.output_source.put_automatic_generation_warning(self.params_description.automatic_generated_warning)

    def __is_class_type(self, type_name):
        path_to_class = type_name.split('::')
        return self.__is_class_type_impl(path_to_class, self.api_description.namespaces)

    def __is_enum_type(self, type_name):
        path_to_enum = type_name.split('::')
        return self.__is_enum_type_impl(path_to_enum, self.api_description.namespaces)

    def __is_enum_in_class(self, type_name):
        class_or_namespace = '::'.join(type_name.split('::')[:-1])
        if self.__is_class_type(class_or_namespace):
            class_or_namespace_type = self.get_class_type(class_or_namespace)
            if type(class_or_namespace_type) is Parser.TClass:
                return True
        return False

    def get_class_type(self, type_name):
        path_to_class = type_name.split('::')
        return self.__get_class_type_impl(path_to_class, self.api_description.namespaces)

    def __get_class_type_impl(self, path_to_class, classes_or_namespaces):
        for class_or_namespace in classes_or_namespaces:
            if class_or_namespace.name == path_to_class[0]:
                if len(path_to_class) == 1:
                    return class_or_namespace
                elif len(path_to_class) == 2:
                    return self.__get_class_type_impl(path_to_class[1:], class_or_namespace.classes)
                else:
                    return self.__get_class_type_impl(path_to_class[1:], class_or_namespace.namespaces)
        return None

    def __is_class_type_impl(self, path_to_class, classes_or_namespaces):
        if self.__get_class_type_impl(path_to_class, classes_or_namespaces):
            return True
        else:
            return False

    def get_enum_type(self, type_name):
        path_to_enum = type_name.split('::')
        return self.__get_enum_type_impl(path_to_enum, self.api_description.namespaces)

    def get_enum_container_class(self, type_name):
        path_to_enum = type_name.split('::')
        if self.__is_enum_in_class(type_name):
            return self.__get_class_type_impl(path_to_enum[:-1], self.api_description.namespaces)
        else:
            return None

    def __get_enum_type_impl(self, path_to_enum, enums_or_namespaces):
        for enum_or_namespace in enums_or_namespaces:
            if enum_or_namespace.name == path_to_enum[0]:
                if len(path_to_enum) == 1:
                    return enum_or_namespace
                elif len(path_to_enum) == 3:
                    return self.__get_enum_type_impl(
                        path_to_enum[1:], enum_or_namespace.namespaces + enum_or_namespace.classes)
                elif len(path_to_enum) == 2:
                    return self.__get_enum_type_impl(path_to_enum[1:], enum_or_namespace.enumerations)
                else:
                    return self.__get_enum_type_impl(path_to_enum[1:], enum_or_namespace.namespaces)
        return None

    def __is_enum_type_impl(self, path_to_enum, enums_or_namespaces):
        if self.__get_enum_type_impl(path_to_enum, enums_or_namespaces):
            return True
        else:
            return False

    def get_flat_type(self, type_name):
        if not type_name:
            return 'void'
        if self.__is_class_type(type_name):
            return 'void*'
        if self.__is_enum_type(type_name):
            return self.get_enum_type(type_name).underlying_type
        return type_name

    def get_cpp_type(self, type_name):
        if not type_name:
            return 'void'
        return type_name

    # Wrapped types
    def get_wrapped_result_var(self, type_name, rest_expression, method):
        if type_name:
            if self.__is_class_type(type_name):
                cur_type = self.get_class_type(type_name)
                return '{result_type}{fwd_suffix} result({rest_expr}, {copy_or_add_ref});'.format(
                    result_type=type_name,
                    fwd_suffix=self.params_description.forward_typedef_suffix,
                    rest_expr=rest_expression,
                    copy_or_add_ref='true' if Helpers.get_return_copy_or_add_ref(method, cur_type) else 'false'
                )
            elif self.__is_enum_type(type_name):
                return '{0} result(static_cast<{0}>({1}));'.format(
                    self.get_wrapped_return_type(type_name), rest_expression)
            else:
                return '{0} result({1});'.format(type_name, rest_expression)
        else:
            return '{0};'.format(rest_expression)

    def get_wrapped_return_instruction(self, type_name, rest_expression, method):
        if type_name:
            if self.__is_class_type(type_name):
                cur_type = self.get_class_type(type_name)
                return 'return {result_type}{fwd_suffix}({rest_expr}, {copy_or_add_ref});'.format(
                    result_type=type_name,
                    fwd_suffix=self.params_description.forward_typedef_suffix,
                    rest_expr=rest_expression,
                    copy_or_add_ref='true' if Helpers.get_return_copy_or_add_ref(method, cur_type) else 'false'
                )
            elif self.__is_enum_type(type_name):
                return 'return static_cast<{cast_type}>({rest_expr});'.format(
                    cast_type=self.get_wrapped_return_type(type_name),
                    rest_expr=rest_expression)
            else:
                return 'return {0};'.format(rest_expression)
        else:
            return '{0};'.format(rest_expression)

    def get_wrapped_return_type(self, type_name):
        if self.__is_class_type(type_name):
            return type_name + self.params_description.forward_typedef_suffix
        elif self.__is_enum_type(type_name):
            return self.get_wrapped_type(type_name)
        return self.get_cpp_type(type_name)

    def get_wrapped_type(self, type_name):
        if self.__is_class_type(type_name):
            cur_type = self.get_class_type(type_name)
            with CreateLifecycleTraits(cur_type, self):
                return 'const {0}&'.format(type_name + self.lifecycle_traits.get_suffix())
        elif self.__is_enum_type(type_name):
            enum_name = type_name
            if self.__is_enum_in_class(type_name):
                path_to_enum = type_name.split('::')
                class_name = '::'.join(path_to_enum[:-1])
                with CreateLifecycleTraits(self.get_class_type(class_name), self):
                    suffix = self.lifecycle_traits.get_suffix() if self.lifecycle_traits else ''
                    enum_name = '{class_name}::{enum_name}'.format(
                        class_name='::'.join(path_to_enum[:-1]) + suffix,
                        enum_name=path_to_enum[-1])
            return enum_name
        else:
            return self.get_cpp_type(type_name)

    def get_wrapped_argument_pair(self, argument):
        return '{0} {1}'.format(self.get_wrapped_type(argument.type_name), argument.name)

    def get_wrapped_argument_pairs(self, arguments):
        return [self.get_wrapped_argument_pair(argument) for argument in arguments]

    # Wrap types from C types
    def get_wrapped_argument_from_c_pair(self, argument):
        if self.__is_class_type(argument.type_name):
            cur_type = self.get_class_type(argument.type_name)
            with CreateLifecycleTraits(cur_type, self):
                return '{0}({1}, true)'.format(argument.type_name + self.lifecycle_traits.get_suffix(), argument.name)
        elif self.__is_enum_type(argument.type_name):
            return 'static_cast<{0}>({1})'.format(self.get_wrapped_type(argument.type_name), argument.name)
        else:
            return argument.name

    def get_wrapped_argument_from_c_pairs(self, arguments):
        return [self.get_wrapped_argument_from_c_pair(argument) for argument in arguments]

    # C types from wrapped types
    def __is_raw_pointer_structure_required(self, arguments):
        for argument in arguments:
            if self.__is_class_type(argument.type_name):
                return True
        return False

    def put_raw_pointer_structure_if_required(self, output_file, arguments):
        if self.__is_raw_pointer_structure_required(arguments):
            Helpers.put_raw_pointer_structure(output_file)

    def get_c_from_wrapped_argument(self, argument):
        class_object = self.get_class_type(argument.type_name)
        if class_object:
            return 'reinterpret_cast<const raw_pointer_holder*>(&{0})->raw_pointer'.format(argument.name)
        elif self.__is_enum_type(argument.type_name):
            enum_type = self.get_enum_type(argument.type_name)
            return 'static_cast<{0}>({1})'.format(enum_type.underlying_type, argument.name)
        else:
            return argument.name

    def get_c_from_wrapped_arguments_impl(self, arguments):
        return [Constants.object_var] + self.get_c_from_wrapped_arguments_for_function_impl(arguments)

    def get_c_from_wrapped_arguments_for_function_impl(self, arguments):
        return [self.get_c_from_wrapped_argument(argument) for argument in arguments]

    # C types from original types
    def get_c_from_original_argument(self, argument):
        class_object = self.get_class_type(argument.type_name)
        if class_object:
            return 'static_cast<void*>({0})'.format(argument.name)
        elif self.__is_enum_type(argument.type_name):
            enum_type = self.get_enum_type(argument.type_name)
            return 'static_cast<{0}>({1})'.format(enum_type.underlying_type, argument.name)
        else:
            return argument.name

    def get_c_from_original_arguments_impl(self, arguments):
        return [Constants.object_var] + self.get_c_from_original_arguments_for_function_impl(arguments)

    def get_c_from_original_arguments_for_function_impl(self, arguments):
        return [self.get_c_from_original_argument(argument) for argument in arguments]

    # C types
    def make_c_return(self, return_type, expression):
        line = '{expression};'
        if return_type:
            if self.__is_class_type(return_type):
                class_object = self.get_class_type(return_type)
                with CreateLifecycleTraits(class_object, self):
                    return self.lifecycle_traits.make_c_return(class_object, expression)
            if self.__is_enum_type(return_type):
                line = 'return static_cast<{cast_type}>({{expression}});'.format(
                    cast_type=self.get_enum_type(return_type).underlying_type)
            else:
                line = 'return {expression};'
        return line.format(expression=expression)

    def get_c_type(self, type_name):
        return self.get_flat_type(type_name)

    def get_c_argument_pair(self, argument):
        return '{0} {1}'.format(self.get_c_type(argument.type_name), argument.name)

    def get_c_argument_pairs_impl(self, arguments):
        return ['void* object_pointer'] + self.get_c_argument_pairs_for_function_impl(arguments)

    def get_c_argument_pairs_for_function_impl(self, arguments):
        return [self.get_c_argument_pair(argument) for argument in arguments]

    # C to original types
    def get_c_to_original_argument(self, argument):
        class_object = self.get_class_type(argument.type_name)
        if class_object:
            with CreateLifecycleTraits(class_object, self):
                return self.lifecycle_traits.generate_get_c_to_original_argument(class_object, argument)
        elif self.__is_enum_type(argument.type_name):
            return 'static_cast<{0}>({1})'.format(self.get_original_type(argument.type_name), argument.name)
        else:
            return argument.name

    def get_c_to_original_arguments(self, arguments):
        return [self.get_c_to_original_argument(argument) for argument in arguments]

    # Original types
    def make_original_return(self, return_type, expression):
        line = '{expression};'
        if return_type:
            line = 'return {expression};'
        return line.format(expression=expression)

    def get_original_result_var(self, return_type, expression):
        line = '{expression};'
        if return_type:
            if self.__is_class_type(return_type):
                line = '{0} result(static_cast<{0}>({{expression}}));'.format(self.get_original_type(return_type))
            elif self.__is_enum_type(return_type):
                line = '{0} result(static_cast<{0}>({{expression}}));'.format(self.get_original_type(return_type))
            else:
                line = '{0} result({{expression}});'.format(self.get_original_type(return_type))
        return line.format(expression=expression)

    def get_original_type(self, type_name):
        class_object = self.get_class_type(type_name)
        if class_object:
            if class_object.lifecycle == Parser.TLifecycle.copy_semantic:
                return '{0}'.format(class_object.implementation_class_name)
            else:
                return '{0}*'.format(class_object.implementation_class_name)
        elif self.__is_enum_type(type_name):
            class_or_namespace = '::'.join(type_name.split('::')[:-1])
            if self.__is_class_type(class_or_namespace):
                class_or_namespace_type = self.get_class_type(class_or_namespace)
                if type(class_or_namespace_type) is Parser.TClass:
                    return '::'.join([class_or_namespace_type.implementation_class_name, type_name.split('::')[-1]])
            return self.get_cpp_type(type_name)
        else:
            return self.get_cpp_type(type_name)

    def get_original_argument(self, argument):
        return self.get_original_type(argument.type_name)

    def get_original_argument_pair(self, argument):
        return '{0} {1}'.format(self.get_original_type(argument.type_name), argument.name)

    def get_original_arguments(self, arguments):
        return [self.get_original_argument(argument) for argument in arguments]

    def get_original_argument_pairs(self, arguments):
        return [self.get_original_argument_pair(argument) for argument in arguments]


def main():
    print(
        'Beautiful Capi  Copyright (C) 2015  Petr Petrovich Petrov\n'
        'This program comes with ABSOLUTELY NO WARRANTY;\n'
        'This is free software, and you are welcome to redistribute it\n'
        'under certain conditions.\n')

    parser = argparse.ArgumentParser(
        prog='Beautiful Capi',
        description='This program generates C and C++ wrappers for your C++ classes.')

    parser.add_argument(
        '-i', '--input', nargs=None, default='input.xml', metavar='INPUT',
        help='specifies input API description file')
    parser.add_argument(
        '-p', '--params', nargs=None, default='params.xml', metavar='PARAMS',
        help='specifies wrapper generation parameters input file')
    parser.add_argument(
        '-o', '--output-folder', nargs=None, default='./output', metavar='OUTPUT_FOLDER',
        help='specifies output folder for generated files')
    parser.add_argument(
        '-w', '--output-wrap-file-name', nargs=None, default='./capi_wrappers.cpp', metavar='OUTPUT_WRAP',
        help='specifies output file name for wrapper C-functions')
    parser.add_argument(
        '-s', '--internal-snippets-folder', nargs=None, default='./internal_snippets', metavar='OUTPUT_SNIPPETS',
        help='specifies output folder for generated library snippets')

    args = parser.parse_args()

    schema_generator = CapiGenerator(
        args.input,
        args.params,
        args.output_folder,
        args.output_wrap_file_name,
        args.internal_snippets_folder
    )
    schema_generator.generate()

if __name__ == '__main__':
    main()
