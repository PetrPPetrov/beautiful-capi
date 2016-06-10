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
    def __init__(self, cur_class, capi_generator):
        super().__init__(cur_class, capi_generator)

    def generate_constructor(self, constructor):
        self.capi_generator.cur_namespace_path.append(constructor.m_name)
        self.put_line('{class_name}({arguments_list})'.format(
            class_name=self.cur_class.m_name + self.capi_generator.lifecycle_traits.get_suffix(),
            arguments_list=', '.join(self.capi_generator.get_wrapped_argument_pairs(constructor.m_arguments))
        ))
        with self.indent_scope():
            self.put_line('SetObject({constructor_c_function}({arguments_list}));'.format(
                constructor_c_function=self.capi_generator.get_namespace_id().lower(),
                arguments_list=', '.join(
                    self.capi_generator.get_c_from_wrapped_arguments_for_function(constructor.m_arguments)
                )
            ))
        c_function_declaration = 'void* {constructor_c_function}({arguments_list})'.format(
            constructor_c_function=self.capi_generator.get_namespace_id().lower(),
            arguments_list=', '.join(self.capi_generator.get_wrapped_argument_pairs(constructor.m_arguments))
        )
        self.capi_generator.loader_traits.add_c_function_declaration(c_function_declaration)
        with self.indent_scope_source():
            self.put_source_line('return new {0}({1});'.format(
                self.cur_class.m_implementation_class_name,
                ', '.join(self.capi_generator.get_c_to_original_arguments(constructor.m_arguments))
            ))
        self.put_source_line('')
        self.capi_generator.cur_namespace_path.pop()


class RequiresCastToBase(InheritanceTraitsBase):
    def __init__(self, cur_class, capi_generator):
        super().__init__(cur_class, capi_generator)

    def generate_pointer_declaration(self):
        self.capi_generator.output_header.put_line('void* {object_var};'.format(object_var=Constants.object_var))

    def generate_set_object(self):
        self.put_line('void SetObject(void* object_pointer)')
        with self.indent_scope():
            self.put_line('{object_var} = object_pointer;'.format(object_var=Constants.object_var))
            if self.cur_class.m_base:
                self.put_line('{base_class}::SetObject({cast_to_base}({object_var}));'.format(
                    base_class=self.cur_class.m_base,
                    cast_to_base=self.capi_generator.get_namespace_id().lower() + Constants.cast_to_base_suffix,
                    object_var=Constants.object_var
                ))
                c_function_declaration = '{cast_to_base}(void* object_pointer)'.format(
                    cast_to_base=self.capi_generator.get_namespace_id().lower() + Constants.cast_to_base_suffix)
                self.capi_generator.loader_traits.add_c_function_declaration(c_function_declaration)
                with self.indent_scope_source():
                    self.put_source_line('return static_cast<{0}*>(static_cast<{1}*>(object_pointer))'.format(
                        self.cur_class.m_base, self.cur_class.m_implementation_class_name
                    ))
                self.put_source_line('')


class SimpleCase(InheritanceTraitsBase):
    def __init__(self, cur_class, capi_generator):
        super().__init__(cur_class, capi_generator)

    def generate_pointer_declaration(self):
        if not self.cur_class.m_base:
            self.capi_generator.output_header.put_line('void* {object_var};'.format(object_var=Constants.object_var))

    def generate_set_object(self):
        self.put_line('void SetObject(void* raw_pointer)')
        with self.indent_scope():
            if self.cur_class.m_base:
                self.put_line('{base_class}::SetObject(raw_pointer);')
            else:
                self.put_line('{object_var} = raw_pointer;'.format(object_var=Constants.object_var))


def create_inheritance_traits(cur_class, capi_generator):
    if cur_class.m_requires_cast_to_base:
        return RequiresCastToBase(cur_class, capi_generator)
    else:
        return SimpleCase(cur_class, capi_generator)


class CreateInheritanceTraits(object):
    def __init__(self, cur_class, capi_generator):
        self.cur_class = cur_class
        self.capi_generator = capi_generator

    def __enter__(self):
        self.capi_generator.inheritance_traits = create_inheritance_traits(self.cur_class, self.capi_generator)

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self.capi_generator.inheritance_traits
        self.capi_generator.inheritance_traits = None
