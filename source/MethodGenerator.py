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


import copy
from Parser import TMethod, TFunction, TConstructor
from ParamsParser import TBeautifulCapiParams
from FileGenerator import FileGenerator, IndentScope
from FileCache import FileCache
from ClassGenerator import ClassGenerator
from NamespaceGenerator import NamespaceGenerator
from ArgumentGenerator import ClassTypeGenerator, ThisArgumentGenerator
from CapiGenerator import CapiGenerator
from Helpers import get_c_name


class ConstructorGenerator(object):
    def __init__(self, constructor_object: TConstructor, parent_class_generator: ClassGenerator,
                 params: TBeautifulCapiParams):
        self.constructor_object = constructor_object
        self.parent_class_generator = parent_class_generator
        self.parent_class_as_argument_type = ClassTypeGenerator(parent_class_generator)
        class_as_argument = self.parent_class_as_argument_type
        class_as_argument.copy_or_add_ref_when_c_2_wrap = False
        if self.constructor_object.return_copy_or_add_ref_filled:
            class_as_argument.copy_or_add_ref_when_c_2_wrap = self.constructor_object.return_copy_or_add_ref
        self.argument_generators = []
        self.params = params
        self.exception_traits = None

    @property
    def full_c_name(self) -> str:
        return get_c_name(self.parent_class_generator.full_c_name + '_' + self.constructor_object.name)

    def wrap_declaration(self) -> str:
        arguments = ', '.join(
            [argument_generator.wrap_argument_declaration() for argument_generator in self.argument_generators])
        return 'inline {name}({arguments})'.format(
            name=self.parent_class_generator.wrap_name,
            arguments=arguments
        )

    def generate_wrap_definition(self, out: FileGenerator, capi_generator: CapiGenerator):
        self.exception_traits = capi_generator.get_exception_traits(self.constructor_object.noexcept)
        arguments = ', '.join(
            [argument_generator.wrap_argument_declaration() for argument_generator in self.argument_generators])
        arguments_call = [argument_generator.wrap_2_c() for argument_generator in self.argument_generators]
        out.put_line('inline {full_name}({arguments})'.format(
            full_name=self.parent_class_generator.full_wrap_name,
            arguments=arguments
        ))
        with IndentScope(out):
            return_expression = self.exception_traits.generate_c_call(
                out, self.parent_class_as_argument_type, self.full_c_name, arguments_call)
            out.put_return_cpp_statement(return_expression)

    def generate_c_function(self, capi_generator: CapiGenerator):
        argument_declaration_list = [
                argument_generator.c_argument_declaration() for argument_generator in self.argument_generators
            ]
        self.exception_traits.modify_c_arguments(argument_declaration_list)
        arguments_declaration = ', '.join(argument_declaration_list)
        implementation_arguments = ', '.join(
            [argument_generator.c_2_implementation() for argument_generator in self.argument_generators])
        c_function_body = FileGenerator(None)
        with IndentScope(c_function_body):
            implementation_call = 'return new {impl_class}({arguments});'.format(
                impl_class=self.parent_class_generator.class_object.implementation_class_name,
                arguments=implementation_arguments
            )
            self.exception_traits.generate_implementation_call(
                c_function_body, self.parent_class_as_argument_type, [implementation_call])
        capi_generator.add_c_function(
            self.parent_class_generator.full_name_array,
            self.parent_class_as_argument_type.c_argument_declaration(),
            self.full_c_name,
            arguments_declaration,
            c_function_body
        )

    def include_dependent_declaration_headers(self, file_generator: FileGenerator, file_cache: FileCache):
        for argument_generator in self.argument_generators:
            argument_generator.include_dependent_declaration_headers(file_generator, file_cache)

    def include_dependent_definition_headers(self, file_generator: FileGenerator, file_cache: FileCache):
        self.exception_traits.include_dependent_definition_headers(file_generator, file_cache)
        for argument_generator in self.argument_generators:
            argument_generator.include_dependent_definition_headers(file_generator, file_cache)


