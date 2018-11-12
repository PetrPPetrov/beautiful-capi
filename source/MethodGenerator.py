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

from Parser import TMethod, TFunction, TConstructor, TImplementationCode, TProlog
from ParamsParser import TBeautifulCapiParams
from FileGenerator import FileGenerator, IndentScope
from FileCache import FileCache
from ClassGenerator import ClassGenerator
from NamespaceGenerator import NamespaceGenerator
from ArgumentGenerator import ClassTypeGenerator, ArgumentGenerator
from ThisArgumentGenerator import ThisArgumentGenerator
from CapiGenerator import CapiGenerator
from LifecycleTraits import get_base_init
from Helpers import get_c_name, get_full_method_name


def generate_custom_implementation_code(implementation_code: TImplementationCode,
                                        argument_generators: [ArgumentGenerator],
                                        return_type_generator) -> [str]:
    substitute_map = {}
    for argument in argument_generators:
        substitute_map.update({argument.name + '_c_2_impl': argument.c_2_implementation()})
        substitute_map.update(
            {argument.name + '_impl_type': argument.type_generator.snippet_implementation_declaration()})
        substitute_map.update({argument.name + '_c_type': argument.type_generator.c_argument_declaration()})
    substitute_map.update({'return_c_type': return_type_generator.c_argument_declaration()})
    substitute_map.update({'return_impl_type': return_type_generator.snippet_implementation_declaration()})

    def substitute_return(expression: str, start_keyword: str, end_keyword: str, func: callable) -> str:
        result = ''
        cur_index = 0
        found_start_index = expression.find(start_keyword, cur_index)
        while found_start_index != -1:
            result += expression[cur_index:found_start_index]
            next_index_to_find = found_start_index + len(start_keyword)
            cur_index = next_index_to_find
            found_end_index = expression.find(end_keyword, next_index_to_find)
            if found_end_index != -1:
                sub_expression = expression[found_start_index + len(start_keyword):found_end_index]
                modified_line = func(sub_expression)
                result += modified_line
                cur_index = found_end_index + len(end_keyword)
            found_start_index = expression.find(start_keyword, cur_index)
        result += expression[cur_index:]
        return result

    def return_generic(expression: str) -> str:
        prepared_expression = expression.format_map(substitute_map)
        result_lines, return_expression = return_type_generator.implementation_2_c_var('', prepared_expression)
        return return_expression

    def return_value(expression: str) -> str:
        return return_type_generator.value_2_c(return_generic(expression))

    def return_pointer(expression: str) -> str:
        return return_type_generator.pointer_2_c(return_generic(expression))

    calling_instructions = []
    for line in implementation_code.all_items:
        processed_return = substitute_return(line, '@ret@', '@', return_generic)
        processed_return_val = substitute_return(processed_return, '@retval@', '@', return_value)
        processed_return_ptr = substitute_return(processed_return_val, '@retptr@', '@', return_pointer)
        prepared_line = processed_return_ptr.format_map(substitute_map)
        if prepared_line:
            calling_instructions.append(prepared_line)
    return calling_instructions


