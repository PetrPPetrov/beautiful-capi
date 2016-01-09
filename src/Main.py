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
import argparse
from xml.dom.minidom import parse
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

    def __process_namespace(self, base_path, namespace, namespace_prefix):
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
                    self.__process_namespace_header(namespace)

        for interface in namespace.m_interfaces:
            self.__process_interface(output_folder, interface)

    def __process_namespace_header(self, namespace):
        pass

    def __process_interface(self, base_path, interface):
        if self.params_description.m_file_per_interface and not self.params_description.m_generate_single_file:
            output_file = os.path.join(base_path, interface.m_name + '.h')
            self.output_header = FileGenerator.FileGenerator(output_file)

        self.output_header.put_copyright_header(self.params_description.m_copyright_header)
        self.output_header.put_automatic_generation_warning(self.params_description.m_automatic_generated_warning)


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
