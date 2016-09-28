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
    def __generate_cast_to_base(class_generator):
        body = FileGenerator(None)
        with IndentScope(body):
            body.put_line('return static_cast<{base_type}*>(static_cast<{this_type}*>(object_pointer));'.format(
                base_type=class_generator.base_class_generator.class_object.implementation_class_name,
                this_type=class_generator.class_object.implementation_class_name
            ))
        class_generator.capi_generator.add_c_function(
            class_generator.full_name_array,
            'void*',
            class_generator.cast_to_base,
            'void* object_pointer',
            body)

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
                RequiresCastToBase.__generate_cast_to_base(class_generator)
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
                out.put_line('{base_class}::SetObject(raw_pointer);'.format(
                    base_class=class_generator.base_class_generator.full_wrap_name))
            else:
                out.put_line('mObject = raw_pointer;')


def create_inheritance_traits(requires_cast_to_base: bool):
    if requires_cast_to_base:
        return RequiresCastToBase()
    else:
        return SimpleCase()
