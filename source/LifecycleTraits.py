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


from Parser import TLifecycle
from ParamsParser import TBeautifulCapiParams
from FileGenerator import FileGenerator, IndentScope, IfDefScope
from BuiltinTypeGenerator import BuiltinTypeGenerator
from ThisArgumentGenerator import ThisArgumentGenerator
from Helpers import BeautifulCapiException


def get_base_init(class_generator):
    if class_generator.base_class_generator:
        return ' : {0}({0}::force_creating_from_raw_pointer, 0, false)'.format(
            class_generator.base_class_generator.full_wrap_name)
    else:
        return ''


def get_base_move_init(class_generator):
    if class_generator.base_class_generator:
        return ' : {0}(std::move(other))'.format(class_generator.base_class_generator.full_wrap_name)
    else:
        return ''


def get_has_rvalue_references(class_generator) -> str:
    return class_generator.full_name_array[0].upper() + '_CPP_COMPILER_HAS_RVALUE_REFERENCES'


class LifecycleTraits(object):
    def __init__(self, class_suffix: str, default_init_noexcept: bool, default_finish_noexcept: bool,
                 params: TBeautifulCapiParams):
        self.suffix = class_suffix
        self.params = params
        self.init_method_exception_traits = None
        self.finish_method_exception_traits = None
        self.default_value_for_init_noexcept = default_init_noexcept
        self.default_value_for_finish_noexcept = default_finish_noexcept

    @property
    def access_operator(self) -> str:
        return '->'

    def create_exception_traits(self, properties_container, capi_generator):
        init_method_no_except = self.default_value_for_init_noexcept
        if properties_container.copy_or_add_ref_noexcept_filled:
            init_method_no_except = properties_container.copy_or_add_ref_noexcept
        self.init_method_exception_traits = capi_generator.get_exception_traits(init_method_no_except)
        finish_method_no_except = self.default_value_for_finish_noexcept
        if properties_container.delete_or_release_noexcept_filled:
            finish_method_no_except = properties_container.delete_or_release_noexcept
        self.finish_method_exception_traits = capi_generator.get_exception_traits(
            finish_method_no_except)

    def __create_exception_traits(self, class_generator):
        self.create_exception_traits(class_generator.class_object, class_generator.capi_generator)

    @staticmethod
    def generate_copy_constructor_declaration(out: FileGenerator, class_generator):
        out.put_line('inline {class_short_name}(const {class_name}& other);'.format(
            class_short_name=class_generator.wrap_short_name,
            class_name=class_generator.wrap_name))

    def generate_move_constructor_declaration(self, out: FileGenerator, class_generator):
        if self.params.enable_cpp11_features_in_wrap_code:
            with IfDefScope(out, get_has_rvalue_references(class_generator), False):
                out.put_line('inline {class_short_name}({class_name}&& other);'.format(
                    class_short_name=class_generator.wrap_short_name,
                    class_name=class_generator.wrap_name))

    def generate_std_methods_declarations(self, out: FileGenerator, class_generator):
        self.__create_exception_traits(class_generator)
        out.put_line('inline {class_name}& operator=(const {class_name}& other);'.format(
            class_name=class_generator.wrap_name))
        if self.params.enable_cpp11_features_in_wrap_code:
            with IfDefScope(out, get_has_rvalue_references(class_generator), False):
                out.put_line('inline {class_name}& operator=({class_name}&& other);'.format(
                    class_name=class_generator.wrap_name))
        out.put_line('static inline {class_name} {null_method}();'.format(
            class_name=class_generator.wrap_name,
            null_method=self.params.null_method_name))
        out.put_line('inline bool {0}() const;'.format(self.params.is_null_method_name))
        out.put_line('inline bool {0}() const;'.format(self.params.is_not_null_method_name))
        out.put_line('inline bool operator!() const;')
        out.put_line('inline void* {detach_method}();'.format(detach_method=self.params.detach_method_name))
        out.put_line('inline void* {get_raw_pointer_method}() const;'.format(
            get_raw_pointer_method=self.params.get_raw_pointer_method_name))

    def generate_move_constructor_definition(self, out: FileGenerator, class_generator):
        if self.params.enable_cpp11_features_in_wrap_code:
            with IfDefScope(out, get_has_rvalue_references(class_generator), False):
                out.put_line('inline {namespace}::{class_short_name}({class_name}&& other){base_init}'.format(
                    namespace=class_generator.full_wrap_name,
                    class_short_name=class_generator.wrap_short_name,
                    class_name=class_generator.wrap_name,
                    base_init=get_base_move_init(class_generator))
                )
                with IndentScope(out):
                    class_generator.inheritance_traits.generate_object_assignment(
                        out, class_generator, '', 'other.mObject')
                    class_generator.inheritance_traits.generate_object_assignment(
                        out, class_generator, 'other.', '0')

    def generate_std_methods_definitions(self, out: FileGenerator, class_generator):
        out.put_line('inline {class_name} {class_name}::{null_method}()'.format(
            class_name=class_generator.full_wrap_name,
            null_method=self.params.null_method_name))
        with IndentScope(out):
            out.put_line('return {class_name}({class_name}::force_creating_from_raw_pointer, 0, false);'.format(
                class_name=class_generator.full_wrap_name))
        out.put_line('')
        out.put_line('inline bool {namespace}::{is_null_method}() const'.format(
            namespace=class_generator.full_wrap_name,
            is_null_method=self.params.is_null_method_name))
        with IndentScope(out):
            out.put_line('return !{get_raw}();'.format(get_raw=self.params.get_raw_pointer_method_name))
        out.put_line('')
        out.put_line('inline bool {namespace}::{is_not_null_method}() const'.format(
            namespace=class_generator.full_wrap_name,
            is_not_null_method=self.params.is_not_null_method_name))
        with IndentScope(out):
            out.put_line('return {get_raw}() != 0;'.format(get_raw=self.params.get_raw_pointer_method_name))
        out.put_line('')
        out.put_line('inline bool {namespace}::operator!() const'.format(namespace=class_generator.full_wrap_name))
        with IndentScope(out):
            out.put_line('return !{get_raw}();'.format(get_raw=self.params.get_raw_pointer_method_name))
        out.put_line('')
        out.put_line('inline void* {namespace}::{detach_method}()'.format(
            namespace=class_generator.full_wrap_name, detach_method=self.params.detach_method_name))
        with IndentScope(out):
            out.put_line('void* result = {get_raw}();'.format(get_raw=self.params.get_raw_pointer_method_name))
            out.put_line('SetObject(0);')
            out.put_line('return result;')
        out.put_line('')
        out.put_line('inline void* {namespace}::{get_raw_pointer_method}() const'.format(
            namespace=class_generator.full_wrap_name, get_raw_pointer_method=self.params.get_raw_pointer_method_name))
        with IndentScope(out):
            out.put_line('return {the_most_basic}::mObject ? mObject: 0;'.format(
                the_most_basic=class_generator.the_most_basic.full_wrap_name))


