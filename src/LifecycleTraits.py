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

import FileGenerator
import Parser


class CopySemantic(object):
    def __init__(self, interface, capi_generator):
        self.interface = interface
        self.capi_generator = capi_generator

    def generate_destructor(self):
        self.capi_generator.output_header.put_line('~{0}()'.format(self.interface.m_name))
        self.capi_generator.output_header.put_line('{')
        self.capi_generator.output_header.put_line('}')


class MoveSemantic(object):
    def __init__(self, interface, capi_generator):
        self.interface = interface
        self.capi_generator = capi_generator

    def generate_destructor(self):
        self.capi_generator.output_header.put_line('~{0}()'.format(self.interface.m_name))
        self.capi_generator.output_header.put_line('{')
        self.capi_generator.output_header.put_line('}')


class RefCountedSemantic(object):
    def __init__(self, interface, capi_generator):
        self.interface = interface
        self.capi_generator = capi_generator

    def generate_destructor(self):
        self.capi_generator.output_header.put_line('~{0}()'.format(self.interface.m_name))
        self.capi_generator.output_header.put_line('{')
        with FileGenerator.Indent(self.capi_generator.output_header):
            self.capi_generator.output_header.put_line('if ({0})'.format(
                self.capi_generator.inheritance_traits.get_pointer()
            ))
            self.capi_generator.output_header.put_line('{')
            with FileGenerator.Indent(self.capi_generator.output_header):
                self.capi_generator.output_header.put_line('{0}({1});'.format(
                    self.capi_generator.get_namespace_id().lower() + '_release',
                    self.capi_generator.inheritance_traits.get_pointer()
                ))
            self.capi_generator.output_header.put_line('}')
        self.capi_generator.output_header.put_line('}')


str_to_lifecycle = {
    Parser.TLifecycle.copy_semantic: CopySemantic,
    Parser.TLifecycle.move_semantic: MoveSemantic,
    Parser.TLifecycle.reference_counted: RefCountedSemantic
}


def create_lifecycle_traits(interface, capi_generator):
    if interface.m_lifecycle in str_to_lifecycle:
        return str_to_lifecycle[interface.m_lifecycle](interface, capi_generator)
    raise ValueError
