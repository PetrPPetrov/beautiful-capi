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


class BuiltinTypeGenerator(object):
    def __init__(self, type_name: str):
        self.type_name = type_name
        self.c_2_impl = ''

    @property
    def is_void(self):
        return True if self.type_name == 'void' or not self.type_name else False

    def wrap_argument_declaration(self) -> str:
        return '{type_name}'.format(type_name='void' if self.is_void else self.type_name)

    def wrap_return_type(self) -> str:
        return self.wrap_argument_declaration()

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

    def wrap_2_c_var(self, result_var: str, expression: str) -> ([str], str):
        return self.implementation_2_c_var(result_var, expression)

    def c_2_implementation(self, expression: str) -> str:
        cur_c_2_impl = self.c_2_impl
        if not cur_c_2_impl:
            cur_c_2_impl = '{expression}'
        return cur_c_2_impl.format(
            implementation_type=self.snippet_implementation_declaration(),
            expression=expression)

    def c_2_implementation_var(self, result_var: str, expression: str) -> ([str], str):
        expression = self.c_2_implementation(expression)
        if not self.is_void:
            if result_var:
                return ['{impl_name} {result_var}({expression});'.format(
                    impl_name=self.snippet_implementation_declaration(),
                    result_var=result_var,
                    expression=expression)], result_var
            else:
                return [], expression
        else:
            return [expression + ';'], ''

    def snippet_implementation_declaration(self) -> str:
        return 'void' if self.is_void else self.type_name

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
