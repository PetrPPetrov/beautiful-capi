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
from LifecycleTraits import create_lifecycle_traits
from InheritanceTraits import create_inheritance_traits
import FileGenerator
import Parser
import ParamsParser


class CapiGenerator(object):
    def __init__(self, input_filename, input_params_filename, output_folder):
        self.input_xml = parse(input_filename)
        self.input_params = parse(input_params_filename)
        self.output_folder = output_folder
        self.api_description = None
        self.params_description = None
        self.output_header = None
        self.cur_namespace_path = []
        self.lifecycle_traits = None
        self.inheritance_traits = None

    @staticmethod
    def __get_arguments_list_for_declaration(arguments):
        return ', '.join(['{0} {1}'.format(argument.m_type, argument.m_name) for argument in arguments])

    @staticmethod
    def __get_arguments_list_for_constructor_call(arguments):
        return ', '.join(['{0}'.format(argument.m_name) for argument in arguments])

    @staticmethod
    def __get_arguments_list_for_c_call(arguments):
        result = CapiGenerator.__get_arguments_list_for_constructor_call(arguments)
        return ', {0}'.format(result) if result else ''

    @staticmethod
    def __get_c_function_name(full_qualified_method_name):
        parsed_name = full_qualified_method_name.split('::')
        return '_'.join(parsed_name)

    def generate(self):
        self.params_description = ParamsParser.load(self.input_params)
        self.api_description = Parser.load(self.input_xml)
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        if self.params_description.m_generate_single_file:
            output_file = os.path.join(self.output_folder,self.params_description.m_single_header_name)
            self.output_header = FileGenerator.FileGenerator(output_file)
        for namespace in self.api_description.m_namespaces:
            self.__process_namespace(self.output_folder, namespace, '')

    def get_namespace_id(self):
        return '_'.join(self.cur_namespace_path)

    def __process_namespace(self, base_path, namespace, namespace_prefix):
        self.cur_namespace_path.append(namespace.m_name)

        output_folder = base_path
        if self.params_description.m_folder_per_namespace and not self.params_description.m_generate_single_file:
            output_folder = os.path.join(base_path, namespace.m_name)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

        for nested_namespace in namespace.m_namespaces:
            self.__process_namespace(output_folder, nested_namespace, namespace_prefix+namespace.m_name)

        if not self.params_description.m_generate_single_file:
            if not self.params_description.m_file_per_interface or self.params_description.m_generate_namespace_header:
                output_file = namespace.m_name + '.h'
                if not self.params_description.m_folder_per_namespace:
                    output_file = namespace_prefix + namespace.m_name + '.h'
                namespace_folder = output_folder
                if self.params_description.m_namespace_header_at_parent_folder:
                    namespace_folder = base_path
                self.output_header = FileGenerator.FileGenerator(os.path.join(namespace_folder, output_file))
                if self.params_description.m_generate_namespace_header:
                    self.__process_namespace_header(namespace, output_folder)

        for interface in namespace.m_interfaces:
            self.__process_interface(output_folder, interface)

        self.cur_namespace_path.pop()

    def __process_namespace_header(self, namespace, base_path_for_files):
        self.output_header.put_copyright_header(self.params_description.m_copyright_header)
        self.output_header.put_automatic_generation_warning(self.params_description.m_automatic_generated_warning)

        watchdog_string = '{0}_INCLUDED'.format(self.get_namespace_id().upper())
        self.output_header.put_line('#ifndef {0}'.format(watchdog_string))
        self.output_header.put_line('#define {0}'.format(watchdog_string))
        self.output_header.put_line('')
        if self.params_description.m_file_per_interface and not self.params_description.m_generate_single_file:
            for interface in namespace.m_interfaces:
                cur_interface_file = posixpath.join('/'.join(self.cur_namespace_path), interface.m_name + '.h')
                self.output_header.put_line('#include "{0}"'.format(cur_interface_file))

        self.output_header.put_line('')
        self.output_header.put_line('#endif // {0}'.format(watchdog_string))

    def __process_interface(self, base_path, interface):
        self.cur_namespace_path.append(interface.m_name)
        self.lifecycle_traits = create_lifecycle_traits(interface, self)
        self.inheritance_traits = create_inheritance_traits(interface, self)

        if self.params_description.m_file_per_interface and not self.params_description.m_generate_single_file:
            output_file = os.path.join(base_path, interface.m_name + '.h')
            self.output_header = FileGenerator.FileGenerator(output_file)

        self.output_header.put_copyright_header(self.params_description.m_copyright_header)
        self.output_header.put_automatic_generation_warning(self.params_description.m_automatic_generated_warning)

        watchdog_string = '{0}_INCLUDED'.format(self.get_namespace_id().upper())
        self.output_header.put_line('#ifndef {0}'.format(watchdog_string))
        self.output_header.put_line('#define {0}'.format(watchdog_string))
        self.output_header.put_line('')

        for cur_namespace in self.cur_namespace_path:
            self.output_header.put_line('namespace {0} {{ '.format(cur_namespace), '')
        self.output_header.put_line('')
        self.output_header.put_line('')

        self.__generate_class(interface)

        self.output_header.put_line('')
        for cur_namespace in self.cur_namespace_path:
            self.output_header.put_line('}', '')
        self.output_header.put_line('')

        self.output_header.put_line('')
        self.output_header.put_line('#endif // {0}'.format(watchdog_string))
        del self.inheritance_traits
        del self.lifecycle_traits
        self.cur_namespace_path.pop()

    def __generate_class(self, interface):
        self.output_header.put_line('class {0}'.format(interface.m_name))
        self.output_header.put_line('{')
        self.output_header.put_line('protected:')
        with FileGenerator.Indent(self.output_header):
            self.inheritance_traits.generate_pointer_declaration()
            self.inheritance_traits.generate_protected_constructor()
        self.output_header.put_line('public:')
        with FileGenerator.Indent(self.output_header):
            for constructor in interface.m_constructors:
                self.__generate_method(constructor, interface.m_name, CapiGenerator.__generate_constructor_body)
            self.lifecycle_traits.generate_destructor()
            for method in interface.m_methods:
                self.__generate_method(method, method.m_name, CapiGenerator.__generate_method_body)
        self.output_header.put_line('};')

    def __generate_method(self, method, method_name, generate_body_method):
        self.cur_namespace_path.append(method.m_name)
        self.output_header.put_line('{0}({1})'.format(
            method_name,
            CapiGenerator.__get_arguments_list_for_declaration(method.m_arguments)))
        self.output_header.put_line('{')
        with FileGenerator.Indent(self.output_header):
            generate_body_method(self, method)
        self.output_header.put_line('}')
        self.cur_namespace_path.pop()

    def __generate_constructor_body(self, method):
        if not self.params_description.m_dynamically_load_functions:
            self.output_header.put_line('m_pointer = {c_function}({arguments});'.format(
                c_function=self.get_namespace_id().lower(),
                arguments=CapiGenerator.__get_arguments_list_for_constructor_call(method.m_arguments)
            ))
        else:
            raise NotImplementedError

    def __generate_method_body(self, method):
        if not self.params_description.m_dynamically_load_functions:
            return_instruction = 'return ' if method.m_return else ''
            self.output_header.put_line('{return_instruction}{c_function}({this_argument}{arguments});'.format(
                return_instruction=return_instruction,
                c_function=self.get_namespace_id().lower(),
                this_argument='m_pointer',
                arguments=CapiGenerator.__get_arguments_list_for_c_call(method.m_arguments)
            ))
        else:
            raise NotImplementedError

    def __is_interface_type(self, type_name):
        path_to_interface = type_name.split('::')
        return self.__is_interface_type_impl(path_to_interface, self.api_description.m_namespaces)

    def __is_interface_type_impl(self, path_to_interface, interfaces_or_namespaces):
        for interface_or_namespace in interfaces_or_namespaces:
            if interface_or_namespace.m_name == path_to_interface[0]:
                if len(path_to_interface) == 1:
                    return True
                elif len(path_to_interface) == 2:
                    return self.__is_interface_type_impl(path_to_interface[1:],interface_or_namespace.m_interfaces)
                else:
                    return self.__is_interface_type_impl(path_to_interface[1:],interface_or_namespace.m_namespaces)
        return False




def main():
    print(
        'Beautifull Capi  Copyright (C) 2015  Petr Petrovich Petrov\n'
        'This program comes with ABSOLUTELY NO WARRANTY;\n'
        'This is free software, and you are welcome to redistribute it\n'
        'under certain conditions.\n')

    parser = argparse.ArgumentParser(
        prog='Beautifull Capi',
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

    args = parser.parse_args()

    schema_generator = CapiGenerator(args.input, args.params, args.output_folder)
    schema_generator.generate()

main()