class CopySemantic(LifecycleTraits):
    def __init__(self, params: TBeautifulCapiParams):
        super().__init__(params.copy_semantic_wrapper_class_suffix, False, True, params)

    @property
    def access_operator(self) -> str:
        return '.'

    @property
    def snippet_implementation_usage(self) -> str:
        return self.params.snippet_implementation_value_usage

    @property
    def implementation_2_c(self) -> str:
        return self.params.value_implementation_2_c

    @staticmethod
    def implementation_result_instructions(class_generator, impl_2_c: str,
                                           result_var: str, expression: str) -> ([str], str):
        cast_expr = (impl_2_c if impl_2_c else '{implementation_type}({expression})').format(
                expression=expression,
                implementation_type=class_generator.class_object.implementation_class_name
        )
        instructions = []
        if result_var:
            instructions.append('void* {result_var}(new {cast_expr});'.format(
                result_var=result_var,
                cast_expr=cast_expr
            ))
            return_expression = result_var
        else:
            return_expression = 'new {cast_expr}'.format(cast_expr=cast_expr)
        return instructions, return_expression

    @staticmethod
    def c_2_impl_default() -> str:
        return '*static_cast<{implementation_type}*>({expression})'

    def generate_std_methods_declarations(self, out: FileGenerator, class_generator):
        super().generate_copy_constructor_declaration(out, class_generator)
        super().generate_move_constructor_declaration(out, class_generator)
        out.put_line('enum ECreateFromRawPointer { force_creating_from_raw_pointer };')
        out.put_line('inline {class_name}(ECreateFromRawPointer, void *object_pointer, bool copy_object);'.format(
            class_name=class_generator.wrap_short_name))
        out.put_line('inline ~{class_name}();'.format(
            class_name=class_generator.wrap_short_name))
        super().generate_std_methods_declarations(out, class_generator)

    def __generate_copy_constructor_definition(self, out: FileGenerator, class_generator):
        out.put_line('inline {namespace}::{class_short_name}(const {class_name}& other){base_init}'.format(
            namespace=class_generator.full_wrap_name,
            class_short_name=class_generator.wrap_short_name,
            class_name=class_generator.wrap_name,
            base_init=get_base_init(class_generator))
        )
        with IndentScope(out):
            out.put_line('if (other.{get_raw}())'.format(get_raw=self.params.get_raw_pointer_method_name))
            with IndentScope(out):
                copy_result = self.init_method_exception_traits.generate_c_call(
                    out, BuiltinTypeGenerator('void*'), class_generator.copy_method,
                    ['other.{get_raw}()'.format(get_raw=self.params.get_raw_pointer_method_name)])
                out.put_line('SetObject({copy_result});'.format(copy_result=copy_result))
            out.put_line('else')
            with IndentScope(out):
                out.put_line('SetObject(0);')

    def __generate_raw_copy_constructor_definition(self, out: FileGenerator, class_generator):
        constructor_arguments = '{class_name}::ECreateFromRawPointer, void *object_pointer, bool copy_object'.format(
            class_name=class_generator.full_wrap_name
        )
        out.put_line('inline {namespace}::{class_name}({arguments}){base_init}'.format(
            namespace=class_generator.full_wrap_name,
            class_name=class_generator.wrap_short_name,
            arguments=constructor_arguments,
            base_init=get_base_init(class_generator))
        )
        with IndentScope(out):
            out.put_line('if (object_pointer && copy_object)')
            with IndentScope(out):
                copy_result = self.init_method_exception_traits.generate_c_call(
                    out, BuiltinTypeGenerator('void*'), class_generator.copy_method, ['object_pointer'])
                out.put_line('SetObject({copy_result});'.format(copy_result=copy_result))
            out.put_line('else')
            with IndentScope(out):
                out.put_line('SetObject(object_pointer);')

    def __generate_deallocate(self, out: FileGenerator, class_generator):
        out.put_line('if ({get_raw}())'.format(
            get_raw=self.params.get_raw_pointer_method_name))
        with IndentScope(out):
            self.finish_method_exception_traits.generate_c_call(
                out, BuiltinTypeGenerator('void'), class_generator.delete_method,
                ['{get_raw}()'.format(get_raw=self.params.get_raw_pointer_method_name)])
            out.put_line('SetObject(0);')

    def __generate_destructor(self, out: FileGenerator, class_generator):
        out.put_line('inline {namespace}::~{class_name}()'.format(
            namespace=class_generator.full_wrap_name,
            class_name=class_generator.wrap_short_name)
        )
        with IndentScope(out):
            self.__generate_deallocate(out, class_generator)

    def __generate_assignment_operator(self, out: FileGenerator, class_generator):
        out.put_line('inline {class_name}& {class_name}::operator=(const {class_name}& other)'.format(
            class_name=class_generator.full_wrap_name))
        with IndentScope(out):
            out.put_line('if (this != &other)')
            with IndentScope(out):
                self.__generate_deallocate(out, class_generator)
                out.put_line('if (other.{get_raw}())'.format(get_raw=self.params.get_raw_pointer_method_name))
                with IndentScope(out):
                    copy_result = self.init_method_exception_traits.generate_c_call(
                        out, BuiltinTypeGenerator('void*'), class_generator.copy_method,
                        ['other.mObject'.format(get_raw=self.params.get_raw_pointer_method_name)])
                    out.put_line('SetObject({copy_result});'.format(copy_result=copy_result))
                out.put_line('else')
                with IndentScope(out):
                    out.put_line('SetObject(0);')
            out.put_line('return *this;')

    def __generate_move_assignment_definition(self, out: FileGenerator, class_generator):
        if self.params.enable_cpp11_features_in_wrap_code:
            with IfDefScope(out, get_has_rvalue_references(class_generator), False):
                out.put_line('inline {class_name}& {class_name}::operator=({class_name}&& other)'.format(
                    class_name=class_generator.full_wrap_name))
                with IndentScope(out):
                    out.put_line('if (this != &other)')
                    with IndentScope(out):
                        self.__generate_deallocate(out, class_generator)
                        if class_generator.base_class_generator:
                            out.put_line('{0}::operator=(std::move(other));'.format(
                                class_generator.base_class_generator.full_wrap_name))
                        class_generator.inheritance_traits.generate_object_assignment(
                            out, class_generator, '', 'other.mObject')
                        class_generator.inheritance_traits.generate_object_assignment(
                            out, class_generator, 'other.', '0')
                    out.put_line('return *this;')

    def generate_std_methods_definitions(self, out: FileGenerator, class_generator):
        self.__generate_copy_constructor_definition(out, class_generator)
        out.put_line('')
        super().generate_move_constructor_definition(out, class_generator)
        out.put_line('')
        self.__generate_raw_copy_constructor_definition(out, class_generator)
        out.put_line('')
        self.__generate_destructor(out, class_generator)
        out.put_line('')
        self.__generate_assignment_operator(out, class_generator)
        out.put_line('')
        self.__generate_move_assignment_definition(out, class_generator)
        out.put_line('')
        super().generate_std_methods_definitions(out, class_generator)

    def generate_c_functions(self, class_generator):
        copy_c_function_body = FileGenerator(None)
        with IndentScope(copy_c_function_body):
            copy_constructor_call = 'return new {impl_name}(*{to_impl_cast});'.format(
                impl_name=class_generator.class_object.implementation_class_name,
                to_impl_cast=ThisArgumentGenerator(class_generator).c_2_implementation()
            )
            self.init_method_exception_traits.generate_implementation_call(
                copy_c_function_body, BuiltinTypeGenerator('void*'), [copy_constructor_call])
        argument_list = ['void* object_pointer']
        self.init_method_exception_traits.modify_c_arguments(argument_list)
        class_generator.capi_generator.add_c_function(
            class_generator.full_name_array,
            'void*',
            class_generator.copy_method,
            ', '.join(argument_list),
            copy_c_function_body)

        delete_c_function_body = FileGenerator(None)
        with IndentScope(delete_c_function_body):
            delete_call = 'delete {to_impl_cast};'.format(
                to_impl_cast=ThisArgumentGenerator(class_generator).c_2_implementation()
            )
            self.finish_method_exception_traits.generate_implementation_call(
                delete_c_function_body, BuiltinTypeGenerator('void'), [delete_call])
        argument_list = ['void* object_pointer']
        self.finish_method_exception_traits.modify_c_arguments(argument_list)
        class_generator.capi_generator.add_c_function(
            class_generator.full_name_array,
            'void',
            class_generator.delete_method,
            ', '.join(argument_list),
            delete_c_function_body)


