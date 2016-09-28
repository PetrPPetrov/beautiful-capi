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
from FileGenerator import FileGenerator, IndentScope
from ArgumentGenerator import BuiltinTypeGenerator, ThisArgumentGenerator
from Helpers import BeautifulCapiException


def get_base_init(class_generator):
    if class_generator.base_class_generator:
        return ' : {0}({0}:force_creating_from_raw_pointer, 0, false)'.format(
            class_generator.base_class_generator.full_wrap_name)
    else:
        return ''


class LifecycleTraits(object):
    def __init__(self, class_suffix: str, params: TBeautifulCapiParams):
        self.suffix = class_suffix
        self.params = params
        self.init_method_exception_traits = None
        self.finish_method_exception_traits = None

    def __create_exception_traits(self, class_generator):
        init_method_no_except = False
        if class_generator.class_object.copy_or_add_ref_noexcept_filled:
            init_method_no_except = class_generator.class_object.copy_or_add_ref_noexcept
        self.init_method_exception_traits = class_generator.capi_generator.get_exception_traits(init_method_no_except)
        finish_method_no_except = True
        if class_generator.class_object.delete_or_release_noexcept_filled:
            finish_method_no_except = class_generator.class_object.delete_or_release_noexcept
        self.finish_method_exception_traits = class_generator.capi_generator.get_exception_traits(
            finish_method_no_except)

    @staticmethod
    def generate_copy_constructor_declaration(out: FileGenerator, class_generator):
        out.put_line('inline {class_name}(const {class_name}& other);'.format(
            class_name=class_generator.wrap_name))

    def generate_std_methods_declarations(self, out: FileGenerator, class_generator):
        self.__create_exception_traits(class_generator)
        out.put_line('inline {class_name}& operator=(const {class_name}& other);'.format(
            class_name=class_generator.wrap_name))
        out.put_line('inline bool {0}() const;'.format(self.params.is_null_method))
        out.put_line('inline bool {0}() const;'.format(self.params.is_not_null_method))
        out.put_line('inline bool operator!() const;')
        out.put_line('inline void* Detach();')
        out.put_line('inline void* get_raw_pointer() const;')

    def generate_std_methods_definitions(self, out: FileGenerator, class_generator):
        out.put_line('inline bool {namespace}::{is_null_method}() const'.format(
            namespace=class_generator.full_wrap_name,
            is_null_method=self.params.is_null_method))
        with IndentScope(out):
            out.put_line('return !mObject;')
        out.put_line('')
        out.put_line('inline bool {namespace}::{is_not_null_method}() const'.format(
            namespace=class_generator.full_wrap_name,
            is_not_null_method=self.params.is_not_null_method))
        with IndentScope(out):
            out.put_line('return mObject != 0;')
        out.put_line('')
        out.put_line('inline bool {namespace}::operator!() const'.format(namespace=class_generator.full_wrap_name))
        with IndentScope(out):
            out.put_line('return !mObject;')
        out.put_line('')
        out.put_line('inline void* {namespace}::Detach()'.format(namespace=class_generator.full_wrap_name))
        with IndentScope(out):
            out.put_line('void* result = mObject;')
            out.put_line('SetObject(0);')
            out.put_line('return result;')
        out.put_line('')
        out.put_line('inline void* {namespace}::get_raw_pointer() const'.format(namespace=class_generator.full_wrap_name))
        with IndentScope(out):
            out.put_line('return mObject;')


