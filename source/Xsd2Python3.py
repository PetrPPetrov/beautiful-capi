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


def string_to_int(string_value):
    return int(string_value)


def get_name_for_field(element):
    name = element.getAttribute('name')
    if name == 'return':
        name = 'return_type'
    elif name == 'return_filled':
        name = 'return_type_filled'
    elif name == 'type':
        name = 'type_name'
    elif name == 'type_filled':
        name = 'type_name_filled'
    return name


def copy_source(output_file, code_object):
    import inspect
    for line in inspect.getsourcelines(code_object)[0]:
        output_file.put_line(line.strip('\n'))
    output_file.put_line('')
    output_file.put_line('')


class SchemaGenerator(object):
    def __init__(self, input_filename, output_filename):
        self.input_xsd = parse(input_filename)
        self.output_file = FileGenerator.FileGenerator(output_filename)

    def build_python_scripts(self):
        self.output_file.put_python_header()
        self.output_file.put_python_gnu_gpl_copyright_header()
        self.output_file.put_python_automatic_generation_warning()
        self.output_file.put_line('from enum import Enum\n\n')

        copy_source(self.output_file, string_to_bool)
        copy_source(self.output_file, string_to_int)
        for simple_type in self.input_xsd.getElementsByTagName('xs:simpleType'):
            self.__build_enum(simple_type)
        for complex_type in self.input_xsd.getElementsByTagName('xs:complexType'):
            self.__build_structure(complex_type)
        self.__build_load_root()
        del self.output_file

    def __build_load_root(self):
        self.output_file.put_line('def load(dom_node):')
        with FileGenerator.Indent(self.output_file):
            for root_element in self.input_xsd.childNodes:
                for element in root_element.childNodes:
                    if element.nodeName == 'xs:element':
                        self.output_file.put_line(
                            'for root_element in [root for root in dom_node.childNodes if root.localName == "{0}"]:'
                            .format(element.getAttribute('name'))
                        )
                        with FileGenerator.Indent(self.output_file):
                            self.output_file.put_line('root_params = {0}()'.format(element.getAttribute('type')))
                            self.output_file.put_line('root_params.load(root_element)')
                            self.output_file.put_line('return root_params')

    def __build_enum(self, enumerator):
        self.output_file.put_line('class {enum_name}(Enum):'.format(enum_name=enumerator.getAttribute('name')))
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
        self.output_file.put_line('class {0}({1}):'.format(complex_type.getAttribute('name'), base_class))
        with FileGenerator.Indent(self.output_file):
            self.__build_structure_impl(complex_type, base_class)
        self.output_file.put_line('')

    def __build_structure_impl(self, complex_type, base_class):
        self.__build_constructor(complex_type, base_class)
        self.output_file.put_line('')
        self.__build_load_element(complex_type, base_class)
        self.output_file.put_line('')
        self.__build_load_attributes(complex_type, base_class)
        self.output_file.put_line('')
        self.__build_load()
        self.output_file.put_line('')

    @staticmethod
    def __get_array_name(name):
        if name == 'returns':
            return name
        suffix = 's'
        prefix = name
        if name[-1] == 's' or name[-1] == 'x':
            suffix = 'es'
        elif name[-1] == 'y':
            suffix = 'ies'
            prefix = name[:-1]
        return '{0}{1}'.format(prefix, suffix)

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
        if attribute.getAttribute('type') == 'xs:integer':
            if attribute.hasAttribute('default'):
                return str(string_to_int(attribute.getAttribute('default')))
            return 0
        if attribute.hasAttribute('default'):
            return attribute.getAttribute('type') + '.' + attribute.getAttribute('default')

    def __build_constructor(self, complex_type, base_class):
        self.output_file.put_line('def __init__(self):')
        with FileGenerator.Indent(self.output_file):
            if base_class != 'object':
                self.output_file.put_line('super().__init__()')
            else:
                self.output_file.put_line('self.all_items = []')
            for attribute in complex_type.getElementsByTagName('xs:attribute'):
                self.__build_init_field(attribute)
            for element in complex_type.getElementsByTagName('xs:element'):
                self.output_file.put_line('self.{0} = []'.format(
                    SchemaGenerator.__get_array_name(get_name_for_field(element))
                ))

    def __build_init_field(self, field):
        self.output_file.put_line('self.{0} = {1}'.format(
                get_name_for_field(field),
                self.__get_attribute_default_value(field)
        ))
        self.output_file.put_line('self.{0}_filled = False'.format(get_name_for_field(field)))

    def __build_load_element_item(self, element, mixed):
        self.output_file.put_line('if element.nodeName == "{0}":'.format(element.getAttribute('name')))
        with FileGenerator.Indent(self.output_file):
            if element.getAttribute('type') == 'xs:string':
                self.output_file.put_line('new_element = "{0}"'.format(element.getAttribute('default')))
                self.output_file.put_line(
                    'for text in [text for text in element.childNodes if text.nodeType == text.TEXT_NODE]:'
                )
                with FileGenerator.Indent(self.output_file):
                    self.output_file.put_line('new_element += text.nodeValue')
            else:
                self.output_file.put_line('new_element = {0}()'.format(element.getAttribute('type')))
                self.output_file.put_line('new_element.load(element)')
            self.output_file.put_line('self.{0}.append(new_element)'.format(
                SchemaGenerator.__get_array_name(get_name_for_field(element))
            ))
            if mixed:
                self.output_file.put_line('self.all_items.append(new_element)')
            self.output_file.put_line('return True')

    def __build_load_element(self, complex_type, base_class):
        self.output_file.put_line('def load_element(self, element):')
        with FileGenerator.Indent(self.output_file):
            if base_class != 'object':
                self.output_file.put_line('if super().load_element(element):')
                with FileGenerator.Indent(self.output_file):
                    self.output_file.put_line('return True')
            mixed = complex_type.hasAttribute('mixed') and string_to_bool(complex_type.getAttribute('mixed'))
            for element in complex_type.getElementsByTagName('xs:element'):
                self.__build_load_element_item(element, mixed)
            if mixed:
                self.output_file.put_line('if element.nodeType == element.TEXT_NODE:')
                with FileGenerator.Indent(self.output_file):
                    self.output_file.put_line("cur_texts = [text.strip() for text in element.data.split('\\n')]")
                    self.output_file.put_line('first = True')
                    self.output_file.put_line('for text in cur_texts:')
                    with FileGenerator.Indent(self.output_file):
                        self.output_file.put_line(
                            'if first and self.all_items and type(self.all_items[-1]) is str:')
                        with FileGenerator.Indent(self.output_file):
                            self.output_file.put_line('self.all_items[-1] += text')
                        self.output_file.put_line('else:')
                        with FileGenerator.Indent(self.output_file):
                            self.output_file.put_line('self.all_items.append(text)')
                        self.output_file.put_line('first = False')
                    self.output_file.put_line('return True')
            self.output_file.put_line('return False')

    def __build_load_attributes(self, complex_type, base_class):
        self.output_file.put_line('def load_attributes(self, dom_node):')
        with FileGenerator.Indent(self.output_file):
            load_is_empty = True
            if base_class != 'object':
                load_is_empty = False
                self.output_file.put_line('super().load_attributes(dom_node)')
            for attribute in complex_type.getElementsByTagName('xs:attribute'):
                load_is_empty = False
                self.output_file.put_line('if dom_node.hasAttribute("{0}"):'.format(attribute.getAttribute('name')))
                with FileGenerator.Indent(self.output_file):
                    self.output_file.put_line('cur_attr = dom_node.getAttribute("{0}")'.format(
                        attribute.getAttribute('name')
                    ))
                    if attribute.getAttribute('type') == 'xs:string':
                        self.output_file.put_line('self.{0} = cur_attr'.format(
                            get_name_for_field(attribute)
                        ))
                    elif attribute.getAttribute('type') == 'xs:boolean':
                        self.output_file.put_line('self.{0} = string_to_bool(cur_attr)'.format(
                            get_name_for_field(attribute)
                        ))
                    elif attribute.getAttribute('type') == 'xs:integer':
                        self.output_file.put_line('self.{0} = string_to_int(cur_attr)'.format(
                            get_name_for_field(attribute)
                        ))
                    else:
                        self.output_file.put_line('self.{0} = {1}.load(cur_attr)'.format(
                            get_name_for_field(attribute),
                            attribute.getAttribute('type')
                        ))
                    self.output_file.put_line('self.{0}_filled = True'.format(get_name_for_field(attribute)))
            if load_is_empty:
                self.output_file.put_line('pass')

    def __build_load(self):
        self.output_file.put_line('def load(self, dom_node):')
        with FileGenerator.Indent(self.output_file):
            self.output_file.put_line('for element in dom_node.childNodes:')
            with FileGenerator.Indent(self.output_file):
                self.output_file.put_line('self.load_element(element)')
            self.output_file.put_line('self.load_attributes(dom_node)')


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


if __name__ == '__main__':
    main()
