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
from LifecycleTraits import CopySemantic, RefCountedSemantic
from Parser import TC2ImplMode
from NamespaceGenerator import NamespaceGenerator
from BuiltinTypeGenerator import BuiltinTypeGenerator, BaseTypeGenerator
from Helpers import bool_to_str, include_headers


class MappedTypeGenerator(BaseTypeGenerator):
    def __init__(self, mapped_type_object, parent_generator):
        self.mapped_type_object = mapped_type_object
        self.name = self.mapped_type_object.name
        self.full_name = parent_generator.full_name + '::' + self.mapped_type_object.name
        self.c_2_impl = ''

    def format(self, casting_expression: str, expression_to_cast: str, result_var: str, type_name: str) -> ([str], str):
        result_expression = casting_expression.format(
            expression=expression_to_cast,
            c_type=self.mapped_type_object.c_type,
            implementation_type=self.mapped_type_object.implementation_type,
            wrap_type=self.mapped_type_object.wrap_type,
            argument_wrap_type=self.mapped_type_object.argument_wrap_type
        )
        if result_var:
            return ['{type_name} {result_var}({expression});'.format(
                type_name=type_name,
                expression=result_expression,
                result_var=result_var
            )], result_var
        else:
            return [], result_expression

    def wrap_return_type(self) -> str:
        return self.mapped_type_object.wrap_type

    def wrap_argument_declaration(self) -> str:
        return self.mapped_type_object.argument_wrap_type if self.mapped_type_object.argument_wrap_type_filled \
            else self.mapped_type_object.wrap_type

    def c_argument_declaration(self) -> str:
        return self.mapped_type_object.c_type

    def wrap_2_c_var(self, result_var: str, expression: str) -> ([str], str):
        return self.format(self.mapped_type_object.wrap_2_c, expression, result_var, self.mapped_type_object.c_type)

    def c_2_implementation(self, expression: str) -> str:
        return self.c_2_implementation_var('', expression)[1]

    def c_2_implementation_var(self, result_var: str, expression: str) -> ([str], str):
        cur_c_2_impl = self.c_2_impl
        if not cur_c_2_impl:
            cur_c_2_impl = self.mapped_type_object.c_2_impl
        return self.format(cur_c_2_impl, expression, result_var,
                           self.mapped_type_object.implementation_type)

    def snippet_implementation_declaration(self) -> str:
        return self.mapped_type_object.implementation_type

    def implementation_2_c_var(self, result_var: str, expression: str) -> ([str], str):
        return self.format(self.mapped_type_object.impl_2_c, expression, result_var, self.mapped_type_object.c_type)

    def c_2_wrap_var(self, result_var: str, expression: str) -> ([str], str):
        return self.format(self.mapped_type_object.c_2_wrap, expression, result_var, self.mapped_type_object.wrap_type)

    def generate_c_default_return_value(self, out: FileGenerator):
        out.put_line('return static_cast<{c_type}>(0);'.format(c_type=self.c_argument_declaration()))

    def include_dependent_declaration_headers(self, file_generator: FileGenerator, file_cache: FileCache):
        include_headers(file_generator, self.mapped_type_object.include_headers)

    def include_dependent_definition_headers(self, file_generator: FileGenerator, file_cache: FileCache):
        pass


class ClassTypeGenerator(BaseTypeGenerator):
    def __init__(self, class_argument_generator):
        self.class_argument_generator = class_argument_generator
        self.copy_or_add_ref_when_c_2_wrap = False
        self.c_2_impl = ''
        self.impl_2_c = ''
        self.impl_2_c_filled = False

    def wrap_argument_declaration(self) -> str:
        return 'const {type_name}&'.format(type_name=self.class_argument_generator.full_wrap_name)

    def wrap_return_type(self) -> str:
        return self.class_argument_generator.full_wrap_name

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
            get_raw_pointer_method=self.class_argument_generator.get_raw_pointer_method_name)
        if result_var:
            return ['void* {result_var}({internal_expression});'.format(
                result_var=result_var,
                internal_expression=internal_expression
            )], result_var
        else:
            return [], internal_expression

    def c_2_implementation(self, expression: str) -> str:
        cur_c_2_impl = self.c_2_impl
        if not cur_c_2_impl:
            cur_c_2_impl = self.class_argument_generator.lifecycle_traits.c_2_impl_default()
        return cur_c_2_impl.format(
            implementation_type=self.class_argument_generator.class_object.implementation_class_name,
            expression=expression)

    def c_2_implementation_pointer(self, expression: str) -> str:
        self.c_2_impl = RefCountedSemantic.c_2_impl_default()
        return self.c_2_implementation(expression)

    def c_2_implementation_var(self, result_var: str, expression: str) -> ([str], str):
        expression = self.c_2_implementation(expression)
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
        default_cast = self.class_argument_generator.lifecycle_traits.implementation_2_c_default()
        cur_impl_2_c = self.impl_2_c if self.impl_2_c_filled else default_cast
        result_expression = cur_impl_2_c.format(
            expression=expression,
            implementation_type=self.class_argument_generator.class_object.implementation_class_name,
            c_type='void*',
            result_var=result_var
        )
        if result_var:
            return ['void* {result_var}({expression})'. format(
                expression=result_expression,
                result_var=result_var
            )], result_var
        return [], result_expression

    @staticmethod
    def generate_c_default_return_value(out: FileGenerator):
        out.put_line('return static_cast<void*>(0);')

    def include_dependent_declaration_headers(self, file_generator: FileGenerator, file_cache: FileCache):
        file_generator.include_user_header(
            file_cache.fwd_header(self.class_argument_generator.full_name_array))

    def include_dependent_definition_headers(self, file_generator: FileGenerator, file_cache: FileCache):
        file_generator.include_user_header(
            file_cache.class_header(self.class_argument_generator.full_name_array))