class RawPointerSemantic(LifecycleTraits):
    def __init__(self, params: TBeautifulCapiParams):
        super().__init__(params.raw_pointer_wrapper_class_suffix, False, True, params)

    @property
    def snippet_implementation_usage(self) -> str:
        return self.params.snippet_implementation_raw_usage

    @property
    def implementation_2_c(self) -> str:
        return self.params.raw_implementation_2_c

    @staticmethod
    def implementation_result_instructions(class_generator, impl_2_c, result_var: str, expression: str) -> ([str], str):
        expression = (impl_2_c if impl_2_c else '{expression}').format(
                expression=expression,
                implementation_type=class_generator.class_object.implementation_class_name
        )
        if result_var:
            instructions = ['void* {result_var}({expression});'.format(result_var=result_var, expression=expression)]
            return instructions, result_var
        else:
            return [], expression

    @staticmethod
    def c_2_impl_default() -> str:
        return 'static_cast<{implementation_type}*>({expression})'

    def generate_std_methods_declarations(self, out: FileGenerator, class_generator):
        super().generate_copy_constructor_declaration(out, class_generator)
        super().generate_move_constructor_declaration(out, class_generator)
        out.put_line('enum ECreateFromRawPointer { force_creating_from_raw_pointer };')
        out.put_line('inline {class_name}(ECreateFromRawPointer, void *object_pointer, bool);'.format(
            class_name=class_generator.wrap_short_name))
        out.put_line('inline void {delete_method}();'.format(
            class_name=class_generator.wrap_name, delete_method=self.params.delete_method_name))
        super().generate_std_methods_declarations(out, class_generator)
        out.put_line('inline {class_name}* operator->();'.format(class_name=class_generator.wrap_name))
        out.put_line('inline const {class_name}* operator->() const;'.format(class_name=class_generator.wrap_name))

    def __generate_copy_constructor_definition(self, out: FileGenerator, class_generator):
        out.put_line('inline {namespace}::{class_short_name}(const {class_name}& other){base_init}'.format(
            namespace=class_generator.full_wrap_name,
            class_short_name=class_generator.wrap_short_name,
            class_name=class_generator.wrap_name,
            base_init=get_base_init(class_generator))
        )
        with IndentScope(out):
            out.put_line('SetObject(other.{get_raw}());'.format(get_raw=self.params.get_raw_pointer_method_name))

    @staticmethod
    def __generate_raw_copy_constructor_definition(out: FileGenerator, class_generator):
        constructor_arguments = '{class_name}::ECreateFromRawPointer, void *object_pointer, bool'.format(
            class_name=class_generator.full_wrap_name
        )
        out.put_line('inline {namespace}::{class_name}({arguments}){base_init}'.format(
            namespace=class_generator.full_wrap_name,
            class_name=class_generator.wrap_short_name,
            arguments=constructor_arguments,
            base_init=get_base_init(class_generator))
        )
        with IndentScope(out):
            out.put_line('SetObject(object_pointer);')

    def __generate_delete_method(self, out: FileGenerator, class_generator):
        out.put_line('inline void {class_name}::{delete_method}()'.format(
            class_name=class_generator.full_wrap_name, delete_method=self.params.delete_method_name))
        with IndentScope(out):
            out.put_line('if ({get_raw}())'.format(
                get_raw=self.params.get_raw_pointer_method_name))
            with IndentScope(out):
                self.finish_method_exception_traits.generate_c_call(
                    out, BuiltinTypeGenerator('void'), class_generator.delete_method,
                    ['{get_raw}()'.format(get_raw=self.params.get_raw_pointer_method_name)])
                out.put_line('SetObject(0);')

    def __generate_assignment_operator(self, out: FileGenerator, class_generator):
        out.put_line('inline {class_name}& {class_name}::operator=(const {class_name}& other)'.format(
            class_name=class_generator.full_wrap_name))
        with IndentScope(out):
            out.put_line('if (this != &other)')
            with IndentScope(out):
                out.put_line('SetObject(other.{get_raw}());'.format(get_raw=self.params.get_raw_pointer_method_name))
            out.put_line('return *this;')

    def __generate_move_assignment_definition(self, out: FileGenerator, class_generator):
        if self.params.enable_cpp11_features_in_wrap_code:
            with IfDefScope(out, get_has_rvalue_references(class_generator), False):
                out.put_line('inline {class_name}& {class_name}::operator=({class_name}&& other)'.format(
                    class_name=class_generator.full_wrap_name))
                with IndentScope(out):
                    out.put_line('if (this != &other)')
                    with IndentScope(out):
                        if class_generator.base_class_generator:
                            out.put_line('{0}::operator=(std::move(other));'.format(
                                class_generator.base_class_generator.full_wrap_name))
                        class_generator.inheritance_traits.generate_object_assignment(
                            out, class_generator, '', 'other.mObject')
                        class_generator.inheritance_traits.generate_object_assignment(
                            out, class_generator, 'other.', '0')
                    out.put_line('return *this;')

    def generate_std_methods_definitions(self, out: FileGenerator, class_generator):
        self.__generate_copy_constructor_definition(out, class_generator)
        out.put_line('')
        super().generate_move_constructor_definition(out, class_generator)
        out.put_line('')
        self.__generate_raw_copy_constructor_definition(out, class_generator)
        out.put_line('')
        self.__generate_delete_method(out, class_generator)
        out.put_line('')
        self.__generate_assignment_operator(out, class_generator)
        out.put_line('')
        self.__generate_move_assignment_definition(out, class_generator)
        out.put_line('')
        super().generate_std_methods_definitions(out, class_generator)
        out.put_line('')
        out.put_line('inline {class_name}* {class_name}::operator->()'.format(
            class_name=class_generator.full_wrap_name))
        with IndentScope(out):
            out.put_line('return this;')
        out.put_line('')
        out.put_line('inline const {class_name}* {class_name}::operator->() const'.format(
            class_name=class_generator.full_wrap_name))
        with IndentScope(out):
            out.put_line('return this;')

    def generate_c_functions(self, class_generator):
        delete_c_function_body = FileGenerator(None)
        with IndentScope(delete_c_function_body):
            delete_call = 'delete {to_impl_cast};'.format(
                to_impl_cast=ThisArgumentGenerator(class_generator).c_2_implementation()
            )
            self.finish_method_exception_traits.generate_implementation_call(
                delete_c_function_body, BuiltinTypeGenerator('void'), [delete_call])
        argument_list = ['void* object_pointer']
        self.finish_method_exception_traits.modify_c_arguments(argument_list)
        class_generator.capi_generator.add_c_function(
            class_generator.full_name_array,
            'void',
            class_generator.delete_method,
            ', '.join(argument_list),
            delete_c_function_body)


