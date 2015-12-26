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
import FileGenerator
from xml.dom.minidom import parse


class SchemaGenerator(object):
    def __init__(self, input_filename, output_filename):
        self.input_xsd = parse(input_filename)
        self.output_file = FileGenerator.FileGenerator(output_filename)

    def build_python_scripts(self):
        self.output_file.put_python_header()
        self.output_file.put_gnu_gpl_copyright_header(False)
        self.output_file.put_autogeneration_warning()
        for complex_type in self.input_xsd.getElementsByTagName("xs:complexType"):
            self.__build_structure(complex_type)

    def __build_structure(self, complex_type):
        self.output_file.put_line('class {0}(object):'.format(complex_type.getAttribute('name')))
        with FileGenerator.Indent(self.output_file):
            self.__build_structure_impl(complex_type)

    def __build_structure_impl(self, complex_type):
        self.output_file.put_line('def __init__(self):')
        pass


def main():
    print(
        'Xsd2Python3  Copyright (C) 2015  Petr Petrovich Petrov\n'
        'This program comes with ABSOLUTELY NO WARRANTY;\n'
        'This is free software, and you are welcome to redistribute it\n'
        'under certain conditions.\n')

    parser = argparse.ArgumentParser(
        prog='Xsd2Python3',
        description='This program converts XSD schemas to Python 3 data structures and parser scripts.')

    parser.add_argument(
        '-i', '--input', nargs=None, default='capi.xsd',
        help='specifies input API description file')
    parser.add_argument(
        '-o', '--output', nargs=None, default='Parser.py',
        help='specifies generated output Python 3 file')

    args = parser.parse_args()

    schema_generator = SchemaGenerator(args.input, args.output)
    schema_generator.build_python_scripts()

main()