class MethodGenerator(object):
    def __init__(self, method_object: TMethod, parent_class_generator: ClassGenerator, params: TBeautifulCapiParams):
        self.method_object = method_object
        self.parent_class_generator = parent_class_generator
        self.argument_generators = []
        self.return_type_generator = None
        self.params = params
        self.exception_traits = None

    @property
    def full_c_name(self) -> str:
        return get_c_name(self.parent_class_generator.full_c_name + '_' + self.method_object.name)

    @property
    def full_wrap_name(self) -> str:
        return '::'.join([self.parent_class_generator.full_wrap_name, self.method_object.name])

    @property
    def c_arguments_list(self) -> []:
        result = copy.copy(self.argument_generators)
        result.insert(0, ThisArgumentGenerator(self.parent_class_generator))
        return result

    def wrap_declaration(self) -> str:
        arguments = ', '.join(
            [argument_generator.wrap_argument_declaration() for argument_generator in self.argument_generators])
        return 'inline {return_type} {name}({arguments}){const}'.format(
            return_type=self.return_type_generator.wrap_return_type(),
            name=self.method_object.name,
            arguments=arguments,
            const=' const' if self.method_object.const else ''
        )

    def generate_wrap_definition(self, out: FileGenerator, capi_generator: CapiGenerator):
        self.exception_traits = capi_generator.get_exception_traits(self.method_object.noexcept)
        arguments = ', '.join(
            [argument_generator.wrap_argument_declaration() for argument_generator in self.argument_generators])
        arguments_call = [argument_generator.wrap_2_c() for argument_generator in self.c_arguments_list]
        out.put_line('inline {return_type} {full_name}({arguments}){const}'.format(
            return_type=self.return_type_generator.wrap_return_type(),
            full_name=self.full_wrap_name,
            arguments=arguments,
            const=' const' if self.method_object.const else ''
        ))
        with IndentScope(out):
            self.return_type_generator.copy_or_add_ref_when_c_2_wrap = True
            if self.method_object.return_copy_or_add_ref_filled:
                self.return_type_generator.copy_or_add_ref_when_c_2_wrap = self.method_object.return_copy_or_add_ref

            return_expression = self.exception_traits.generate_c_call(
                out, self.return_type_generator, self.full_c_name, arguments_call)
            out.put_return_cpp_statement(return_expression)

    def generate_c_function(self, capi_generator: CapiGenerator):
        argument_declaration_list = [
                argument_generator.c_argument_declaration() for argument_generator in self.c_arguments_list
            ]
        self.exception_traits.modify_c_arguments(argument_declaration_list)
        arguments_declaration = ', '.join(argument_declaration_list)
        implementation_arguments = ', '.join(
            [argument_generator.c_2_implementation() for argument_generator in self.argument_generators])
        c_function_body = FileGenerator(None)
        with IndentScope(c_function_body):
            c_function_body.put_line('{const}{self_impl_class}* self = {to_impl_cast};'.format(
                const='const ' if self.method_object.const else '',
                self_impl_class=self.parent_class_generator.class_object.implementation_class_name,
                to_impl_cast=self.c_arguments_list[0].c_2_implementation()
            ))
            self_access = 'self->'
            if self.parent_class_generator.class_object.pointer_access:
                self_access = '(*self)->'
            implementation_call = '{self_access}{method_name}({arguments})'.format(
                self_access=self_access,
                method_name=self.method_object.name,
                arguments=implementation_arguments
            )
            calling_instructions, return_expression = self.return_type_generator.implementation_2_c_var(
                '', implementation_call
            )
            if return_expression:
                calling_instructions.append('return {0};'.format(return_expression))
            self.exception_traits.generate_implementation_call(
                c_function_body, self.return_type_generator, calling_instructions)
        capi_generator.add_c_function(
            self.parent_class_generator.full_name_array,
            self.return_type_generator.c_argument_declaration(),
            self.full_c_name,
            arguments_declaration,
            c_function_body
        )

    def include_dependent_declaration_headers(self, file_generator: FileGenerator, file_cache: FileCache):
        for argument_generator in self.argument_generators:
            argument_generator.include_dependent_declaration_headers(file_generator, file_cache)
        self.return_type_generator.include_dependent_declaration_headers(file_generator, file_cache)

    def include_dependent_definition_headers(self, file_generator: FileGenerator, file_cache: FileCache):
        self.exception_traits.include_dependent_definition_headers(file_generator, file_cache)
        for argument_generator in self.argument_generators:
            argument_generator.include_dependent_definition_headers(file_generator, file_cache)
        self.return_type_generator.include_dependent_definition_headers(file_generator, file_cache)

    def generate_snippet(self, out: FileGenerator):
        arguments = ', '.join([arg_gen.snippet_implementation_declaration() for arg_gen in self.argument_generators])
        declaration = 'virtual {return_type} {name}({arguments}){const} = 0;'.format(
            return_type=self.return_type_generator.snippet_implementation_declaration(),
            name=self.method_object.name,
            arguments=arguments,
            const=' const' if self.method_object.const else ''
        )
        out.put_line(declaration)