class ConstructorGenerator(object):
    def __init__(self, constructor_object: TConstructor, parent_class_generator: ClassGenerator,
                 params: TBeautifulCapiParams):
        self.constructor_object = constructor_object
        self.parent_class_generator = parent_class_generator
        self.parent_class_as_argument_type = ClassTypeGenerator(parent_class_generator)
        class_as_argument = self.parent_class_as_argument_type
        class_as_argument.copy_or_add_ref_when_c_2_wrap = self.constructor_object.return_copy_or_add_ref
        self.argument_generators = []
        self.params = params
        self.exception_traits = None

    @property
    def access_operator(self) -> str:
        return self.parent_class_generator.access_operator

    @property
    def full_name(self) -> str:
        return '::'.join([self.parent_class_generator.full_name, self.constructor_object.name])

    @property
    def full_c_name(self) -> str:
        return get_c_name(self.parent_class_generator.full_c_name + '_' + self.constructor_object.name)

    @property
    def wrap_name(self) -> str:
        return '::'.join([self.parent_class_generator.wrap_name, self.constructor_object.name])

    @property
    def full_wrap_name(self) -> str:
        return '::'.join([self.parent_class_generator.full_wrap_name, self.constructor_object.name])

    def wrap_declaration(self) -> str:
        arguments = ', '.join(
            [argument_generator.wrap_argument_declaration() for argument_generator in self.argument_generators])
        return 'inline {explicit}{name}({arguments})'.format(
            name=self.parent_class_generator.wrap_short_name,
            arguments=arguments,
            explicit='explicit ' if self.constructor_object.explicit else ''
        )

    def generate_wrap_definition(self, out: FileGenerator, capi_generator: CapiGenerator):
        self.exception_traits = capi_generator.get_exception_traits(self.constructor_object.noexcept)
        arguments = ', '.join(
            [argument_generator.wrap_argument_declaration() for argument_generator in self.argument_generators])
        arguments_call = [argument_generator.wrap_2_c() for argument_generator in self.argument_generators]
        out.put_line('inline {namespace}::{class_name}({arguments}){base_init}'.format(
            namespace=self.parent_class_generator.full_wrap_name,
            class_name=self.parent_class_generator.wrap_short_name,
            arguments=arguments,
            base_init=get_base_init(self.parent_class_generator)
        ))
        with IndentScope(out):
            result_expression = self.exception_traits.generate_c_call(
                out, self.parent_class_as_argument_type, self.full_c_name, arguments_call)
            out.put_line('SetObject({result_expression}.{detach}());'.format(
                result_expression=result_expression, detach=self.params.detach_method_name))

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
            if self.constructor_object.implementation_codes:
                calling_instructions = generate_custom_implementation_code(
                    self.constructor_object.implementation_codes[0],
                    self.argument_generators,
                    self.parent_class_as_argument_type)
            else:
                implementation_call = 'return new {impl_class}({arguments});'.format(
                    impl_class=self.parent_class_generator.class_object.implementation_class_name,
                    arguments=implementation_arguments
                )
                calling_instructions = [implementation_call]
            self.exception_traits.generate_implementation_call(
                c_function_body, self.parent_class_as_argument_type, calling_instructions)
        capi_generator.add_c_function(
            self.parent_class_generator.full_name_array[:-1],
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
    def access_operator(self) -> str:
        return self.parent_class_generator.access_operator

    @property
    def name(self) -> str:
        return self.method_object.name

    @property
    def full_name(self) -> str:
        return '::'.join([self.parent_class_generator.full_name, self.method_object.name])

    @property
    def c_name(self) -> str:
        compound_name = get_full_method_name(self.method_object)
        return get_c_name('_'.join(compound_name))

    @property
    def full_c_name(self) -> str:
        return get_c_name(self.parent_class_generator.full_c_name + '_' + self.c_name)

    @property
    def wrap_name(self) -> str:
        return self.method_object.name

    @property
    def full_wrap_name(self) -> str:
        return '::'.join([self.parent_class_generator.full_wrap_name, self.method_object.name])

    @property
    def callback_type(self) -> str:
        return self.full_c_name + '_callback_type'

    @property
    def c_arguments_list(self) -> []:
        result = copy.copy(self.argument_generators)
        result.insert(0, ThisArgumentGenerator(self.parent_class_generator))
        return result

    @property
    def prolog(self) -> TProlog:
        if self.method_object.prologs:
            return self.method_object.prologs[0]
        return self.parent_class_generator.method_prolog

    def wrap_declaration(self, capi_generator: CapiGenerator) -> str:
        self.exception_traits = capi_generator.get_exception_traits(self.method_object.noexcept)
        arguments = ', '.join(
            [argument_generator.wrap_argument_declaration() for argument_generator in self.argument_generators])
        return 'inline {return_type} {name}({arguments}){const}'.format(
            return_type=self.return_type_generator.wrap_return_type(),
            name=self.method_object.name,
            arguments=arguments,
            const=' const' if self.method_object.const else ''
        )

    def generate_wrap_definition(self, out: FileGenerator):
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
            if self.method_object.implementation_codes:
                calling_instructions = generate_custom_implementation_code(
                    self.method_object.implementation_codes[0],
                    self.argument_generators,
                    self.return_type_generator)
            else:
                function_prolog = self.prolog
                if function_prolog:
                    c_function_body.put_lines(function_prolog.all_items)
                self_access = 'self->'
                if self.parent_class_generator.class_object.pointer_access:
                    self_access = '(*self)->'
                method_name = self.method_object.implementation_name
                if not method_name:
                    method_name = self.method_object.name
                if self.method_object.getter_field_name_filled:
                    implementation_call = '{self_access}{field_name}'.format(
                        self_access=self_access, field_name=self.method_object.getter_field_name)
                elif self.method_object.setter_field_name_filled:
                    implementation_call = '{self_access}{field_name} = {arguments}'.format(
                        self_access=self_access, field_name=self.method_object.setter_field_name,
                        arguments=implementation_arguments
                    )
                else:
                    implementation_call = '{self_access}{method_name}({arguments})'.format(
                        self_access=self_access,
                        method_name=method_name,
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
            self.parent_class_generator.full_name_array[:-1],
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
    def name(self) -> str:
        return self.function_object.name

    @property
    def full_name(self) -> str:
        return '::'.join([self.parent_namespace_generator.full_name, self.name])

    @property
    def c_name(self) -> str:
        return get_c_name(self.name + '_' + self.function_object.overload_suffix if self.function_object.overload_suffix
                          else self.name)

    @property
    def full_c_name(self) -> str:
        return get_c_name(self.parent_namespace_generator.full_c_name + '_' + self.c_name)

    @property
    def wrap_name(self) -> str:
        return self.name

    @property
    def full_wrap_name(self) -> str:
        return '::'.join([self.parent_namespace_generator.full_wrap_name, self.name])

    @property
    def prolog(self) -> TProlog:
        if self.function_object.prologs:
            return self.function_object.prologs[0]
        return self.parent_namespace_generator.function_prolog

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
            self.return_type_generator.copy_or_add_ref_when_c_2_wrap = self.function_object.return_copy_or_add_ref
            return_expression = self.exception_traits.generate_c_call(
                out, self.return_type_generator, self.full_c_name, arguments_call)
            out.put_return_cpp_statement(return_expression)

    def generate_c_function(self, capi_generator: CapiGenerator):
        c_arguments_list = [
            argument_generator.c_argument_declaration() for argument_generator in self.argument_generators
        ]
        self.exception_traits.modify_c_arguments(c_arguments_list)
        c_arguments = ', '.join(c_arguments_list)
        implementation_arguments = ', '.join(
            [argument_generator.c_2_implementation() for argument_generator in self.argument_generators])
        c_function_body = FileGenerator(None)
        with IndentScope(c_function_body):
            function_name = self.function_object.implementation_name
            if not function_name:
                function_name = self.function_object.name
            implementation_call = '{function_name}({arguments})'.format(
                function_name=function_name,
                arguments=implementation_arguments
            )
            if self.function_object.implementation_codes:
                calling_instructions = generate_custom_implementation_code(
                    self.function_object.implementation_codes[0],
                    self.argument_generators,
                    self.return_type_generator
                )
            else:
                function_prolog = self.prolog
                if function_prolog:
                    c_function_body.put_lines(function_prolog.all_items)
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
