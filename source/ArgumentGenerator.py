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


from FileGenerator import FileGenerator
from FileCache import FileCache


class ClassTypeGenerator(object):
    def __init__(self, class_argument_generator):
        self.class_argument_generator = class_argument_generator

    def wrap_argument_declaration(self) -> str:
        return 'const {type_name}&'.format(type_name=self.class_argument_generator.full_wrap_name)

    def wrap_return_type(self) -> str:
        return self.class_argument_generator.full_wrap_name

    @staticmethod
    def wrap_2_c(name: str) -> str:
        return '{name}.get_raw_pointer()'.format(name=name)

    @staticmethod
    def c_argument_declaration() -> str:
        return 'void*'

    def c_2_wrap_var(self, result_var: str, expression: str) -> ([str], str):
        if result_var:
            return ['{type_name}{result_var}({expression}, true);'.format(
                type_name=self.wrap_return_type(),
                result_var=' ' + result_var if result_var else '',
                expression=expression)], result_var
        else:
            return [], '{type_name}({expression}, true)'.format(
                type_name=self.wrap_return_type(), expression=expression)

    def c_2_implementation(self, name: str) -> str:
        return 'static_cast<{implementation_class_name}*>({name})'.format(
            implementation_class_name=self.class_argument_generator.class_object.implementation_class_name,
            name=name
        )

    def implementation_2_c_var(self, result_var: str, expression: str) -> ([str], str):
        return self.class_argument_generator.implementation_result_instructions(result_var, expression)

    @staticmethod
    def generate_c_default_return_value(out: FileGenerator):
        out.put_line('return static_cast<void*>(0);')

    def include_dependent_declaration_headers(self, file_generator: FileGenerator, file_cache: FileCache):
        file_generator.include_user_header(
            file_cache.class_header_decl(self.class_argument_generator.full_name_array))

    def include_dependent_definition_headers(self, file_generator: FileGenerator, file_cache: FileCache):
        file_generator.include_user_header(
            file_cache.class_header(self.class_argument_generator.full_name_array))


# class EnumTypeGenerator(object):
#     def __init__(self, enum_argument_generator):
#         pass


class BuiltinTypeGenerator(object):
    def __init__(self, type_name: str):
        self.type_name = type_name

    @property
    def is_void(self):
        return True if self.type_name == 'void' or not self.type_name else False

    def wrap_argument_declaration(self) -> str:
        return '{type_name}'.format(type_name='void' if self.is_void else self.type_name)

    def wrap_return_type(self) -> str:
        return self.wrap_argument_declaration()

    @staticmethod
    def wrap_2_c(name: str) -> str:
        return name

    def c_argument_declaration(self) -> str:
        return self.wrap_argument_declaration()

    def c_2_wrap_var(self, result_var: str, expression: str) -> ([str], str):
        if not self.is_void:
            if result_var:
                return ['{type_name} {result_var}({expression});'.format(
                    type_name=self.wrap_return_type(),
                    result_var=result_var,
                    expression=expression)], result_var
            else:
                return [], expression
        else:
            return [expression + ';'], ''

    @staticmethod
    def c_2_implementation(name: str) -> str:
        return name

    def implementation_2_c_var(self, result_var: str, expression: str) -> ([str], str):
        if not self.is_void:
            if result_var:
                return ['{type_name} {result_var}({expression});'.format(
                    type_name=self.type_name,
                    result_var=result_var,
                    expression=expression)], result_var
            else:
                return [], expression
        else:
            return [expression + ';'], ''

    def generate_c_default_return_value(self, out: FileGenerator):
        if not self.is_void:
            out.put_line('return static_cast<{type_name}>(0);'.format(type_name=self.type_name))

    def include_dependent_declaration_headers(self, file_generator: FileGenerator, file_cache: FileCache):
        pass

    def include_dependent_definition_headers(self, file_generator: FileGenerator, file_cache: FileCache):
        pass


class ArgumentGenerator(object):
    def __init__(self, type_generator: ClassTypeGenerator or BuiltinTypeGenerator, name: str):
        self.type_generator = type_generator
        self.name = name

    def wrap_argument_declaration(self) -> str:
        return self.type_generator.wrap_argument_declaration() + ' ' + self.name

    def wrap_2_c(self) -> str:
        return self.type_generator.wrap_2_c(self.name)

    def c_argument_declaration(self) -> str:
        return self.type_generator.c_argument_declaration() + ' ' + self.name

    def c_2_implementation(self) -> str:
        return self.type_generator.c_2_implementation(self.name)

    def include_dependent_declaration_headers(self, file_generator: FileGenerator, file_cache: FileCache):
        self.type_generator.include_dependent_declaration_headers(file_generator, file_cache)

    def include_dependent_definition_headers(self, file_generator: FileGenerator, file_cache: FileCache):
        self.type_generator.include_dependent_definition_headers(file_generator, file_cache)


class ThisArgumentGenerator(object):
    def __init__(self, class_argument_generator):
        self.type_generator = ClassTypeGenerator(class_argument_generator)

    @staticmethod
    def wrap_2_c() -> str:
        return 'this->get_raw_pointer()'

    @staticmethod
    def c_argument_declaration() -> str:
        return 'void* object_pointer'

    def c_2_implementation(self) -> str:
        return self.type_generator.c_2_implementation('object_pointer')

    def include_dependent_declaration_headers(self, file_generator: FileGenerator, file_cache: FileCache):
        pass

    def include_dependent_definition_headers(self, file_generator: FileGenerator, file_cache: FileCache):
        pass