class FunctionGenerator(object):
    def __init__(self, function_object: TFunction,
                 parent_namespace_generator: NamespaceGenerator, params: TBeautifulCapiParams):
        self.function_object = function_object
        self.parent_namespace_generator = parent_namespace_generator
        self.argument_generators = []
        self.return_type_generator = None
        self.params = params
        self.exception_traits = None

    @property
    def full_c_name(self) -> str:
        return get_c_name(self.parent_namespace_generator.full_c_name + '_' + self.function_object.name)

    @property
    def wrap_name(self) -> str:
        return self.function_object.name

    @property
    def full_wrap_name(self) -> str:
        return '::'.join([self.parent_namespace_generator.full_wrap_name, self.function_object.name])

    def generate_wrap_definition(self, out: FileGenerator, capi_generator: CapiGenerator):
        self.exception_traits = capi_generator.get_exception_traits(self.function_object.noexcept)
        arguments = ', '.join(
            [argument_generator.wrap_argument_declaration() for argument_generator in self.argument_generators])
        arguments_call = [argument_generator.wrap_2_c() for argument_generator in self.argument_generators]
        out.put_line('inline {return_type} {name}({arguments})'.format(
            return_type=self.return_type_generator.wrap_return_type(),
            name=self.wrap_name,
            arguments=arguments
        ))
        with IndentScope(out):
            self.return_type_generator.copy_or_add_ref_when_c_2_wrap = True
            if self.function_object.return_copy_or_add_ref_filled:
                self.return_type_generator.copy_or_add_ref_when_c_2_wrap = self.function_object.return_copy_or_add_ref

            return_expression = self.exception_traits.generate_c_call(
                out, self.return_type_generator, self.full_c_name, arguments_call)
            out.put_return_cpp_statement(return_expression)

    def generate_c_function(self, capi_generator: CapiGenerator):
        c_arguments = ', '.join(
            [argument_generator.c_argument_declaration() for argument_generator in self.argument_generators])
        implementation_arguments = ', '.join(
            [argument_generator.c_2_implementation() for argument_generator in self.argument_generators])
        c_function_body = FileGenerator(None)
        with IndentScope(c_function_body):
            implementation_call = '{method_name}({arguments})'.format(
                method_name=self.function_object.implementation_name,
                arguments=implementation_arguments
            )
            calling_instructions, return_expression = self.return_type_generator.implementation_2_c_var(
                '', implementation_call
            )
            if return_expression:
                calling_instructions.append('return {0};'.format(return_expression))
            self.exception_traits.generate_implementation_call(
                c_function_body, self.return_type_generator, calling_instructions)
        capi_generator.add_c_function(
            self.parent_namespace_generator.full_name_array,
            self.return_type_generator.c_argument_declaration(),
            self.full_c_name,
            c_arguments,
            c_function_body
        )

    def include_dependent_definition_headers(self, file_generator: FileGenerator, file_cache: FileCache):
        self.exception_traits.include_dependent_definition_headers(file_generator, file_cache)
        for argument_generator in self.argument_generators:
            argument_generator.include_dependent_definition_headers(file_generator, file_cache)
        self.return_type_generator.include_dependent_definition_headers(file_generator, file_cache)

    def include_dependent_implementation_headers(self, capi_generator: CapiGenerator):
        if self.function_object.implementation_header_filled:
            capi_generator.additional_includes.include_user_header(self.function_object.implementation_header)
