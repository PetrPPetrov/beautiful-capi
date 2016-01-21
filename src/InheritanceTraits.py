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
import FileGenerator


class InheritanceBase(object):
    def __init__(self, interface, capi_generator):
        self.interface = interface
        self.capi_generator = capi_generator

    def put_line(self, line, eol='\n'):
        self.capi_generator.output_header.put_line(line, eol)

    def indent(self):
        return FileGenerator.Indent(self.capi_generator.output_header)


class RequiresCastToBase(InheritanceBase):
    def __init__(self, interface, capi_generator):
        super().__init__(interface, capi_generator)

    def generate_pointer_declaration(self):
        self.capi_generator.output_header.put_line('void* mObject;')

    def generate_set_object(self):
        self.put_line('SetObject(void* raw_pointer)')
        self.put_line('{')
        with self.indent():
            self.put_line('mObject = raw_pointer;')
            if self.interface.m_base:
                self.put_line('{base_class}::SetObject({cast_to_base}(mObject));'.format(
                    base_class=self.interface.m_base,
                    cast_to_base=self.capi_generator.get_namespace_id().lower() + '_cast_to_base'))
        self.put_line('}')

    def generate_constructor(self, constructor):
        self.capi_generator.cur_namespace_path.append(constructor.m_name)
        self.put_line('{class_name}({arguments_list})'.format(
            class_name=self.interface.m_name,
            arguments_list=Helpers.get_arguments_list_for_declaration(constructor.m_arguments)))
        self.put_line('{')
        with self.indent():
            self.put_line('SetObject({constructor_c_function}({arguments_list}));'.format(
                constructor_c_function=self.capi_generator.get_namespace_id().lower(),
                arguments_list=Helpers.get_arguments_list_for_constructor_call(constructor.m_arguments)))
        self.put_line('}')
        self.capi_generator.cur_namespace_path.pop()

    def get_object(self):
        return 'mObject'


class SimpleCase(InheritanceBase):
    def __init__(self, interface, capi_generator):
        super().__init__(interface, capi_generator)

    def generate_pointer_declaration(self):
        if not self.interface.m_base:
            self.capi_generator.output_header.put_line('void* mObject;')

    def generate_set_object(self):
        self.put_line('SetObject(void* raw_pointer)')
        self.put_line('{')
        with self.indent():
            if self.interface.m_base:
                self.put_line('{base_class}::SetObject(raw_pointer);')
            else:
                self.put_line('mObject = raw_pointer;')
        self.put_line('}')

    def generate_constructor(self, constructor):
        self.capi_generator.cur_namespace_path.append(constructor.m_name)
        self.put_line('{class_name}({arguments_list})'.format(
            class_name=self.interface.m_name,
            arguments_list=Helpers.get_arguments_list_for_declaration(constructor.m_arguments)))
        self.put_line('{')
        with self.indent():
            self.put_line('SetObject({constructor_c_function}({arguments_list}));'.format(
                constructor_c_function=self.capi_generator.get_namespace_id().lower(),
                arguments_list=Helpers.get_arguments_list_for_constructor_call(constructor.m_arguments)))
        self.put_line('}')
        self.capi_generator.cur_namespace_path.pop()

    def get_object(self):
        return 'mObject'


def create_inheritance_traits(interface, capi_generator):
    if interface.m_requires_cast_to_base:
        return RequiresCastToBase(interface, capi_generator)
    else:
        return SimpleCase(interface, capi_generator)
