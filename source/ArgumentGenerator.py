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
from NamespaceGenerator import NamespaceGenerator
from Parser import TArgument
from Helpers import bool_to_str


class ClassTypeGenerator(object):
    def __init__(self, class_argument_generator):
        self.class_argument_generator = class_argument_generator
        self.copy_or_add_ref_when_c_2_wrap = False

    def wrap_argument_declaration(self) -> str:
        return 'const {type_name}&'.format(type_name=self.class_argument_generator.full_wrap_name)

    def wrap_return_type(self) -> str:
        return self.class_argument_generator.full_wrap_name

    def wrap_2_c(self, name: str) -> str:
        return '{name}.{get_raw_pointer_method}()'.format(
            name=name, get_raw_pointer_method=self.class_argument_generator.params.get_raw_pointer_method_name)

    @staticmethod
    def c_argument_declaration() -> str:
        return 'void*'

    def c_2_wrap_var(self, result_var: str, expression: str) -> ([str], str):
        internal_expression = '{type_name}::force_creating_from_raw_pointer, {expression}, {copy_or_add_ref}'.format(
            type_name=self.wrap_return_type(),
            expression=expression,
            copy_or_add_ref=bool_to_str(self.copy_or_add_ref_when_c_2_wrap)
        )
        if result_var:
            return ['{type_name} {result_var}({internal_expression});'.format(
                type_name=self.wrap_return_type(),
                result_var=result_var,
                internal_expression=internal_expression
            )], result_var
        else:
            return [], '{type_name}({internal_expression})'.format(
                type_name=self.wrap_return_type(), internal_expression=internal_expression)

    def wrap_2_c_var(self, result_var: str, expression: str) -> ([str], str):
        internal_expression = '{expression}.{get_raw_pointer_method}()'.format(
            expression=expression,
            get_raw_pointer_method=self.class_argument_generator.params.get_get_raw_pointer_method)
        if result_var:
            return ['void* {result_var}({internal_expression});'.format(
                result_var=result_var,
                internal_expression=internal_expression
            )], result_var
        else:
            return [], internal_expression

    def c_2_implementation(self, name: str) -> str:
        return self.class_argument_generator.lifecycle_traits.c_2_impl_value(
            'static_cast<{implementation_class_name}*>({name})'.format(
                implementation_class_name=self.class_argument_generator.class_object.implementation_class_name,
                name=name
            ))

    def c_2_implementation_to_pointer(self, name: str) -> str:
        return self.class_argument_generator.lifecycle_traits.c_2_impl_pointer(
            'static_cast<{implementation_class_name}*>({name})'.format(
                implementation_class_name=self.class_argument_generator.class_object.implementation_class_name,
                name=name
            ))

    def c_2_implementation_var(self, result_var: str, expression: str) -> ([str], str):
        expression = self.class_argument_generator.lifecycle_traits.c_2_impl_value().format(expression=expression)
        if result_var:
            return ['{impl_name} {result_var}({expression});'.format(
                impl_name=self.snippet_implementation_declaration(),
                result_var=result_var,
                expression=expression)], result_var
        else:
            return [], '{impl_name}({expression})'.format(
                impl_name=self.snippet_implementation_declaration(),
                expression=expression)

    def snippet_implementation_declaration(self) -> str:
        return self.class_argument_generator.snippet_implementation_declaration

    def implementation_2_c_var(self, result_var: str, expression: str) -> ([str], str):
        expression = self.class_argument_generator.lifecycle_traits.implementation_2_c.format(
            implementation_expression=expression)
        return self.class_argument_generator.implementation_result_instructions(result_var, expression)

    @staticmethod
    def generate_c_default_return_value(out: FileGenerator):
        out.put_line('return static_cast<void*>(0);')

    def include_dependent_declaration_headers(self, file_generator: FileGenerator, file_cache: FileCache):
        file_generator.include_user_header(
            file_cache.fwd_header(self.class_argument_generator.full_name_array))

    def include_dependent_definition_headers(self, file_generator: FileGenerator, file_cache: FileCache):
        file_generator.include_user_header(
            file_cache.class_header(self.class_argument_generator.full_name_array))


