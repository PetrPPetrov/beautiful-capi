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

    def generate(self):
        self.params_description = ParamsParser.load(self.input_params)
        self.api_description = Parser.load(self.input_xml)
        for namespace in self.api_description.m_namespaces:
            self.__process_namespace(self.output_folder, namespace)

    def __process_namespace(self, base_path, namespace):
        output_folder = os.path.join(base_path, namespace.m_name)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        for nested_namespace in namespace.m_namespaces:
            self.__process_namespace(output_folder, nested_namespace)
        for interface in namespace.m_interfaces:
            self.__process_interface(output_folder, interface)
        #namespace_header = os.path.join(base_path, namespace.m_name + '.h')

    def __process_interface(self, base_path, interface):
        output_file = os.path.join(base_path, interface.m_name + '.h')
        output_header = FileGenerator.FileGenerator(output_file)
        output_header.put_line(self.params_description.m_copyright_header)
        output_header.put_line(self.params_description.m_automatic_generated_warning)


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
