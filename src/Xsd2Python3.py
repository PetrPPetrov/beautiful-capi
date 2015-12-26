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
        self.output_file.put_line('from enum import Enum\n\n')
        for simple_type in self.input_xsd.getElementsByTagName('xs:simpleType'):
            self.__build_enum(simple_type)
        for complex_type in self.input_xsd.getElementsByTagName('xs:complexType'):
            self.__build_structure(complex_type)
        self.output_file.put_line('def load(dom_node):')
        with FileGenerator.Indent(self.output_file):
            for root_element in self.input_xsd.childNodes:
                for element in root_element.childNodes:
                    if element.nodeName == 'xs:element':
                        self.output_file.put_line('for root_element in dom_node.childNodes:')
                        #[root for root in dom_node.childNodes if root.nodeName == "{0}"]:'.format(element.getAttribute('name')))
                        # Another dummy
                        with FileGenerator.Indent(self.output_file):
                            self.output_file.put_line('root_params = {0}()'.format(element.getAttribute('type')))
                            self.output_file.put_line('root_params.load(root_element)')
                            self.output_file.put_line('return root_params')

    def __build_enum(self, enumerator):
        self.output_file.put_line('class {0}(Enum):'.format(enumerator.getAttribute('name')))
        enum_counter = 0
        with FileGenerator.Indent(self.output_file):
            for enumeration in enumerator.getElementsByTagName('xs:enumeration'):
                self.output_file.put_line('{0} = {1}'.format(
                    enumeration.getAttribute('value'),
                    enum_counter))
                enum_counter += 1
        self.output_file.put_line('')
        with FileGenerator.Indent(self.output_file):
            self.output_file.put_line('@staticmethod')
            self.output_file.put_line('def load(value):')
            with FileGenerator.Indent(self.output_file):
                for enumeration in enumerator.getElementsByTagName('xs:enumeration'):
                    self.output_file.put_line('if value == "{0}":'.format(enumeration.getAttribute('value')))
                    with FileGenerator.Indent(self.output_file):
                        self.output_file.put_line('return {0}.{1}'.format(
                            enumerator.getAttribute('name'),
                            enumeration.getAttribute('value')))
                self.output_file.put_line('raise ValueError')
        self.output_file.put_line('')
        self.output_file.put_line('')

    def __build_structure(self, complex_type):
        self.output_file.put_line('class {0}(object):'.format(complex_type.getAttribute('name')))
        with FileGenerator.Indent(self.output_file):
            self.__build_structure_impl(complex_type)
        self.output_file.put_line('')

    def __build_structure_impl(self, complex_type):
        self.output_file.put_line('def __init__(self):')
        with FileGenerator.Indent(self.output_file):
            self.__build_constructor(complex_type)
        self.output_file.put_line('')
        self.output_file.put_line('def load(self, dom_node):')
        with FileGenerator.Indent(self.output_file):
            self.__build_load(complex_type)
        self.output_file.put_line('')

    @staticmethod
    def __get_attribute_default_value(attribute):
        if attribute.getAttribute('type') == 'xs:string':
            if attribute.hasAttribute('default'):
                return '"' + attribute.getAttribute('default') + '"'
            return '""'
        if attribute.hasAttribute('default'):
            return attribute.getAttribute('type') + '.' + attribute.getAttribute('default')

    def __build_constructor(self, complex_type):
        for attribute in complex_type.getElementsByTagName('xs:attribute'):
            self.output_file.put_line('self.m_{0} = {1}'.format(
                attribute.getAttribute('name'),
                self.__get_attribute_default_value(attribute)
            ))
        for element in complex_type.getElementsByTagName('xs:element'):
            self.output_file.put_line('self.m_{0}s = []'.format(element.getAttribute('name')))

    def __build_load(self, complex_type):
        for element in complex_type.getElementsByTagName('xs:element'):
            self.__build_load_element(element)
        for attribute in complex_type.getElementsByTagName('xs:attribute'):
            self.__build_load_attribute(attribute)

    def __build_load_element(self, element):
        self.output_file.put_line(
            'for element in [node for node in dom_node.childNodes if node.nodeName == "{0}"]:'.format(
            element.getAttribute('name')))
        with FileGenerator.Indent(self.output_file):
            self.output_file.put_line('new_element = {0}()'.format(element.getAttribute('type')))
            self.output_file.put_line('new_element.load(element)')
            self.output_file.put_line('self.m_{0}s.append(new_element)'.format(element.getAttribute('name')))

    def __build_load_attribute(self, attribute):
        self.output_file.put_line('if dom_node.hasAttribute("{0}"):'.format(attribute.getAttribute('name')))
        with FileGenerator.Indent(self.output_file):
            self.output_file.put_line('cur_attr = dom_node.getAttribute("{0}")'.format(
                attribute.getAttribute('name')))
            if attribute.getAttribute('type') == 'xs:string':
                self.output_file.put_line('self.m_{0} = cur_attr'.format(
                    attribute.getAttribute('name')))
            else:
                self.output_file.put_line('self.m_{0} = {1}.load(cur_attr)'.format(
                    attribute.getAttribute('name'),
                    attribute.getAttribute('type')))

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
        '-i', '--input', nargs=None, default='capi.xsd', metavar='INPUT',
        help='specifies input API description file')
    parser.add_argument(
        '-o', '--output', nargs=None, default='Parser.py', metavar='OUTPUT',
        help='specifies generated output Python 3 file')

    args = parser.parse_args()

    schema_generator = SchemaGenerator(args.input, args.output)
    schema_generator.build_python_scripts()

main()
