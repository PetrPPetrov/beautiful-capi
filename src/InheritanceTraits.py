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


class RequiresCastToBase(object):
    def __init__(self, interface, capi_generator):
        self.interface = interface
        self.capi_generator = capi_generator

    def generate_pointer_declaration(self):
        self.capi_generator.output_header.put_line('void* m_raw_pointer;')

    def generate_protected_constructor(self):
        self.capi_generator.output_header.put_line('{0}(void* raw_pointer) : m_raw_pointer(raw_pointer)'.format(
            self.interface.m_name), '')
        if self.interface.m_base:
            self.capi_generator.output_header.put_line(', {base_class}({cast_to_base}(raw_pointer))'.format(
                base_class=self.interface.m_base,
                cast_to_base=self.capi_generator.get_namespace_id().lower() + '_cast_to_base'
            ))
        else:
            self.capi_generator.output_header.put_line('')
        self.capi_generator.output_header.put_line('{')
        self.capi_generator.output_header.put_line('}')

    def get_pointer(self):
        return 'm_raw_pointer'


class SimpleCase(object):
    def __init__(self, interface, capi_generator):
        self.interface = interface
        self.capi_generator = capi_generator
        self.m_base = interface.m_base if interface.m_base else 'm_raw_pointer'

    def generate_pointer_declaration(self):
        if not self.interface.m_base:
            self.capi_generator.output_header.put_line('void* m_raw_pointer;')

    def generate_protected_constructor(self):
        self.capi_generator.output_header.put_line('{0}(void* raw_pointer) : {1}(raw_pointer)'.format(
            self.interface.m_name, self.m_base))
        self.capi_generator.output_header.put_line('{')
        self.capi_generator.output_header.put_line('}')

    def get_pointer(self):
        return 'm_raw_pointer'


def create_inheritance_traits(interface, capi_generator):
    if interface.m_requires_cast_to_base:
        return RequiresCastToBase(interface, capi_generator)
    else:
        return SimpleCase(interface, capi_generator)