class CopySemantic(LifecycleTraits):
    def __init__(self, params: TBeautifulCapiParams):
        super().__init__(params.wrapper_class_suffix_copy_semantic, params)

    @staticmethod
    def implementation_result_instructions(class_generator, result_var: str, expression: str) -> ([str], str):
        instructions = ['{impl_class_name} result_implementation_copy({expression});'.format(
            impl_class_name=class_generator.class_object.implementation_class_name,
            result_var=result_var,
            expression=expression
        )]
        if result_var:
            instructions.append('void* {result_var}({copy_method}(&result_implementation_copy));'.format(
                result_var=result_var,
                copy_method=class_generator.copy_method
            ))
            return_expression = result_var
        else:
            return_expression = '{copy_method}(&result_implementation_copy)'.format(
                result_var=result_var,
                copy_method=class_generator.copy_method)
        return instructions, return_expression

    def generate_std_methods_declarations(self, out: FileGenerator, class_generator):
        super().generate_copy_constructor_declaration(out, class_generator)
        out.put_line('enum ECreateFromRawPointer { force_creating_from_raw_pointer };')
        out.put_line('inline {class_name}(ECreateFromRawPointer, void *object_pointer, bool copy_object);'.format(
            class_name=class_generator.wrap_name))
        out.put_line('inline ~{class_name}();'.format(
            class_name=class_generator.wrap_name))
        super().generate_std_methods_declarations(out, class_generator)

    def __generate_copy_constructor_definition(self, out: FileGenerator, class_generator):
        out.put_line('inline {class_name}(const {class_name}& other){base_init}'.format(
            class_name=class_generator.full_wrap_name, base_init=get_base_init(class_generator))
        )
        with IndentScope(out):
            out.put_line('if (other.mObject)')
            with IndentScope(out):
                copy_result = self.init_method_exception_traits.generate_c_call(
                    out, BuiltinTypeGenerator('void*'), class_generator.copy_method, ['other.mObject'])
                out.put_line('SetObject({copy_result});'.format(copy_result=copy_result))
            out.put_line('else')
            with IndentScope(out):
                out.put_line('SetObject(0);')

    def __generate_raw_copy_constructor_definition(self, out: FileGenerator, class_generator):
        out.put_line('inline {class_name}(void *object_pointer, bool copy_object){base_init}'.format(
            class_name=class_generator.full_wrap_name, base_init=get_base_init(class_generator))
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

    def __generate_destructor(self, out: FileGenerator, class_generator):
        out.put_line('inline {namespace}::~{class_name}()'.format(
            namespace=class_generator.parent_namespace.full_name,
            class_name=class_generator.wrap_name)
        )
        with IndentScope(out):
            out.put_line('if (mObject)')
            with IndentScope(out):
                self.finish_method_exception_traits.generate_c_call(
                    out, BuiltinTypeGenerator('void'), class_generator.delete_method, ['mObject'])
                out.put_line('SetObject(0);')

    def __generate_assignment_operator(self, out: FileGenerator, class_generator):
        out.put_line('inline {class_name}& {class_name}::operator=(const {class_name}& other)'.format(
            class_name=class_generator.full_wrap_name))
        with IndentScope(out):
            out.put_line('if (mObject != other.mObject)')
            with IndentScope(out):
                out.put_line('if (mObject)')
                with IndentScope(out):
                    self.finish_method_exception_traits.generate_c_call(
                        out, BuiltinTypeGenerator('void'), class_generator.delete_method, ['mObject'])
                    out.put_line('SetObject(0);')
                out.put_line('if (other.mObject)')
                with IndentScope(out):
                    copy_result = self.init_method_exception_traits.generate_c_call(
                        out, BuiltinTypeGenerator('void*'), class_generator.copy_method, ['other.mObject'])
                    out.put_line('SetObject({copy_result});'.format(copy_result=copy_result))
                out.put_line('else')
                with IndentScope(out):
                    out.put_line('SetObject(0);')
            out.put_line('return *this;')

    def generate_std_methods_definitions(self, out: FileGenerator, class_generator):
        self.__generate_copy_constructor_definition(out, class_generator)
        out.put_line('')
        self.__generate_raw_copy_constructor_definition(out, class_generator)
        out.put_line('')
        self.__generate_destructor(out, class_generator)
        out.put_line('')
        self.__generate_assignment_operator(out, class_generator)
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
        class_generator.capi_generator.add_c_function(
            class_generator.full_name_array,
            'void*',
            class_generator.copy_method,
            'void* object_pointer',
            copy_c_function_body)

        delete_c_function_body = FileGenerator(None)
        with IndentScope(delete_c_function_body):
            delete_call = 'delete {to_impl_cast};'.format(
                to_impl_cast=ThisArgumentGenerator(class_generator).c_2_implementation()
            )
            self.finish_method_exception_traits.generate_implementation_call(
                delete_c_function_body, BuiltinTypeGenerator('void'), [delete_call])
        class_generator.capi_generator.add_c_function(
            class_generator.full_name_array,
            'void',
            class_generator.delete_method,
            'void* object_pointer',
            delete_c_function_body)


class RawPointerSemantic(LifecycleTraits):
    def __init__(self, params: TBeautifulCapiParams):
        super().__init__(params.wrapper_class_suffix_raw_pointer, params)

    @staticmethod
    def implementation_result_instructions(class_generator, result_var: str, expression: str) -> ([str], str):
        if result_var:
            instructions = ['void* {result_var}({expression});'.format(result_var=result_var, expression=expression)]
            return instructions, result_var
        else:
            return [], expression

    def generate_std_methods_declarations(self, out: FileGenerator, class_generator):
        super().generate_copy_constructor_declaration(out, class_generator)
        out.put_line('enum ECreateFromRawPointer { force_creating_from_raw_pointer };')
        out.put_line('inline {class_name}(ECreateFromRawPointer, void *object_pointer, bool);'.format(
            class_name=class_generator.wrap_name))
        out.put_line('inline void Delete();'.format(
            class_name=class_generator.wrap_name))
        super().generate_std_methods_declarations(out, class_generator)
        out.put_line('inline {class_name}* operator->();'.format(class_name=class_generator.wrap_name))
        out.put_line('inline const {class_name}* operator->() const;'.format(class_name=class_generator.wrap_name))

    @staticmethod
    def __generate_copy_constructor_definition(out: FileGenerator, class_generator):
        out.put_line('inline {class_name}(const {class_name}& other){base_init}'.format(
            class_name=class_generator.full_wrap_name, base_init=get_base_init(class_generator))
        )
        with IndentScope(out):
            out.put_line('SetObject(other.mObject);')

    @staticmethod
    def __generate_raw_copy_constructor_definition(out: FileGenerator, class_generator):
        out.put_line('inline {class_name}(void *object_pointer, bool){base_init}'.format(
            class_name=class_generator.full_wrap_name, base_init=get_base_init(class_generator))
        )
        with IndentScope(out):
            out.put_line('SetObject(object_pointer);')

    def __generate_delete_method(self, out: FileGenerator, class_generator):
        out.put_line('inline void {class_name}::Delete()'.format(class_name=class_generator.full_wrap_name))
        with IndentScope(out):
            out.put_line('if (mObject)')
            with IndentScope(out):
                self.finish_method_exception_traits.generate_c_call(
                    out, BuiltinTypeGenerator('void'), class_generator.delete_method, ['mObject'])
                out.put_line('SetObject(0);')

    @staticmethod
    def __generate_assignment_operator(out: FileGenerator, class_generator):
        out.put_line('inline {class_name}& {class_name}::operator=(const {class_name}& other)'.format(
            class_name=class_generator.full_wrap_name))
        with IndentScope(out):
            out.put_line('SetObject(other.mObject);')
            out.put_line('return *this;')

    def generate_std_methods_definitions(self, out: FileGenerator, class_generator):
        self.__generate_copy_constructor_definition(out, class_generator)
        out.put_line('')
        self.__generate_raw_copy_constructor_definition(out, class_generator)
        out.put_line('')
        self.__generate_delete_method(out, class_generator)
        out.put_line('')
        self.__generate_assignment_operator(out, class_generator)
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
        class_generator.capi_generator.add_c_function(
            class_generator.full_name_array,
            'void',
            class_generator.delete_method,
            'void* object_pointer',
            delete_c_function_body)


class RefCountedSemantic(LifecycleTraits):
    def __init__(self, params: TBeautifulCapiParams):
        super().__init__(params.wrapper_class_suffix_reference_counted, params)

    @staticmethod
    def implementation_result_instructions(class_generator, result_var: str, expression: str) -> ([str], str):
        if result_var:
            instructions = ['void* {result_var}({expression});'.format(result_var=result_var, expression=expression)]
            return instructions, result_var
        else:
            return [], expression

    def generate_std_methods_declarations(self, out: FileGenerator, class_generator):
        super().generate_copy_constructor_declaration(out, class_generator)
        out.put_line('enum ECreateFromRawPointer { force_creating_from_raw_pointer };')
        out.put_line('inline {class_name}(ECreateFromRawPointer, void *object_pointer, bool add_ref_object);'.format(
            class_name=class_generator.wrap_name))
        out.put_line('inline ~{class_name}();'.format(
            class_name=class_generator.wrap_name))
        super().generate_std_methods_declarations(out, class_generator)
        out.put_line('inline {class_name}* operator->();'.format(class_name=class_generator.wrap_name))
        out.put_line('inline const {class_name}* operator->() const;'.format(class_name=class_generator.wrap_name))

    def __generate_copy_constructor_definition(self, out: FileGenerator, class_generator):
        out.put_line('inline {class_name}(const {class_name}& other){base_init}'.format(
            class_name=class_generator.full_wrap_name, base_init=get_base_init(class_generator))
        )
        with IndentScope(out):
            out.put_line('SetObject(other.mObject);')
            out.put_line('if (other.mObject)')
            with IndentScope(out):
                self.init_method_exception_traits.generate_c_call(
                    out, BuiltinTypeGenerator('void'), class_generator.add_ref_method, ['other.mObject'])

    def __generate_raw_copy_constructor_definition(self, out: FileGenerator, class_generator):
        out.put_line('inline {class_name}(void *object_pointer, bool add_ref_object){base_init}'.format(
            class_name=class_generator.full_wrap_name, base_init=get_base_init(class_generator))
        )
        with IndentScope(out):
            out.put_line('SetObject(object_pointer);')
            out.put_line('if (add_ref_object && object_pointer)')
            with IndentScope(out):
                self.init_method_exception_traits.generate_c_call(
                    out, BuiltinTypeGenerator('void'), class_generator.add_ref_method, ['object_pointer'])

    def __generate_destructor(self, out: FileGenerator, class_generator):
        out.put_line('inline {namespace}::~{class_name}()'.format(
            namespace=class_generator.parent_namespace.full_name,
            class_name=class_generator.wrap_name)
        )
        with IndentScope(out):
            out.put_line('if (mObject)')
            with IndentScope(out):
                self.finish_method_exception_traits.generate_c_call(
                    out, BuiltinTypeGenerator('void'), class_generator.release_method, ['mObject'])
                out.put_line('SetObject(0);')

    def __generate_assignment_operator(self, out: FileGenerator, class_generator):
        out.put_line('inline {class_name}& {class_name}::operator=(const {class_name}& other)'.format(
            class_name=class_generator.full_wrap_name))
        with IndentScope(out):
            out.put_line('if (mObject != other.mObject)')
            with IndentScope(out):
                out.put_line('if (mObject)')
                with IndentScope(out):
                    self.finish_method_exception_traits.generate_c_call(
                        out, BuiltinTypeGenerator('void'), class_generator.release_method, ['mObject'])
                    out.put_line('SetObject(0);')
                out.put_line('SetObject(other.mObject);')
                out.put_line('if (other.mObject)')
                with IndentScope(out):
                    self.init_method_exception_traits.generate_c_call(
                        out, BuiltinTypeGenerator('void'), class_generator.add_ref_method, ['other.mObject'])
            out.put_line('return *this;')

    def generate_std_methods_definitions(self, out: FileGenerator, class_generator):
        self.__generate_copy_constructor_definition(out, class_generator)
        out.put_line('')
        self.__generate_raw_copy_constructor_definition(out, class_generator)
        out.put_line('')
        self.__generate_destructor(out, class_generator)
        out.put_line('')
        self.__generate_assignment_operator(out, class_generator)
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
        class_generator.capi_generator.add_c_function(
            class_generator.full_name_array,
            'void',
            class_generator.add_ref_method,
            'void* object_pointer',
            add_ref_c_function_body)

        release_c_function_body = FileGenerator(None)
        with IndentScope(release_c_function_body):
            release_call = 'intrusive_ptr_release({to_impl_cast});'.format(
                to_impl_cast=ThisArgumentGenerator(class_generator).c_2_implementation()
            )
            self.finish_method_exception_traits.generate_implementation_call(
                release_c_function_body, BuiltinTypeGenerator('void'), [release_call])
        class_generator.capi_generator.add_c_function(
            class_generator.full_name_array,
            'void',
            class_generator.release_method,
            'void* object_pointer',
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