class EnumTypeGenerator(object):
    def __init__(self, enum_argument_generator):
        self.enum_argument_generator = enum_argument_generator

    def wrap_argument_declaration(self) -> str:
        return self.enum_argument_generator.full_wrap_name

    def wrap_return_type(self) -> str:
        return self.enum_argument_generator.full_wrap_name

    def wrap_2_c(self, name: str) -> str:
        return 'static_cast<{c_type}>({name})'.format(c_type=self.c_argument_declaration(), name=name)

    def c_argument_declaration(self) -> str:
        return self.enum_argument_generator.enum_object.underlying_type

    def c_2_wrap_var(self, result_var: str, expression: str) -> ([str], str):
        if result_var:
            return ['{type_name} {result_var}(static_cast<{type_name}>({expression}));'.format(
                type_name=self.wrap_return_type(),
                result_var=result_var,
                expression=expression
            )], result_var
        else:
            return [], '{type_name}(static_cast<{type_name}>({expression}))'.format(
                type_name=self.wrap_return_type(), expression=expression)

    def wrap_2_c_var(self, result_var: str, expression: str) -> ([str], str):
        return self.implementation_2_c_var(result_var, expression)

    def c_2_implementation(self, name: str) -> str:
        return 'static_cast<{implementation_name}>({name})'.format(
            implementation_name=self.enum_argument_generator.implementation_name,
            name=name
        )

    def c_2_implementation_var(self, result_var: str, expression: str) -> ([str], str):
        if result_var:
            return ['{impl_name} {result_var}(static_cast<{impl_name}>({expression}));'.format(
                impl_name=self.snippet_implementation_declaration(),
                result_var=result_var,
                expression=expression)], result_var
        else:
            return [], 'static_cast<{impl_name}>({expression})'.format(
                impl_name=self.snippet_implementation_declaration(),
                expression=expression)

    def snippet_implementation_declaration(self) -> str:
        return self.enum_argument_generator.implementation_name

    def implementation_2_c_var(self, result_var: str, expression: str) -> ([str], str):
        casting_expression = 'static_cast<{c_type}>({expression})'.format(
            c_type=self.c_argument_declaration(), expression=expression
        )
        if result_var:
            return ['{type_name} {result_var}({expression});'.format(
                type_name=self.c_argument_declaration(),
                result_var=result_var,
                expression=casting_expression)], result_var
        else:
            return [], casting_expression

    def generate_c_default_return_value(self, out: FileGenerator):
        out.put_line('return static_cast<{c_type}>(0);'.format(c_type=self.c_argument_declaration()))

    def include_dependent_declaration_headers(self, file_generator: FileGenerator, file_cache: FileCache):
        parent_generator = self.enum_argument_generator.parent_generator
        if type(parent_generator) is NamespaceGenerator:
            header_to_include = file_cache.enums_header(parent_generator.full_name_array)
        else:
            header_to_include = file_cache.class_header_decl(parent_generator.full_name_array)
        file_generator.include_user_header(header_to_include)

    def include_dependent_definition_headers(self, file_generator: FileGenerator, file_cache: FileCache):
        pass


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

    def wrap_2_c_var(self, result_var: str, expression: str) -> ([str], str):
        return self.implementation_2_c_var(result_var, expression)

    @staticmethod
    def c_2_implementation(name: str) -> str:
        return name

    def c_2_implementation_var(self, result_var: str, expression: str) -> ([str], str):
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


class ArgumentGenerator(object):
    def __init__(self, type_generator: ClassTypeGenerator or EnumTypeGenerator or BuiltinTypeGenerator, name: str):
        self.type_generator = type_generator
        self.argument_object = None
        self.name = name

    def wrap_argument_declaration(self) -> str:
        return self.type_generator.wrap_argument_declaration() + ' ' + self.name

    def wrap_2_c(self) -> str:
        return self.type_generator.wrap_2_c(self.name)

    def c_argument_declaration(self) -> str:
        return self.type_generator.c_argument_declaration() + ' ' + self.name

    def c_2_wrap(self) -> str:
        return self.type_generator.c_2_wrap_var('', self.name)[1]

    def c_2_implementation(self) -> str:
        return self.type_generator.c_2_implementation(self.name)

    def c_2_implementation_to_pointer(self) -> str:
        return self.type_generator.c_2_implementation_to_pointer(self.name)

    def snippet_implementation_declaration(self) -> str:
        return self.type_generator.snippet_implementation_declaration() + ' ' + self.name

    def implementation_2_c(self) -> str:
        return self.type_generator.implementation_2_c_var('', self.name)[1]

    def include_dependent_declaration_headers(self, file_generator: FileGenerator, file_cache: FileCache):
        self.type_generator.include_dependent_declaration_headers(file_generator, file_cache)

    def include_dependent_definition_headers(self, file_generator: FileGenerator, file_cache: FileCache):
        self.type_generator.include_dependent_definition_headers(file_generator, file_cache)


class ThisArgumentGenerator(object):
    def __init__(self, class_argument_generator):
        self.type_generator = ClassTypeGenerator(class_argument_generator)

    def wrap_2_c(self) -> str:
        return '{get_raw_pointer_method}()'.format(
            get_raw_pointer_method=self.type_generator.class_argument_generator.params.get_raw_pointer_method_name)

    @staticmethod
    def c_argument_declaration() -> str:
        return 'void* object_pointer'

    def c_2_implementation(self) -> str:
        return self.type_generator.c_2_implementation_to_pointer('object_pointer')

    def implementation_2_c(self) -> str:
        return self.type_generator.implementation_2_c_var('', 'mObject')[1]

    def include_dependent_declaration_headers(self, file_generator: FileGenerator, file_cache: FileCache):
        pass

    def include_dependent_definition_headers(self, file_generator: FileGenerator, file_cache: FileCache):
        pass