class ExternalClassTypeGenerator(ClassTypeGenerator):
    def c_2_implementation(self, expression: str) -> str:
        return '{impl_type}({impl_type}::force_creating_from_raw_pointer, {expression}, true)'.format(
            impl_type=self.class_argument_generator.full_wrap_name,
            expression=expression)

    def snippet_implementation_declaration(self) -> str:
        return self.class_argument_generator.full_wrap_name

    def implementation_2_c_var(self, result_var: str, expression: str) -> ([str], str):
        result_expression = '{full_wrap_name}({expression}).{detach_method_name}()'.format(
            full_wrap_name=self.class_argument_generator.full_wrap_name,
            expression=expression,
            detach_method_name=self.class_argument_generator.parent_namespace.namespace_object.detach_method_name,
            c_type='void*'
        )
        if result_var:
            return ['void* {result_var}({expression})'. format(
                expression=result_expression,
                result_var=result_var
            )], result_var
        return [], result_expression

    def __include_required_header(self, file_generator: FileGenerator, cur_header: str):
        base_namespace = self.class_argument_generator.parent_namespace
        while not cur_header:
            if not base_namespace:
                return
            cur_header = base_namespace.namespace_object.include
            base_namespace = base_namespace.parent_namespace
        file_generator.include_user_header(cur_header)

    def include_dependent_declaration_headers(self, file_generator: FileGenerator, file_cache: FileCache):
        self.__include_required_header(file_generator, self.class_argument_generator.class_object.include_declaration)

    def include_dependent_definition_headers(self, file_generator: FileGenerator, file_cache: FileCache):
        self.__include_required_header(file_generator, self.class_argument_generator.class_object.include_definition)


class EnumTypeGenerator(BaseTypeGenerator):
    def __init__(self, enum_argument_generator):
        self.enum_argument_generator = enum_argument_generator
        self.c_2_impl = ''

    def wrap_argument_declaration(self) -> str:
        return self.enum_argument_generator.full_wrap_name

    def wrap_return_type(self) -> str:
        return self.enum_argument_generator.full_wrap_name

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

    def c_2_implementation(self, expression: str) -> str:
        cur_c_2_impl = self.c_2_impl
        if not cur_c_2_impl:
            cur_c_2_impl = 'static_cast<{implementation_type}>({expression})'
        return cur_c_2_impl.format(
            implementation_type=self.enum_argument_generator.implementation_name,
            expression=expression
        )

    def c_2_implementation_var(self, result_var: str, expression: str) -> ([str], str):
        expression = self.c_2_implementation(expression)
        if result_var:
            return ['{impl_name} {result_var}({expression});'.format(
                impl_name=self.snippet_implementation_declaration(),
                result_var=result_var,
                expression=expression)], result_var
        else:
            return [], expression

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


class ArgumentGenerator(object):
    def __init__(self,
                 type_generator: BaseTypeGenerator,
                 name: str):
        self.type_generator = type_generator
        self.argument_object = None
        self.name = name

    def wrap_argument_declaration(self) -> str:
        return self.type_generator.wrap_argument_declaration() + ' ' + self.name

    def wrap_2_c(self) -> str:
        return self.type_generator.wrap_2_c_var('', self.name)[1]

    def c_argument_declaration(self) -> str:
        return self.type_generator.c_argument_declaration() + ' ' + self.name

    def c_2_wrap(self) -> str:
        return self.type_generator.c_2_wrap_var('', self.name)[1]

    def c_2_implementation(self) -> str:
        self.type_generator.c_2_impl = ''
        if self.argument_object.c_2_impl_filled:
            self.type_generator.c_2_impl = self.argument_object.c_2_impl
        else:
            if self.argument_object.c_2_impl_mode == TC2ImplMode.to_pointer:
                self.type_generator.c_2_impl = RefCountedSemantic.c_2_impl_default()
            elif self.argument_object.c_2_impl_mode == TC2ImplMode.to_value:
                self.type_generator.c_2_impl = CopySemantic.c_2_impl_default()
        return self.type_generator.c_2_implementation(self.name)

    def c_2_implementation_pointer(self) -> str:
        return self.type_generator.c_2_implementation_pointer(self.name)

    def snippet_implementation_declaration(self) -> str:
        return self.type_generator.snippet_implementation_declaration() + ' ' + self.name

    def implementation_2_c(self) -> str:
        return self.type_generator.implementation_2_c_var('', self.name)[1]

    def include_dependent_declaration_headers(self, file_generator: FileGenerator, file_cache: FileCache):
        self.type_generator.include_dependent_declaration_headers(file_generator, file_cache)

    def include_dependent_definition_headers(self, file_generator: FileGenerator, file_cache: FileCache):
        self.type_generator.include_dependent_definition_headers(file_generator, file_cache)
