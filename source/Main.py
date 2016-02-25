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
import Helpers
from Constants import Constants
from LifecycleTraits import create_lifecycle_traits
from InheritanceTraits import create_inheritance_traits
from CfunctionTraits import create_loader_traits
import FileGenerator
import Parser
import ParamsParser


class CapiGenerator(object):
    def __init__(self, input_filename, input_params_filename, output_folder, output_wrap_file_name):
        self.input_xml = parse(input_filename)
        self.input_params = parse(input_params_filename)
        self.output_folder = output_folder
        self.api_description = None
        self.params_description = None
        self.output_header = None
        self.output_source = None
        self.output_wrap_file_name = output_wrap_file_name
        self.cur_namespace_path = []
        self.lifecycle_traits = None
        self.inheritance_traits = None
        self.loader_traits = None
        self.api_defines_generated = False
        self.generated_files = []

    def generate(self):
        self.params_description = ParamsParser.load(self.input_params)
        self.api_description = Parser.load(self.input_xml)
        self.loader_traits = create_loader_traits(self.params_description.m_dynamically_load_functions, self)
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        if self.params_description.m_generate_single_file:
            output_file = os.path.join(self.output_folder, self.params_description.m_single_header_name)
            self.__set_output_header(FileGenerator.FileGenerator(output_file))
        self.__set_output_source(FileGenerator.FileGenerator(self.output_wrap_file_name))
        self.__process_source_begin()
        for namespace in self.api_description.m_namespaces:
            self.__process_namespace(self.output_folder, namespace, '')
        del self.loader_traits

    def get_namespace_id(self):
        return '_'.join(self.cur_namespace_path)

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

    def __process_namespace(self, base_path, namespace, namespace_prefix):
        self.cur_namespace_path.append(namespace.m_name)

        output_folder = base_path
        if self.params_description.m_folder_per_namespace and not self.params_description.m_generate_single_file:
            output_folder = os.path.join(base_path, namespace.m_name)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

        for nested_namespace in namespace.m_namespaces:
            self.__process_namespace(output_folder, nested_namespace, namespace_prefix+namespace.m_name)

        self.api_defines_generated = False
        if not self.params_description.m_generate_single_file:
            if not self.params_description.m_file_per_class or self.params_description.m_generate_namespace_header:
                output_file = namespace.m_name + '.h'
                if not self.params_description.m_folder_per_namespace:
                    output_file = namespace_prefix + namespace.m_name + '.h'
                namespace_folder = output_folder
                if self.params_description.m_namespace_header_at_parent_folder:
                    namespace_folder = base_path
                self.__set_output_header(FileGenerator.FileGenerator(os.path.join(namespace_folder, output_file)))
                if self.params_description.m_generate_namespace_header:
                    self.__process_namespace_header(namespace)
        if len(self.cur_namespace_path) == 1 and not self.api_defines_generated:
            self.loader_traits.generate_c_functions_declarations()

        for cur_class in namespace.m_classes:
            self.__process_class(output_folder, cur_class)

        self.cur_namespace_path.pop()

    def __process_namespace_header(self, namespace):
        self.output_header.put_copyright_header(self.params_description.m_copyright_header)
        self.output_header.put_automatic_generation_warning(self.params_description.m_automatic_generated_warning)

        watchdog_string = '{0}_INCLUDED'.format(self.get_namespace_id().upper())
        self.output_header.put_line('#ifndef {0}'.format(watchdog_string))
        self.output_header.put_line('#define {0}'.format(watchdog_string))
        self.output_header.put_line('')
        if len(self.cur_namespace_path) == 1 and not self.api_defines_generated:
            self.loader_traits.generate_c_functions_declarations()
        self.loader_traits.add_impl_header(namespace.m_implementation_header)

        self.output_header.put_line('')

        if self.params_description.m_file_per_class and not self.params_description.m_generate_single_file:
            for cur_class in namespace.m_classes:
                cur_class_file = posixpath.join('/'.join(self.cur_namespace_path), cur_class.m_name + '.h')
                self.output_header.put_line('#include "{0}"'.format(cur_class_file))

        if namespace.m_factory_functions or namespace.m_functions:
            self.output_header.put_line('')
            self.output_header.put_line('#ifdef __cplusplus')
            self.output_header.put_line('')
            for cur_namespace in self.cur_namespace_path:
                self.output_header.put_line('namespace {0} {{ '.format(cur_namespace), '')
            self.output_header.put_line('')
            self.output_header.put_line('')
            for function in namespace.m_functions:
                self.__process_function(function)
            for factory_function in namespace.m_factory_functions:
                self.__process_factory_function(factory_function)
            self.output_header.put_line('')
            for cur_namespace in self.cur_namespace_path:
                self.output_header.put_line('}', '')
            self.output_header.put_line('')
            self.output_header.put_line('')
            self.output_header.put_line('#endif /* __cplusplus */')

        self.output_header.put_line('')
        self.output_header.put_line('#endif /* {0} */'.format(watchdog_string))

    def __process_class(self, base_path, cur_class):
        self.cur_namespace_path.append(cur_class.m_name)
        self.lifecycle_traits = create_lifecycle_traits(cur_class, self)
        self.inheritance_traits = create_inheritance_traits(cur_class, self)

        if self.params_description.m_file_per_class and not self.params_description.m_generate_single_file:
            output_file = os.path.join(base_path, cur_class.m_name + '.h')
            self.__set_output_header(FileGenerator.FileGenerator(output_file))

        self.output_header.put_copyright_header(self.params_description.m_copyright_header)
        self.output_header.put_automatic_generation_warning(self.params_description.m_automatic_generated_warning)

        watchdog_string = '{0}_INCLUDED'.format(self.get_namespace_id().upper())
        self.output_header.put_line('#ifndef {0}'.format(watchdog_string))
        self.output_header.put_line('#define {0}'.format(watchdog_string))
        self.output_header.put_line('')

        self.output_header.put_line('#ifdef __cplusplus')
        self.output_header.put_line('')

        for cur_namespace in self.cur_namespace_path[:-1]:
            self.output_header.put_line('namespace {0} {{ '.format(cur_namespace), '')
        self.output_header.put_line('')
        self.output_header.put_line('')

        self.__generate_class(cur_class)

        for cur_namespace in self.cur_namespace_path[:-1]:
            self.output_header.put_line('}', '')
        self.output_header.put_line('')

        self.output_header.put_line('')
        self.output_header.put_line('#endif /* __cplusplus */ ')

        self.output_header.put_line('')
        self.output_header.put_line('#endif /* {0} */'.format(watchdog_string))
        del self.inheritance_traits
        del self.lifecycle_traits
        self.cur_namespace_path.pop()

    def __generate_class(self, cur_class):
        self.loader_traits.add_impl_header(cur_class.m_implementation_class_header)
        self.output_header.put_line('class {0}'.format(cur_class.m_name))
        self.output_header.put_line('{')
        self.output_header.put_line('protected:')
        with FileGenerator.Indent(self.output_header):
            self.inheritance_traits.generate_pointer_declaration()
            self.inheritance_traits.generate_set_object()
        self.output_header.put_line('public:')
        with FileGenerator.Indent(self.output_header):
            self.lifecycle_traits.generate_copy_constructor()
            self.lifecycle_traits.generate_void_constructor()
            for constructor in cur_class.m_constructors:
                self.inheritance_traits.generate_constructor(constructor)
            self.lifecycle_traits.generate_destructor()
            for method in cur_class.m_methods:
                self.__generate_method(method, cur_class)
        self.output_header.put_line('};')

    def __generate_method(self, method, cur_class):
        return_instruction = 'return ' if method.m_return else ''
        return_type = self.get_flat_type(method.m_return)
        self.cur_namespace_path.append(method.m_name)
        self.output_header.put_line('{return_type} {method_name}({arguments})'.format(
            return_type=return_type,
            method_name=method.m_name,
            arguments=Helpers.get_arguments_list_for_declaration(method.m_arguments)))
        with FileGenerator.IndentScope(self.output_header):
            self.output_header.put_line('{return_instruction}{c_function}({this_argument}{arguments});'.format(
                return_instruction=return_instruction,
                c_function=self.get_namespace_id().lower(),
                this_argument=Constants.object_var,
                arguments=Helpers.get_arguments_list_for_c_call(method.m_arguments)
            ))
        c_function_declaration = '{return_type} {c_function}({arguments})'.format(
            return_type=return_type,
            c_function=self.get_namespace_id().lower(),
            arguments=Helpers.get_arguments_list_for_wrap_declaration(method.m_arguments)
        )
        self.loader_traits.add_c_function_declaration(c_function_declaration)
        with FileGenerator.IndentScope(self.output_source):
            self.output_source.put_line('{0}* self = static_cast<{0}*>(object_pointer);'.format(
                cur_class.m_implementation_class_name
            ))
            self.output_source.put_line('{0}self->{1}({2});'.format(
                return_instruction,
                method.m_name,
                ', '.join(self.get_unwrapped_arguments(method.m_arguments))
            ))
        self.output_source.put_line('')
        self.cur_namespace_path.pop()

    def __process_function(self, function):
        return_type = self.get_flat_type(function.m_return)
        self.output_header.put_line('{return_type} {c_function}({arguments})'.format(
            return_type=return_type,
            c_function=self.get_namespace_id().lower() + '_' + function.m_name.lower(),
            arguments=Helpers.get_arguments_list_for_c_call(function.m_arguments)
        ))

    def __process_factory_function(self, factory_function):
        if not self.__is_class_type(factory_function.m_return):
            print('Factory {0} does not return class type'.format(factory_function.m_name))
            raise ValueError

        return_type = self.get_flat_type(factory_function.m_return)
        c_function_name = self.get_namespace_id().lower() + Helpers.pascal_to_stl(factory_function.m_name)
        c_function_declaration = '{return_type} {c_function}({arguments})'.format(
            return_type=return_type,
            c_function=c_function_name,
            arguments=Helpers.get_arguments_list_for_declaration(factory_function.m_arguments)
        )
        self.loader_traits.add_c_function_declaration(c_function_declaration)
        with FileGenerator.IndentScope(self.output_source):
            self.output_source.put_line('return {function_name}({arguments});'.format(
                function_name=factory_function.m_name
                if not factory_function.m_implementation_name else factory_function.m_implementation_name,
                arguments=', '.join(self.get_unwrapped_arguments(factory_function.m_arguments))
            ))
        self.output_source.put_line('')
        self.output_header.put_line('inline {return_type} {function_name}({arguments})'.format(
            return_type=self.get_cpp_type(factory_function.m_return),
            function_name=factory_function.m_name,
            arguments=Helpers.get_arguments_list_for_c_call(factory_function.m_arguments)
        ))
        with FileGenerator.IndentScope(self.output_header):
            self.output_header.put_line('return {return_type}({c_function}({arguments}));'.format(
                return_type=self.get_cpp_type(factory_function.m_return),
                c_function=c_function_name,
                arguments=Helpers.get_arguments_list_for_c_call(factory_function.m_arguments)
            ))
        self.output_header.put_line('')

    def __process_source_begin(self):
        self.output_source.put_copyright_header(self.params_description.m_copyright_header)
        self.output_source.put_automatic_generation_warning(self.params_description.m_automatic_generated_warning)

    def __is_class_type(self, type_name):
        path_to_class = type_name.split('::')
        return self.__is_class_type_impl(path_to_class, self.api_description.m_namespaces)

    def __is_class_type_impl(self, path_to_class, classes_or_namespaces):
        for class_or_namespace in classes_or_namespaces:
            if class_or_namespace.m_name == path_to_class[0]:
                if len(path_to_class) == 1:
                    return True
                elif len(path_to_class) == 2:
                    return self.__is_class_type_impl(path_to_class[1:], class_or_namespace.m_classes)
                else:
                    return self.__is_class_type_impl(path_to_class[1:], class_or_namespace.m_namespaces)
        return False

    def get_unwrapped_argument(self, argument):
        if self.__is_class_type(argument.m_type):
            return 'static_cast<{0}*>({1})'.format(argument.m_type, argument.m_name)
        else:
            return argument.m_name

    def get_unwrapped_arguments(self, arguments):
        return [self.get_unwrapped_argument(argument) for argument in arguments]

    def __set_output_header(self, header):
        self.generated_files.append(header)
        self.output_header = header

    def __set_output_source(self, source):
        self.generated_files.append(source)
        self.output_source = source


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
