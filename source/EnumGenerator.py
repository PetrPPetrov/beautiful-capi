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


from Parser import TEnumeration, TEnumerationItem
from FileGenerator import FileGenerator, IndentScope


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
        return '::'.join([self.parent_generator.implementation_name, self.name])

    @staticmethod
    def __get_enum_item_definition(enum_item: TEnumerationItem) -> str:
        if enum_item.value_filled:
            return '{name} = {value}'.format(name=enum_item.name, value=enum_item.value)
        else:
            return '{name}'.format(name=enum_item.name)

    def generate_enum_definition(self, out: FileGenerator):
        out.put_line('enum {name}'.format(name=self.name))
        with IndentScope(out, '};'):
            items_definitions = [self.__get_enum_item_definition(enum_item) for enum_item in self.enum_object.items]
            items_definitions_with_comma = [item + ',' for item in items_definitions[:-1]]
            if items_definitions:
                items_definitions_with_comma.append(items_definitions[-1])
            for item_definition in items_definitions_with_comma:
                out.put_line(item_definition)
