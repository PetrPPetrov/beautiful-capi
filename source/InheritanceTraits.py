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


from FileGenerator import FileGenerator, IndentScope


class RequiresCastToBase(object):
    @staticmethod
    def generate_pointer_declaration(out: FileGenerator, class_generator):
        out.put_line('void* mObject;')

    @staticmethod
    def generate_set_object_declaration(out: FileGenerator, class_generator):
        out.put_line('inline void SetObject(void* object_pointer);')

    @staticmethod
    def generate_set_object_definition(out: FileGenerator, class_generator):
        out.put_line('inline void {namespace}::SetObject(void* object_pointer)'.format(
            namespace=class_generator.full_wrap_name))
        with IndentScope(out):
            out.put_line('mObject = object_pointer;')
            if class_generator.base_class_generator:
                out.put_line('if (mObject)')
                with IndentScope(out):
                    out.put_line('{base_class}::SetObject({cast_to_base}(mObject));'.format(
                        base_class=class_generator.base_class_generator.full_wrap_name,
                        cast_to_base=class_generator.cast_to_base
                    ))
                out.put_line('else')
                with IndentScope(out):
                    out.put_line('{base_class}::SetObject(0);'.format(
                        base_class=class_generator.base_class_generator.full_wrap_name))

    @staticmethod
    def generate_object_assignment(out: FileGenerator, class_generator, prefix: str, expression: str):
        out.put_line('{prefix}mObject = {expression};'.format(prefix=prefix, expression=expression))

    @staticmethod
    def generate_c_functions(class_generator):
        if class_generator.base_class_generator:
            body = FileGenerator(None)
            with IndentScope(body):
                cast_str = 'return static_cast<{base_type}*>(static_cast<{this_type}*>(object_pointer));'
                if class_generator.class_object.custom_cast_to_base_filled:
                    cast_str = class_generator.class_object.custom_cast_to_base
                body.put_line(cast_str.format(
                    base_type=class_generator.base_class_generator.class_object.implementation_class_name,
                    this_type=class_generator.class_object.implementation_class_name
                ))
            class_generator.capi_generator.add_c_function(
                class_generator.full_name_array[:-1],
                'void*',
                class_generator.cast_to_base,
                'void* object_pointer',
                body)


class SimpleCase(object):
    @staticmethod
    def generate_pointer_declaration(out: FileGenerator, class_generator):
        if not class_generator.base_class_generator:
            RequiresCastToBase().generate_pointer_declaration(out, class_generator)

    @staticmethod
    def generate_set_object_declaration(out: FileGenerator, class_generator):
        out.put_line('inline void SetObject(void* object_pointer);')

    @staticmethod
    def generate_set_object_definition(out: FileGenerator, class_generator):
        out.put_line('inline void {namespace}::SetObject(void* object_pointer)'.format(
            namespace=class_generator.full_wrap_name))
        with IndentScope(out):
            if class_generator.base_class_generator:
                out.put_line('{base_class}::SetObject(object_pointer);'.format(
                    base_class=class_generator.base_class_generator.full_wrap_name))
            else:
                out.put_line('mObject = object_pointer;')

    @staticmethod
    def generate_object_assignment(out: FileGenerator, class_generator, prefix: str, expression: str):
        if not class_generator.base_class_generator:
            RequiresCastToBase().generate_object_assignment(out, class_generator, prefix, expression)

    def generate_c_functions(self, class_generator):
        # We still need to generate _cast_to_base function to use it in the unit tests
        # to verify what casted to base implementation object is equal to the current object's
        # implementation object
        RequiresCastToBase.generate_c_functions(class_generator)


def create_inheritance_traits(requires_cast_to_base: bool):
    if requires_cast_to_base:
        return RequiresCastToBase()
    else:
        return SimpleCase()
