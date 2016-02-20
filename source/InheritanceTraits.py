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

import Helpers
from Constants import Constants
from TraitsBase import TraitsBase


class InheritanceTraitsBase(TraitsBase):
    def __init__(self, interface, capi_generator):
        super().__init__(interface, capi_generator)

    def generate_constructor(self, constructor):
        self.capi_generator.cur_namespace_path.append(constructor.m_name)
        self.put_line('{class_name}({arguments_list})'.format(
            class_name=self.interface.m_name,
            arguments_list=Helpers.get_arguments_list_for_declaration(constructor.m_arguments)
        ))
        with self.indent_scope():
            self.put_line('SetObject({constructor_c_function}({arguments_list}));'.format(
                constructor_c_function=self.capi_generator.get_namespace_id().lower(),
                arguments_list=Helpers.get_arguments_list_for_constructor_call(constructor.m_arguments)
            ))
        c_function_declaration = 'void* {constructor_c_function}({arguments_list})'.format(
            constructor_c_function=self.capi_generator.get_namespace_id().lower(),
            arguments_list=Helpers.get_arguments_list_for_declaration(constructor.m_arguments)
        )
        self.capi_generator.loader_traits.add_c_function_declaration(c_function_declaration)
        with self.indent_scope_source():
            self.put_source_line('return new {0}({1});'.format(
                self.interface.m_implementation_class_name,
                ', '.join(self.capi_generator.get_unwrapped_arguments(constructor.m_arguments))
            ))
        self.put_source_line('')
        self.capi_generator.cur_namespace_path.pop()


class RequiresCastToBase(InheritanceTraitsBase):
    def __init__(self, interface, capi_generator):
        super().__init__(interface, capi_generator)

    def generate_pointer_declaration(self):
        self.capi_generator.output_header.put_line('void* {object_var};'.format(object_var=Constants.object_var))

    def generate_set_object(self):
        self.put_line('void SetObject(void* object_pointer)')
        with self.indent_scope():
            self.put_line('{object_var} = object_pointer;'.format(object_var=Constants.object_var))
            if self.interface.m_base:
                self.put_line('{base_class}::SetObject({cast_to_base}({object_var}));'.format(
                    base_class=self.interface.m_base,
                    cast_to_base=self.capi_generator.get_namespace_id().lower() + Constants.cast_to_base_suffix,
                    object_var=Constants.object_var
                ))
                c_function_declaration = '{cast_to_base}(void* object_pointer)'.format(
                    cast_to_base=self.capi_generator.get_namespace_id().lower() + Constants.cast_to_base_suffix)
                self.capi_generator.loader_traits.add_c_function_declaration(c_function_declaration)
                with self.indent_scope_source():
                    self.put_source_line('return static_cast<{0}*>(static_cast<{1}*>(object_pointer))'.format(
                        self.interface.m_base, self.interface.m_implementation_class_name
                    ))
                self.put_source_line('')


class SimpleCase(InheritanceTraitsBase):
    def __init__(self, interface, capi_generator):
        super().__init__(interface, capi_generator)

    def generate_pointer_declaration(self):
        if not self.interface.m_base:
            self.capi_generator.output_header.put_line('void* {object_var};'.format(object_var=Constants.object_var))

    def generate_set_object(self):
        self.put_line('void SetObject(void* raw_pointer)')
        with self.indent_scope():
            if self.interface.m_base:
                self.put_line('{base_class}::SetObject(raw_pointer);')
            else:
                self.put_line('{object_var} = raw_pointer;'.format(object_var=Constants.object_var))


def create_inheritance_traits(interface, capi_generator):
    if interface.m_requires_cast_to_base:
        return RequiresCastToBase(interface, capi_generator)
    else:
        return SimpleCase(interface, capi_generator)
