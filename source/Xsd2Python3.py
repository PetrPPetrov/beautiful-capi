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
from xml.dom.minidom import parse
import FileGenerator


def string_to_bool(string_value):
    return string_value.lower() in ['true', 'on', 'yes', '1']


def get_name_for_field(element):
    name = element.getAttribute('name')
    if name == 'return':
        name = 'return_type'
    elif name == 'return_filled':
        name = 'return_type_filled'
    if name == 'type':
        name = 'type_name'
    elif name == 'type_filled':
        name = 'type_name_filled'
    return name


class SchemaGenerator(object):
    def __init__(self, input_filename, output_filename):
        self.input_xsd = parse(input_filename)
        self.output_file = FileGenerator.FileGenerator(output_filename)

    def build_python_scripts(self):
        self.output_file.put_python_header()
        self.output_file.put_python_gnu_gpl_copyright_header()
        self.output_file.put_python_automatic_generation_warning()
        self.output_file.put_line('from enum import Enum\n\n')
        self.__build_string_to_bool()
        for simple_type in self.input_xsd.getElementsByTagName('xs:simpleType'):
            self.__build_enum(simple_type)
        for complex_type in self.input_xsd.getElementsByTagName('xs:complexType'):
            self.__build_structure(complex_type)
        self.__build_load_root()

    def __build_string_to_bool(self):
        self.output_file.put_line('def string_to_bool(string_value):')
        with FileGenerator.Indent(self.output_file):
            self.output_file.put_line('return string_value.lower() in ["true", "on", "yes", "1"]')
        self.output_file.put_line('')
        self.output_file.put_line('')

    def __build_load_root(self):
        self.output_file.put_line('def load(dom_node):')
        with FileGenerator.Indent(self.output_file):
            for root_element in self.input_xsd.childNodes:
                for element in root_element.childNodes:
                    if element.nodeName == 'xs:element':
                        self.output_file.put_line(
                            'for root_element in [root for root in dom_node.childNodes if root.localName == "{0}"]:'
                            .format(get_name_for_field(element))
                        )
                        with FileGenerator.Indent(self.output_file):
                            self.output_file.put_line('root_params = {0}()'.format(element.getAttribute('type')))
                            self.output_file.put_line('root_params.load(root_element)')
                            self.output_file.put_line('return root_params')

    def __build_enum(self, enumerator):
        self.output_file.put_line('class {enum_name}(Enum):'.format(enum_name=get_name_for_field(enumerator)))
        enum_counter = 0
        with FileGenerator.Indent(self.output_file):
            for enumeration in enumerator.getElementsByTagName('xs:enumeration'):
                self.output_file.put_line('{0} = {1}'.format(
                    enumeration.getAttribute('value'),
                    enum_counter)
                )
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
                            get_name_for_field(enumerator),
                            enumeration.getAttribute('value')
                        ))
                self.output_file.put_line('raise ValueError')
        self.output_file.put_line('')
        self.output_file.put_line('')

    def __build_structure(self, complex_type):
        base_class = 'object'
        for cur_base_class in complex_type.getElementsByTagName('xs:extension'):
            base_class = cur_base_class.getAttribute('base')
        self.output_file.put_line('class {0}({1}):'.format(get_name_for_field(complex_type), base_class))
        with FileGenerator.Indent(self.output_file):
            self.__build_structure_impl(complex_type, base_class)
        self.output_file.put_line('')

    def __build_structure_impl(self, complex_type, base_class):
        self.output_file.put_line('def __init__(self):')
        with FileGenerator.Indent(self.output_file):
            if base_class != 'object':
                self.output_file.put_line('super().__init__()')
            self.__build_constructor(complex_type)
        self.output_file.put_line('')
        self.output_file.put_line('def load(self, dom_node):')
        with FileGenerator.Indent(self.output_file):
            if base_class != 'object':
                self.output_file.put_line('super().load(dom_node)')
            self.__build_load(complex_type)
        self.output_file.put_line('')

    @staticmethod
    def __get_array_name(name):
        return '{0}{1}'.format(name, 'es' if name[-1] == 's' else 's')

    @staticmethod
    def __get_attribute_default_value(attribute):
        if attribute.getAttribute('type') == 'xs:string':
            if attribute.hasAttribute('default'):
                return '"' + attribute.getAttribute('default') + '"'
            return '""'
        if attribute.getAttribute('type') == 'xs:boolean':
            if attribute.hasAttribute('default'):
                return str(string_to_bool(attribute.getAttribute('default')))
            return "False"
        if attribute.hasAttribute('default'):
            return attribute.getAttribute('type') + '.' + attribute.getAttribute('default')

    def __build_constructor(self, complex_type):
        for attribute in complex_type.getElementsByTagName('xs:attribute'):
            self.__build_init_field(attribute)
        for element in complex_type.getElementsByTagName('xs:element'):
            if element.getAttribute('type') == 'xs:string':
                self.__build_init_field(element)
            else:
                self.output_file.put_line('self.{0} = []'.format(
                    SchemaGenerator.__get_array_name(get_name_for_field(element))
                ))

    def __build_init_field(self, field):
        #TODO
        self.output_file.put_line('self.{0} = {1}'.format(
                get_name_for_field(field),
                self.__get_attribute_default_value(field)
        ))
        #TODO
        self.output_file.put_line('self.{0}_filled = False'.format(get_name_for_field(field)))

    def __build_load(self, complex_type):
        for element in complex_type.getElementsByTagName('xs:element'):
            self.__build_load_element(element)
        for attribute in complex_type.getElementsByTagName('xs:attribute'):
            self.__build_load_attribute(attribute)

    def __build_load_element(self, element):
        self.output_file.put_line(
                'for element in [node for node in dom_node.childNodes if node.nodeName == "{0}"]:'.format(
                    get_name_for_field(element)
                )
            )
        with FileGenerator.Indent(self.output_file):
            if element.getAttribute('type') == 'xs:string':
                self.output_file.put_line(
                    'for text in [text for text in element.childNodes if text.nodeType == text.TEXT_NODE]:'
                )
                with FileGenerator.Indent(self.output_file):
        #TODO
                    self.output_file.put_line('self.{0} += text.nodeValue'.format(get_name_for_field(element)))
            else:
                self.output_file.put_line('new_element = {0}()'.format(element.getAttribute('type')))
                self.output_file.put_line('new_element.load(element)')
                self.output_file.put_line('self.{0}.append(new_element)'.format(
                    SchemaGenerator.__get_array_name(get_name_for_field(element))
                ))

    def __build_load_attribute(self, attribute):
        self.output_file.put_line('if dom_node.hasAttribute("{0}"):'.format(get_name_for_field(attribute)))
        with FileGenerator.Indent(self.output_file):
            self.output_file.put_line('cur_attr = dom_node.getAttribute("{0}")'.format(
                get_name_for_field(attribute)
            ))
            if attribute.getAttribute('type') == 'xs:string':
        #TODO
                self.output_file.put_line('self.{0} = cur_attr'.format(
                    get_name_for_field(attribute)
                ))
            elif attribute.getAttribute('type') == 'xs:boolean':
        #TODO
                self.output_file.put_line('self.{0} = string_to_bool(cur_attr)'.format(
                    get_name_for_field(attribute)
                ))
            else:
        #TODO
                self.output_file.put_line('self.{0} = {1}.load(cur_attr)'.format(
                    get_name_for_field(attribute),
                    attribute.getAttribute('type')
                ))
        #TODO
            self.output_file.put_line('self.{0}_filled = True'.format(get_name_for_field(attribute)))


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