class RefCountedSemantic(LifecycleTraits):
    def __init__(self, params: TBeautifulCapiParams):
        super().__init__(params.reference_counted_wrapper_class_suffix, True, True, params)

    @property
    def snippet_implementation_usage(self) -> str:
        return self.params.snippet_implementation_reference_counted_usage

    @property
    def implementation_2_c(self) -> str:
        return self.params.reference_counted_implementation_2_c

    @staticmethod
    def implementation_result_instructions(class_generator, impl_2_c, result_var: str, expression: str) -> ([str], str):
        expression = (impl_2_c if impl_2_c else '{expression}').format(
                expression=expression,
                implementation_type=class_generator.class_object.implementation_class_name
        )
        if result_var:
            instructions = ['void* {result_var}({expression});'.format(result_var=result_var, expression=expression)]
            return instructions, result_var
        else:
            return [],  expression

    @staticmethod
    def c_2_impl_default() -> str:
        return 'static_cast<{implementation_type}*>({expression})'

    def generate_std_methods_declarations(self, out: FileGenerator, class_generator):
        super().generate_copy_constructor_declaration(out, class_generator)
        super().generate_move_constructor_declaration(out, class_generator)
        out.put_line('enum ECreateFromRawPointer { force_creating_from_raw_pointer };')
        out.put_line('inline {class_name}(ECreateFromRawPointer, void *object_pointer, bool add_ref_object);'.format(
            class_name=class_generator.wrap_short_name))
        out.put_line('inline ~{class_name}();'.format(
            class_name=class_generator.wrap_short_name))
        super().generate_std_methods_declarations(out, class_generator)
        out.put_line('inline {class_name}* operator->();'.format(class_name=class_generator.wrap_name))
        out.put_line('inline const {class_name}* operator->() const;'.format(class_name=class_generator.wrap_name))

    def __generate_copy_constructor_definition(self, out: FileGenerator, class_generator):
        out.put_line('inline {namespace}::{class_short_name}(const {class_name}& other){base_init}'.format(
            namespace=class_generator.full_wrap_name,
            class_short_name=class_generator.wrap_short_name,
            class_name=class_generator.wrap_name,
            base_init=get_base_init(class_generator))
        )
        with IndentScope(out):
            out.put_line('SetObject(other.{get_raw}());'.format(get_raw=self.params.get_raw_pointer_method_name))
            out.put_line('if (other.{get_raw}())'.format(get_raw=self.params.get_raw_pointer_method_name))
            with IndentScope(out):
                self.init_method_exception_traits.generate_c_call(
                    out, BuiltinTypeGenerator('void'), class_generator.add_ref_method,
                    ['other.{get_raw}()'.format(get_raw=self.params.get_raw_pointer_method_name)])

    def __generate_raw_copy_constructor_definition(self, out: FileGenerator, class_generator):
        constructor_arguments = '{class_name}::ECreateFromRawPointer, void *object_pointer, bool add_ref_object'.format(
            class_name=class_generator.full_wrap_name
        )
        out.put_line('inline {namespace}::{class_name}({arguments}){base_init}'.format(
            namespace=class_generator.full_wrap_name,
            class_name=class_generator.wrap_short_name,
            arguments=constructor_arguments,
            base_init=get_base_init(class_generator))
        )
        with IndentScope(out):
            out.put_line('SetObject(object_pointer);')
            out.put_line('if (add_ref_object && object_pointer)')
            with IndentScope(out):
                self.init_method_exception_traits.generate_c_call(
                    out, BuiltinTypeGenerator('void'), class_generator.add_ref_method, ['object_pointer'])

    def __generate_deallocate(self, out: FileGenerator, class_generator):
        out.put_line('if ({get_raw}())'.format(
            get_raw=self.params.get_raw_pointer_method_name))
        with IndentScope(out):
            self.finish_method_exception_traits.generate_c_call(
                out, BuiltinTypeGenerator('void'), class_generator.release_method,
                ['{get_raw}()'.format(get_raw=self.params.get_raw_pointer_method_name)])
            out.put_line('SetObject(0);')

    def __generate_destructor(self, out: FileGenerator, class_generator):
        out.put_line('inline {namespace}::~{class_name}()'.format(
            namespace=class_generator.full_wrap_name,
            class_name=class_generator.wrap_short_name)
        )
        with IndentScope(out):
            self.__generate_deallocate(out, class_generator)

    def __generate_assignment_operator(self, out: FileGenerator, class_generator):
        out.put_line('inline {class_name}& {class_name}::operator=(const {class_name}& other)'.format(
            class_name=class_generator.full_wrap_name))
        with IndentScope(out):
            out.put_line('if ({get_raw}() != other.{get_raw}())'.format(
                get_raw=self.params.get_raw_pointer_method_name))
            with IndentScope(out):
                self.__generate_deallocate(out, class_generator)
                out.put_line('SetObject(other.{get_raw}());'.format(get_raw=self.params.get_raw_pointer_method_name))
                out.put_line('if (other.{get_raw}())'.format(get_raw=self.params.get_raw_pointer_method_name))
                with IndentScope(out):
                    self.init_method_exception_traits.generate_c_call(
                        out, BuiltinTypeGenerator('void'), class_generator.add_ref_method,
                        ['other.{get_raw}()'.format(get_raw=self.params.get_raw_pointer_method_name)])
            out.put_line('return *this;')

    def __generate_move_assignment_definition(self, out: FileGenerator, class_generator):
        if self.params.enable_cpp11_features_in_wrap_code:
            with IfDefScope(out, get_has_rvalue_references(class_generator), False):
                out.put_line('inline {class_name}& {class_name}::operator=({class_name}&& other)'.format(
                    class_name=class_generator.full_wrap_name))
                with IndentScope(out):
                    out.put_line('if ({get_raw}() != other.{get_raw}())'.format(
                        get_raw=self.params.get_raw_pointer_method_name))
                    with IndentScope(out):
                        self.__generate_deallocate(out, class_generator)
                        if class_generator.base_class_generator:
                            out.put_line('{0}::operator=(std::move(other));'.format(
                                class_generator.base_class_generator.full_wrap_name))
                        class_generator.inheritance_traits.generate_object_assignment(
                            out, class_generator, '', 'other.mObject')
                        class_generator.inheritance_traits.generate_object_assignment(
                            out, class_generator, 'other.', '0')
                    out.put_line('return *this;')

    def generate_std_methods_definitions(self, out: FileGenerator, class_generator):
        self.__generate_copy_constructor_definition(out, class_generator)
        out.put_line('')
        super().generate_move_constructor_definition(out, class_generator)
        out.put_line('')
        self.__generate_raw_copy_constructor_definition(out, class_generator)
        out.put_line('')
        self.__generate_destructor(out, class_generator)
        out.put_line('')
        self.__generate_assignment_operator(out, class_generator)
        out.put_line('')
        self.__generate_move_assignment_definition(out, class_generator)
        out.put_line('')
        super().generate_std_methods_definitions(out, class_generator)
        out.put_line('')
        out.put_line('inline {class_name}* {class_name}::operator->()'.format(
            class_name=class_generator.full_wrap_name))
        with IndentScope(out):
            out.put_line('return this;')
        out.put_line('')
        out.put_line('inline const {class_name}* {class_name}::operator->() const'.format(
            class_name=class_generator.full_wrap_name))
        with IndentScope(out):
            out.put_line('return this;')

    def generate_c_functions(self, class_generator):
        add_ref_c_function_body = FileGenerator(None)
        with IndentScope(add_ref_c_function_body):
            add_ref_call = 'intrusive_ptr_add_ref({to_impl_cast});'.format(
                to_impl_cast=ThisArgumentGenerator(class_generator).c_2_implementation()
            )
            self.init_method_exception_traits.generate_implementation_call(
                add_ref_c_function_body, BuiltinTypeGenerator('void*'), [add_ref_call])
        argument_list = ['void* object_pointer']
        self.init_method_exception_traits.modify_c_arguments(argument_list)
        class_generator.capi_generator.add_c_function(
            class_generator.full_name_array,
            'void',
            class_generator.add_ref_method,
            ', '.join(argument_list),
            add_ref_c_function_body)

        release_c_function_body = FileGenerator(None)
        with IndentScope(release_c_function_body):
            release_call = 'intrusive_ptr_release({to_impl_cast});'.format(
                to_impl_cast=ThisArgumentGenerator(class_generator).c_2_implementation()
            )
            self.finish_method_exception_traits.generate_implementation_call(
                release_c_function_body, BuiltinTypeGenerator('void'), [release_call])
        argument_list = ['void* object_pointer']
        self.finish_method_exception_traits.modify_c_arguments(argument_list)
        class_generator.capi_generator.add_c_function(
            class_generator.full_name_array,
            'void',
            class_generator.release_method,
            ', '.join(argument_list),
            release_c_function_body)


str_to_lifecycle = {
    TLifecycle.copy_semantic: CopySemantic,
    TLifecycle.raw_pointer_semantic: RawPointerSemantic,
    TLifecycle.reference_counted: RefCountedSemantic
}


def create_lifecycle_traits(lifecycle: TLifecycle, params: TBeautifulCapiParams) -> LifecycleTraits:
    if lifecycle in str_to_lifecycle:
        return str_to_lifecycle[lifecycle](params)
    raise BeautifulCapiException('invalid lifecycle value, {0}'.format(lifecycle))
