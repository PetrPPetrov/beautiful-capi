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
import posixpath
import argparse
from xml.dom.minidom import parse
from Helpers import NamespaceScope
import Helpers
from Constants import Constants
from LifecycleTraits import CreateLifecycleTraits
from InheritanceTraits import CreateInheritanceTraits
from CfunctionTraits import CreateLoaderTraits
from FileTraits import CreateFileTraits
from FileGenerator import WatchdogScope
from FileGenerator import IfDefScope
import FileGenerator
import Parser
import ParamsParser


class CapiGenerator(object):
    def __init__(self, input_filename, input_params_filename, output_folder, output_wrap_file_name):
        self.input_xml = parse(input_filename)
        self.input_params = parse(input_params_filename)
        self.output_folder = output_folder
        self.output_wrap_file_name = output_wrap_file_name
        self.api_description = None
        self.params_description = None
        self.output_header = None
        self.output_source = None
        self.cur_namespace_path = []
        self.loader_traits = None
        self.file_traits = None
        self.lifecycle_traits = None
        self.inheritance_traits = None

    def generate(self):
        self.params_description = ParamsParser.load(self.input_params)
        self.api_description = Parser.load(self.input_xml)
        with CreateLoaderTraits(self):
            with CreateFileTraits(self):
                self.output_source = FileGenerator.FileGenerator(self.output_wrap_file_name)
                self.__process_source_begin()
                for namespace in self.api_description.m_namespaces:
                    self.__process_namespace(namespace)

    def get_namespace_id(self):
        return '_'.join(self.cur_namespace_path)

    def __process_namespace(self, namespace):
        with NamespaceScope(self.cur_namespace_path, namespace):
            self.__process_namespace_header(namespace)

            for nested_namespace in namespace.m_namespaces:
                self.__process_namespace(nested_namespace)

            for cur_class in namespace.m_classes:
                self.__process_class(cur_class)

    def __process_namespace_header(self, namespace):
        self.output_header = self.file_traits.get_file_for_namespace(self.cur_namespace_path)
        self.output_header.put_copyright_header(self.params_description.m_copyright_header)
        self.output_header.put_automatic_generation_warning(self.params_description.m_automatic_generated_warning)

        with WatchdogScope(self.output_header, '{0}_INCLUDED'.format(self.get_namespace_id().upper())):
            self.__process_capi()
            self.__process_fwd(namespace)
            self.loader_traits.add_impl_header(namespace.m_implementation_header)

            for cur_namespace in namespace.m_namespaces:
                with NamespaceScope(self.cur_namespace_path, cur_namespace):
                    self.file_traits.include_namespace_header(self.cur_namespace_path)

            for cur_class in namespace.m_classes:
                self.file_traits.include_class_header(self.cur_namespace_path, cur_class)

            if namespace.m_functions:
                self.output_header.put_line('')
                with IfDefScope(self.output_header, '__cplusplus'):
                    for cur_namespace in self.cur_namespace_path:
                        self.output_header.put_line('namespace {0} {{ '.format(cur_namespace), '')
                    self.output_header.put_line('')
                    self.output_header.put_line('')
                    for function in namespace.m_functions:
                        self.__process_function(function)
                    self.output_header.put_line('')
                    for cur_namespace in self.cur_namespace_path:
                        self.output_header.put_line('}', '')
                    self.output_header.put_line('')

    def __process_capi(self):
        if len(self.cur_namespace_path) == 1:
            self.output_header = self.file_traits.get_file_for_capi(self.cur_namespace_path)
            self.output_header.put_copyright_header(self.params_description.m_copyright_header)
            self.output_header.put_automatic_generation_warning(self.params_description.m_automatic_generated_warning)
            with WatchdogScope(self.output_header, '{0}_CAPI_INCLUDED'.format(self.get_namespace_id().upper())):
                self.loader_traits.generate_c_functions_declarations()
        self.output_header = self.file_traits.get_file_for_namespace(self.cur_namespace_path)
        self.file_traits.include_capi_header(self.cur_namespace_path)

    def __process_fwd(self, namespace):
        if len(self.cur_namespace_path) == 1:
            self.output_header = self.file_traits.get_file_for_fwd(self.cur_namespace_path)
            self.output_header.put_copyright_header(self.params_description.m_copyright_header)
            self.output_header.put_automatic_generation_warning(self.params_description.m_automatic_generated_warning)
            with WatchdogScope(self.output_header, '{0}_FWD_INCLUDED'.format(self.get_namespace_id().upper())):
                self.output_header.put_line('')
                with IfDefScope(self.output_header, '__cplusplus'):
                    self.output_header.put_line('#include <memory>')
                    self.output_header.put_line('')
                    self.__generate_forwards(namespace, True)
        self.output_header = self.file_traits.get_file_for_namespace(self.cur_namespace_path)
        self.file_traits.include_fwd_header(self.cur_namespace_path)

    def __generate_forwards(self, namespace, top_level_namespace):
        self.output_header.put_line('namespace {0}'.format(namespace.m_name))
        with FileGenerator.IndentScope(self.output_header):
            if top_level_namespace:
                self.__generate_forward_holder()
            for cur_class in namespace.m_classes:
                with CreateLifecycleTraits(cur_class, self):
                    self.output_header.put_line('class {0};'.format(
                        cur_class.m_name + self.lifecycle_traits.get_suffix()))
                    self.output_header.put_line(
                        'typedef beautiful_capi::forward_pointer_holder<{0}> {1};'.format(
                            cur_class.m_name + self.lifecycle_traits.get_suffix(),
                            cur_class.m_name + self.params_description.m_forward_typedef_suffix))
            for nested_namespace in namespace.m_namespaces:
                with NamespaceScope(self.cur_namespace_path, nested_namespace):
                    self.__generate_forwards(nested_namespace, False)

    def __generate_forward_holder(self):
        self.output_header.put_line('namespace beautiful_capi')
        with FileGenerator.IndentScope(self.output_header):
            self.output_header.put_line('template<typename WrappedObjType>')
            self.output_header.put_line('class forward_pointer_holder')
            with FileGenerator.IndentScope(self.output_header, '};'):
                self.output_header.put_line('void* m_pointer;')
                self.output_header.put_line('bool m_object_was_created;')
                self.output_header.put_line('const bool m_add_ref;')
                with FileGenerator.Unindent(self.output_header):
                    self.output_header.put_line('public:')
                self.output_header.put_line('forward_pointer_holder(void* pointer, bool add_ref)')
                self.output_header.put_line(' : m_object_was_created(false), m_pointer(pointer), m_add_ref(add_ref)')
                with FileGenerator.IndentScope(self.output_header):
                    pass
                self.output_header.put_line('~forward_pointer_holder()')
                with FileGenerator.IndentScope(self.output_header):
                    self.output_header.put_line('if (m_object_was_created)')
                    with FileGenerator.IndentScope(self.output_header):
                        self.output_header.put_line('reinterpret_cast<WrappedObjType*>(this)->~WrappedObjType();')
                self.output_header.put_line('operator WrappedObjType()')
                with FileGenerator.IndentScope(self.output_header):
                    self.output_header.put_line('return WrappedObjType(m_pointer, m_add_ref);')
                self.output_header.put_line('WrappedObjType* operator->()')
                with FileGenerator.IndentScope(self.output_header):
                    self.output_header.put_line('m_object_was_created = true;')
                    self.output_header.put_line('return new(this) WrappedObjType(m_pointer, m_add_ref);')
                self.output_header.put_line('void* get_raw_pointer() const')
                with FileGenerator.IndentScope(self.output_header):
                    self.output_header.put_line('return m_pointer;')
        self.output_header.put_line('')

    def __process_class(self, cur_class):
        self.output_header = self.file_traits.get_file_for_class(self.cur_namespace_path, cur_class)
        with NamespaceScope(self.cur_namespace_path, cur_class):
            with CreateLifecycleTraits(cur_class, self):
                with CreateInheritanceTraits(cur_class, self):
                    self.output_header.put_copyright_header(self.params_description.m_copyright_header)
                    self.output_header.put_automatic_generation_warning(
                        self.params_description.m_automatic_generated_warning
                    )
                    with WatchdogScope(self.output_header, '{0}_INCLUDED'.format(self.get_namespace_id().upper())):
                        self.file_traits.include_capi_header(self.cur_namespace_path)
                        self.file_traits.include_fwd_header(self.cur_namespace_path)
                        self.__include_additional_capi_and_fwd(cur_class)
                        self.output_header.put_line('')
                        with IfDefScope(self.output_header, '__cplusplus'):
                            for cur_namespace in self.cur_namespace_path[:-1]:
                                self.output_header.put_line('namespace {0} {{ '.format(cur_namespace), '')
                            self.output_header.put_line('')
                            self.output_header.put_line('')

                            self.__generate_class(cur_class)
                            self.output_header.put_line('')

                            for cur_namespace in self.cur_namespace_path[:-1]:
                                self.output_header.put_line('}', '')
                            self.output_header.put_line('')

    def __include_additional_capi_and_fwd(self, cur_class):
        additional_namespaces = {}
        for constructor in cur_class.m_constructors:
            self.__include_additional_capi_and_fwd_function(constructor, additional_namespaces)
        for method in cur_class.m_methods:
            self.__include_additional_capi_and_fwd_method(method, additional_namespaces)
        for additional_namespace in additional_namespaces.keys():
            if additional_namespace != self.cur_namespace_path[0]:
                self.file_traits.include_capi_header([additional_namespace])
                self.file_traits.include_fwd_header([additional_namespace])

    def __include_additional_capi_and_fwd_check_type(self, type_name, additional_namespaces):
        if self.__is_class_type(type_name):
            additional_namespaces.update({type_name.split('::')[0]: True})

    def __include_additional_capi_and_fwd_function(self, function, additional_namespaces):
        for argument in function.m_arguments:
            self.__include_additional_capi_and_fwd_check_type(argument.m_type, additional_namespaces)

    def __include_additional_capi_and_fwd_method(self, method, additional_namespaces):
        self.__include_additional_capi_and_fwd_function(method, additional_namespaces)
        if self.__is_class_type(method.m_return):
            self.__include_additional_capi_and_fwd_check_type(method.m_return, additional_namespaces)

    def __generate_class(self, cur_class):
        self.loader_traits.add_impl_header(cur_class.m_implementation_class_header)
        self.output_header.put_line('class {0}'.format(
            cur_class.m_name + self.lifecycle_traits.get_suffix()))
        with FileGenerator.IndentScope(self.output_header, '};'):
            with FileGenerator.Unindent(self.output_header):
                self.output_header.put_line('protected:')
            self.inheritance_traits.generate_pointer_declaration()
            self.inheritance_traits.generate_set_object()
            with FileGenerator.Unindent(self.output_header):
                self.output_header.put_line('public:')
            self.lifecycle_traits.generate_copy_constructor()
            self.lifecycle_traits.generate_std_methods()
            for constructor in cur_class.m_constructors:
                self.inheritance_traits.generate_constructor(constructor)
            self.lifecycle_traits.generate_destructor()
            self.lifecycle_traits.generate_delete_method()
            for method in cur_class.m_methods:
                self.__generate_method(method, cur_class)

    def __generate_method(self, method, cur_class):
        with NamespaceScope(self.cur_namespace_path, method):
            self.output_header.put_line('{return_type} {method_name}({arguments})'.format(
                return_type=self.get_wrapped_return_type(method.m_return),
                method_name=method.m_name,
                arguments=', '.join(self.get_wrapped_argument_pairs(method.m_arguments))))
            with FileGenerator.IndentScope(self.output_header):
                self.__put_raw_pointer_structure_if_required(self.output_header, method.m_arguments)
                self.output_header.put_line(self.get_wrapped_return_instruction(
                    method.m_return,
                    '{c_function}({arguments})'.format(
                        c_function=self.get_namespace_id().lower(),
                        arguments=', '.join(self.get_c_from_wrapped_arguments(method.m_arguments))
                    ),
                    method
                ))
            c_function_declaration = '{return_type} {c_function}({arguments})'.format(
                return_type=self.get_c_type(method.m_return),
                c_function=self.get_namespace_id().lower(),
                arguments=', '.join(self.get_c_argument_pairs(method.m_arguments))
            )
            self.loader_traits.add_c_function_declaration(c_function_declaration)
            with FileGenerator.IndentScope(self.output_source):
                self.output_source.put_line('{0}* self = static_cast<{0}*>(object_pointer);'.format(
                    cur_class.m_implementation_class_name
                ))
                self.output_source.put_line('{0}{1}->{2}({3});'.format(
                    self.get_c_return_instruction(method.m_return),
                    Helpers.get_self(cur_class),
                    method.m_name,
                    ', '.join(self.get_c_to_original_arguments(method.m_arguments))
                ))
            self.output_source.put_line('')

    def __process_function(self, function):
        self.loader_traits.add_impl_header(function.m_implementation_header)
        self.output_header.put_line('inline {return_type} {function_name}({arguments})'.format(
            return_type=self.get_wrapped_return_type(function.m_return),
            function_name=function.m_name,
            arguments=', '.join(self.get_wrapped_argument_pairs(function.m_arguments))))
        c_function_name = self.get_namespace_id().lower() + Helpers.pascal_to_stl(function.m_name)
        with FileGenerator.IndentScope(self.output_header):
            self.__put_raw_pointer_structure_if_required(self.output_header, function.m_arguments)
            self.output_header.put_line(self.get_wrapped_return_instruction(
                function.m_return,
                '{c_function}({arguments})'.format(
                    c_function=c_function_name,
                    arguments=', '.join(self.get_c_from_wrapped_arguments_for_function(function.m_arguments))
                ),
                function
            ))
        self.output_header.put_line('')
        c_function_declaration = '{return_type} {c_function}({arguments})'.format(
            return_type=self.get_c_type(function.m_return),
            c_function=c_function_name,
            arguments=', '.join(self.get_c_argument_pairs_for_function(function.m_arguments))
        )
        self.loader_traits.add_c_function_declaration(c_function_declaration)
        with FileGenerator.IndentScope(self.output_source):
            self.output_source.put_line('{return_instruction}{function_name}({arguments});'.format(
                return_instruction=self.get_c_return_instruction(function.m_return),
                function_name=function.m_name
                if not function.m_implementation_name else function.m_implementation_name,
                arguments=', '.join(self.get_c_to_original_arguments(function.m_arguments))
             ))
        self.output_source.put_line('')

    def __process_source_begin(self):
        self.output_source.put_copyright_header(self.params_description.m_copyright_header)
        self.output_source.put_automatic_generation_warning(self.params_description.m_automatic_generated_warning)

    def __is_class_type(self, type_name):
        path_to_class = type_name.split('::')
        return self.__is_class_type_impl(path_to_class, self.api_description.m_namespaces)

    def __get_class_type(self, type_name):
        path_to_class = type_name.split('::')
        return self.__get_class_type_impl(path_to_class, self.api_description.m_namespaces)

    def __get_class_type_impl(self, path_to_class, classes_or_namespaces):
        for class_or_namespace in classes_or_namespaces:
            if class_or_namespace.m_name == path_to_class[0]:
                if len(path_to_class) == 1:
                    return class_or_namespace
                elif len(path_to_class) == 2:
                    return self.__get_class_type_impl(path_to_class[1:], class_or_namespace.m_classes)
                else:
                    return self.__get_class_type_impl(path_to_class[1:], class_or_namespace.m_namespaces)
        return None

    def __is_class_type_impl(self, path_to_class, classes_or_namespaces):
        if self.__get_class_type_impl(path_to_class, classes_or_namespaces):
            return True
        else:
            return False

    def get_flat_type(self, type_name):
        if not type_name:
            return 'void'
        if self.__is_class_type(type_name):
            return 'void*'
        return type_name

    def get_cpp_type(self, type_name):
        if not type_name:
            return 'void'
        return type_name

    # Wrapped types
    def get_wrapped_return_instruction(self, type_name, rest_expression, method):
        if type_name:
            if self.__is_class_type(type_name):
                return 'return {result_type}{fwd_suffix}({rest_expr}, {add_ref});'.format(
                    result_type=type_name,
                    fwd_suffix=self.params_description.m_forward_typedef_suffix,
                    rest_expr=rest_expression,
                    add_ref='true' if method.m_return_value_add_ref else 'false'
                )
            else:
                return 'return {0};'.format(rest_expression)
        else:
            return '{0};'.format(rest_expression)

    def get_wrapped_return_type(self, type_name):
        if self.__is_class_type(type_name):
            return type_name + self.params_description.m_forward_typedef_suffix
        return self.get_cpp_type(type_name)

    def get_wrapped_type(self, type_name):
        if self.__is_class_type(type_name):
            return 'const {0}&'.format(type_name + self.lifecycle_traits.get_suffix())
        else:
            return self.get_cpp_type(type_name)

    def get_wrapped_argument_pair(self, argument):
        return '{0} {1}'.format(self.get_wrapped_type(argument.m_type), argument.m_name)

    def get_wrapped_argument_pairs(self, arguments):
        return [self.get_wrapped_argument_pair(argument) for argument in arguments]

    # C types from wrapped types
    def __is_raw_pointer_structure_required(self, arguments):
        for argument in arguments:
            if self.__is_class_type(argument.m_type):
                return True
        return False

    def __put_raw_pointer_structure_if_required(self, output_file, arguments):
        if self.__is_raw_pointer_structure_required(arguments):
            output_file.put_line('struct raw_pointer_holder { void* raw_pointer; };')

    def get_c_from_wrapped_argument(self, argument):
        class_object = self.__get_class_type(argument.m_type)
        if class_object:
            return 'reinterpret_cast<const raw_pointer_holder*>(&{0})->raw_pointer'.format(argument.m_name)
        else:
            return argument.m_name

    def get_c_from_wrapped_arguments(self, arguments):
        return [Constants.object_var] + self.get_c_from_wrapped_arguments_for_function(arguments)

    def get_c_from_wrapped_arguments_for_function(self, arguments):
        return [self.get_c_from_wrapped_argument(argument) for argument in arguments]

    # C types
    def get_c_return_instruction(self, type_name):
        if type_name:
            return 'return '
        else:
            return ''

    def get_c_type(self, type_name):
        return self.get_flat_type(type_name)

    def get_c_argument_pair(self, argument):
        return '{0} {1}'.format(self.get_c_type(argument.m_type), argument.m_name)

    def get_c_argument_pairs(self, arguments):
        return ['void* object_pointer'] + self.get_c_argument_pairs_for_function(arguments)

    def get_c_argument_pairs_for_function(self, arguments):
        return [self.get_c_argument_pair(argument) for argument in arguments]

    # C to original types
    def get_c_to_original_argument(self, argument):
        class_object = self.__get_class_type(argument.m_type)
        if class_object:
            return 'static_cast<{0}*>({1})'.format(class_object.m_implementation_class_name, argument.m_name)
        else:
            return argument.m_name

    def get_c_to_original_arguments(self, arguments):
        return [self.get_c_to_original_argument(argument) for argument in arguments]


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

    args = parser.parse_args()

    schema_generator = CapiGenerator(args.input, args.params, args.output_folder, args.output_wrap_file_name)
    schema_generator.generate()

main()
