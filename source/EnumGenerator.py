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


from ExternalNamespaceGenerator import ExternalNamespaceGenerator
from FileCache import FileCache
from NamespaceGenerator import NamespaceGenerator
from Parser import TEnumeration, TEnumerationItem, TNamespace, TBeautifulCapiRoot, TFunction, TClass, TArgument
from Parser import TImplementationCode
from FileGenerator import FileGenerator, IndentScope
from DoxygenCpp import DoxygenCppGenerator


class EnumGenerator(object):
    def __init__(self, enum_object: TEnumeration, parent_generator):
        self.enum_object = enum_object
        self.parent_generator = parent_generator

    @property
    def name(self) -> str:
        return self.enum_object.name

    @property
    def full_name_array(self) -> [str]:
        return self.parent_generator.full_name_array + [self.name]

    @property
    def full_name(self) -> str:
        return '::'.join([self.parent_generator.full_name, self.name])

    @property
    def wrap_name(self) -> str:
        return self.name

    @property
    def full_wrap_name(self) -> str:
        return '::'.join([self.parent_generator.full_wrap_name, self.wrap_name])

    @property
    def implementation_name(self) -> str:
        if self.enum_object.implementation_type_filled:
            return self.enum_object.implementation_type
        else:
            return '::'.join([self.parent_generator.implementation_name, self.name])

    @staticmethod
    def __get_enum_item_definition(enum_item: TEnumerationItem) -> str:
        if enum_item.value_filled:
            return '{name} = {value}'.format(name=enum_item.name, value=enum_item.value)
        else:
            return '{name}'.format(name=enum_item.name)

    def generate_enum_definition(self, out: FileGenerator):
        DoxygenCppGenerator().generate_for_enum(out, self.enum_object)
        out.put_line('enum {name}'.format(name=self.name))
        with IndentScope(out, '};'):
            items_definitions = [self.__get_enum_item_definition(enum_item) for enum_item in self.enum_object.items]
            items_definitions_with_comma = [item + ',' for item in items_definitions[:-1]]
            if items_definitions:
                items_definitions_with_comma.append(items_definitions[-1])
            for item_definition, item in zip(items_definitions_with_comma, self.enum_object.items):
                out.put_line(item_definition + DoxygenCppGenerator().get_for_enum_item(item))

    def declaration_header(self, file_cache: FileCache):
        parent_generator = self.parent_generator
        if isinstance(parent_generator, NamespaceGenerator) or isinstance(parent_generator, ExternalNamespaceGenerator):
            header = file_cache.enums_header(parent_generator.full_name_array)
        else:
            header = file_cache.class_header_decl(parent_generator.full_name_array)
        return header

    def definition_header(self, file_cache: FileCache):
        return self.declaration_header(file_cache)

    def generate_forward_declaration(self, out: FileGenerator):
        out.put_line('enum {name};'.format(name=self.name))

    def dependent_implementation_headers(self):
        result = []
        if self.enum_object.implementation_header_filled:
            result = [self.enum_object.implementation_header]
        parent_generator = self.parent_generator
        if not isinstance(parent_generator, NamespaceGenerator):
            if not isinstance(parent_generator, ExternalNamespaceGenerator):
                result += parent_generator.dependent_implementation_headers()
        return result

    @property
    def is_in_namespace(self):
        return self.parent_generator and (isinstance(self.parent_generator, NamespaceGenerator) or
                                          isinstance(self.parent_generator, ExternalNamespaceGenerator))


class EnumProcessor(object):
    def __init__(self, api_description: TBeautifulCapiRoot):
        self.namespaces = api_description.namespaces
        self.namespace_stack = []

    def add_function(self, enum: TEnumeration, parent_class: TClass = None):
        if enum.implementation_type_filled:
            func = TFunction()
            class_name = parent_class.implementation_class_name.split('::')[-1] if parent_class else ''
            func.name = class_name + 'GetImplementationValueFor' + enum.name
            func.return_type = enum.underlying_type
            argument = TArgument()
            argument.name = 'index'
            argument.type_name = 'size_t'
            if enum.implementation_header_filled:
                func.implementation_header_filled = True
                func.implementation_header = enum.implementation_header
            func.arguments.append(argument)
            implementation_code = TImplementationCode()
            implementation_code.all_items.append('switch(index)')
            implementation_code.all_items.append('{{')
            name_array = [class_name] if class_name else [ns.name for ns in self.namespace_stack]
            for index, item in enumerate(enum.items):
                item_name = item.implementation_name if item.implementation_name else item.name
                full_name = '::'.join(enum.implementation_type.split('::')[:-1] + [item_name])
                implementation_code.all_items.append(' ' * 4 + 'case {index}:'.format(index=index))
                implementation_code.all_items.append(' ' * 8 + 'return static_cast<{0}>({1});'.format(
                    enum.underlying_type, full_name))
            implementation_code.all_items.append(' ' * 4 + 'default:')
            implementation_code.all_items.append(' ' * 8 + 'assert (false);')
            enum_name = '::'.join(name_array + [enum.name])
            implementation_code.all_items.append(
                ' ' * 8 + 'throw std::runtime_error("{name}: index out of range");'.format(name=enum_name))
            implementation_code.all_items.append('}}')
            implementation_code.all_items.append('return @ret@0;')
            func.implementation_codes = [implementation_code]
            self.namespace_stack[len(self.namespace_stack)-1].functions.append(func)

    def process_namespace(self, namespace: TNamespace):
        self.namespace_stack.append(namespace)
        for nested_ns in namespace.namespaces:
            self.process_namespace(nested_ns)
        for class_ in namespace.classes:
            for enum in class_.enumerations:
                self.add_function(enum, class_)
        for enum in namespace.enumerations:
            self.add_function(enum)
        self.namespace_stack.pop()

    def process(self):
        for cur_namespace in self.namespaces:
            self.process_namespace(cur_namespace)


def process_enum_impl_functions(api_description: TBeautifulCapiRoot):
        processor = EnumProcessor(api_description)
        processor.process()
