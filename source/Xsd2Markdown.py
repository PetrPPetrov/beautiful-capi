#!/usr/bin/env python
#
# Beautiful Capi generates beautiful C API wrappers for your C++ classes
# Copyright (C) 2017 Petr Petrovich Petrov
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

from FileGenerator import FileGenerator, Indent


def get_attribute(node, attribute):
    if node.hasAttribute(attribute):
        attr = node.getAttribute(attribute)
        return attr if attr else '""'
    return '""'


def get_children_by_tag(node, tag: str):
    result = []
    for child in node.childNodes:
        if child.nodeName == tag:
            result.append(child)
    return result


def get_documentation(node):
    children = get_children_by_tag(node, 'xs:annotation')
    if children:
        doc = get_children_by_tag(children[0], 'xs:documentation')
        if doc:
            return doc[0].firstChild.data.strip()
    return ''


class MarkDownGenerator(object):
    def __init__(self, input_filename, output_filename):
        self.input_xsd = parse(input_filename)
        self.output_file = FileGenerator(output_filename)
        self.output_file.indent_size = 2
        self.types = []

    def __fill_types(self):
        for simple_type in self.input_xsd.getElementsByTagName('xs:simpleType'):
            self.types.append(simple_type.getAttribute('name'))
        for complex_type in self.input_xsd.getElementsByTagName('xs:complexType'):
            self.types.append(complex_type.getAttribute('name'))

    def build_markdown(self):
        self.__fill_types()
        self.put_automatic_generation_warning()
        for complex_type in self.input_xsd.getElementsByTagName('xs:complexType'):
            self.__build_complex_type(complex_type)
        for simple_type in self.input_xsd.getElementsByTagName('xs:simpleType'):
            self.__build_simple_type(simple_type)

    def __build_simple_type(self, simple_type):
        self.output_file.put_line('### {type}'.format(type=simple_type.getAttribute('name')))
        doc = get_documentation(simple_type)
        if doc:
            self.output_file.put_line(doc)
        restriction = get_children_by_tag(simple_type, 'xs:restriction')[0]
        if restriction:
            enums = restriction.getElementsByTagName('xs:enumeration')
            if enums:
                self.output_file.put_line('{type} is enumeration of {basic_type}'.format(
                    type=simple_type.getAttribute('name'),
                    basic_type=restriction.getAttribute('base')
                ))
                enum_elements = []
                for enum in enums:
                    enum_elements.append((enum.getAttribute('value'), get_documentation(enum), ))
                self.__build_table(
                    '{type}, possible values'.format(type=simple_type.getAttribute('name')),
                    ['Value', 'Description'],
                    enum_elements
                )
            # TODO: also add another possible values

    def __build_complex_type(self, complex_type):
        self.output_file.put_line('### {type}'.format(type=complex_type.getAttribute('name')))
        doc = get_documentation(complex_type)
        if doc:
            self.output_file.put_line(doc)
        complex_content = get_children_by_tag(complex_type, 'xs:complexContent')
        if complex_content:
            extension = get_children_by_tag(complex_content[0], 'xs:extension')
            if extension[0]:
                self.output_file.put_line('{type} is Inherited from {basic_type}'.format(
                    type=complex_type.getAttribute('name'),
                    basic_type=extension[0].getAttribute('base')
                ))
                extension[0].setAttribute('name', complex_type.getAttribute('name'))
                self.__build_attribute_table(extension[0])
                self.__build_element_table(extension[0])

        else:
            self.__build_attribute_table(complex_type)
            self.__build_element_table(complex_type)

    def __build_attribute_table(self, node):
        attributes = []
        for attribute in get_children_by_tag(node, 'xs:attribute'):
            element_type = get_attribute(attribute, 'type')
            if element_type in self.types:
                element_type = '<a href="#{lower_name}">{name}</a>'.format(
                    name=element_type,
                    lower_name=element_type.lower()
                )
            attributes.append((get_attribute(attribute, 'name'),
                               element_type,
                               get_attribute(attribute, 'use'),
                               get_documentation(attribute),
                               get_attribute(attribute, 'default'),
                               )
                              )
        if attributes:
            self.__build_table(
                '{name}, list of attributes'.format(name=node.getAttribute('name')),
                ['Attribute', 'Type', 'Use', 'Description', 'Default'],
                attributes
            )

    def __build_element_table(self, node):
        elements = []
        for element in node.getElementsByTagName('xs:element'):
            element_type = get_attribute(element, 'type')
            if element_type in self.types:
                element_type = '<a href="#{lower_name}">{name}</a>'.format(
                    name=element_type,
                    lower_name=element_type.lower()
                )
            elements.append((
                get_attribute(element, 'name'),
                '{min}..{max}'.format(
                     min=element.getAttribute('minOccurs') if element.hasAttribute('minOccurs') else 0,
                     max=element.getAttribute('maxOccurs') if element.hasAttribute('maxOccurs') else 'unbounded'
                 ),
                element_type,
                get_documentation(element),
            ))
        if elements:
            self.__build_table(
                '{name}, list of elements'.format(name=node.getAttribute('name')),
                ['Element', 'Multiplicity', 'Type', 'Description'],
                elements
            )

    def __build_table(self, caption: str, columns_names: [str], rows: [(str,)]):
        self.output_file.put_line('<table>')
        with Indent(self.output_file):
            self.output_file.put_line('<caption>{caption}</caption>'.format(caption=caption))
            self.output_file.put_line('<tr>')
            with Indent(self.output_file):
                for column_name in columns_names:
                    self.output_file.put_line('<td> {title} </td>'.format(title=column_name))
            self.output_file.put_line('</tr>')

            for row in rows:
                self.output_file.put_line('<tr>')
                with Indent(self.output_file):
                    for cell in row:
                        self.output_file.put_line('<td>')
                        with Indent(self.output_file):
                            self.output_file.put_line(cell)
                        self.output_file.put_line('</td>')
                self.output_file.put_line('</tr>')
        self.output_file.put_line('</table>')

    def put_automatic_generation_warning(self):
        self.output_file.put_line(
            'WARNING: This file was automatically generated by Xsd2Markdown.py program!\n'
            'Do not edit this file! Please edit the source XSD schema.\n'
            '\n'
        )


def main():
    print(
        'Xsd2Markdown  Copyright (C) 2015  Petr Petrovich Petrov\n'
        'This program comes with ABSOLUTELY NO WARRANTY;\n'
        'This is free software, and you are welcome to redistribute it\n'
        'under certain conditions.\n'
    )

    parser = argparse.ArgumentParser(
        prog='Xsd2Markdown',
        description='This program creates MarkDown description from XSD Schema annotation')

    parser.add_argument(
        '-i', '--input', nargs=None, default='Capi.xsd', metavar='INPUT',
        help='specifies input API description file')
    parser.add_argument(
        '-o', '--output', nargs=None, default='../doc/DescriptionSchema.md', metavar='OUTPUT',
        help='specifies generated MarkDown description')

    args = parser.parse_args()

    md_generator = MarkDownGenerator(args.input, args.output)
    md_generator.build_markdown()

if __name__ == '__main__':
    main()
