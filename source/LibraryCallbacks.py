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
from FileGenerator import FileGenerator, IndentScope, Unindent, Indent
from BuiltinTypeGenerator import BuiltinTypeGenerator
from Callbacks import get_callback_impl_name, get_all_methods


def generate_copy_semantic_callback_members(out: FileGenerator, callback_names, class_generator):
    out.put_line('{0} copy_callback;'.format(class_generator.base_class_generator.copy_callback_type))
    callback_names.append('copy_callback')
    out.put_line('{0} delete_callback;'.format(class_generator.base_class_generator.delete_callback_type))
    callback_names.append('delete_callback')


def generate_reference_counted_semantic_callback_members(out: FileGenerator, callback_names, class_generator):
    out.put_line('{0} add_ref_callback;'.format(class_generator.base_class_generator.add_ref_callback_type))
    callback_names.append('add_ref_callback')
    out.put_line('{0} release_callback;'.format(class_generator.base_class_generator.release_callback_type))
    callback_names.append('release_callback')


def generate_lifecycle_callback_members(out: FileGenerator, callback_names, class_generator, callback):
    if callback.lifecycle == TLifecycle.copy_semantic:
        generate_copy_semantic_callback_members(out, callback_names, class_generator)
    elif callback.lifecycle == TLifecycle.reference_counted:
        generate_reference_counted_semantic_callback_members(out, callback_names, class_generator)


def generate_callback_member(out: FileGenerator, callback_names, cur_method_generator):
    out.put_line('{callback_type} {method_name}_callback;'.format(
        callback_type=cur_method_generator.callback_type,
        method_name=cur_method_generator.c_name
    ))
    callback_names.append('{method_name}_callback'.format(method_name=cur_method_generator.c_name))


def generate_callback_members(out: FileGenerator, callback_names, class_generator):
    for cur_method_generator in get_all_methods(class_generator.base_class_generator):
        generate_callback_member(out, callback_names, cur_method_generator)


def generate_callback_implementation_default_constructor(out: FileGenerator, callback_names, impl_class_name):
    out.put_line('{0}() :'.format(impl_class_name))
    with Indent(out):
        for callback_name in callback_names:
            out.put_line('{callback_name}(0),'.format(callback_name=callback_name))
        out.put_line('mObject(0)')
    with IndentScope(out):
        pass


def generate_callback_implementation_copy_constructor_body_copy(out: FileGenerator, class_generator):
    out.put_line('if (mObject && copy_callback)')
    with IndentScope(out):
        exception_traits = class_generator.callback_lifecycle_traits.init_method_exception_traits
        return_expression = exception_traits.generate_c_call_from_impl(
            out, BuiltinTypeGenerator('void*'), 'copy_callback', ['mObject'])
        if return_expression:
            out.put_line('mObject = {return_expression};'.format(return_expression=return_expression))


def generate_callback_implementation_copy_constructor_add_ref(out: FileGenerator, class_generator):
    out.put_line('if (mObject && add_ref_callback)')
    with IndentScope(out):
        exception_traits = class_generator.callback_lifecycle_traits.init_method_exception_traits
        return_expression = exception_traits.generate_c_call_from_impl(
            out, BuiltinTypeGenerator('void'), 'add_ref_callback', ['mObject'])
        if return_expression:
            out.put_line('{return_expression};'.format(return_expression=return_expression))


def generate_callback_implementation_copy_constructor_body(out: FileGenerator, callback, class_generator):
    if callback.lifecycle == TLifecycle.copy_semantic:
        generate_callback_implementation_copy_constructor_body_copy(out, class_generator)
    elif callback.lifecycle == TLifecycle.reference_counted:
        generate_callback_implementation_copy_constructor_add_ref(out, class_generator)


def generate_callback_implementation_copy_constructor(
        out: FileGenerator, callback, callback_names, impl_class_name, class_generator):
    out.put_line('{0}(const {0}& other) :'.format(impl_class_name))
    with Indent(out):
        for callback_name in callback_names:
            out.put_line('{0}(other.{0}),'.format(callback_name))
        out.put_line('mObject(other.mObject)')
    with IndentScope(out):
        generate_callback_implementation_copy_constructor_body(out, callback, class_generator)


def generate_callback_implementation_destructor_body(out: FileGenerator, class_generator, callback_function_name):
    with IndentScope(out):
        out.put_line('if (mObject && {0})'.format(callback_function_name))
        with IndentScope(out):
            exception_traits = class_generator.callback_lifecycle_traits.finish_method_exception_traits
            return_expression = exception_traits.generate_c_call_from_impl(
                out, BuiltinTypeGenerator('void'), callback_function_name, ['mObject'])
            if return_expression:
                out.put_line('{return_expression};'.format(return_expression=return_expression))


def generate_callback_implementation_destructor(out: FileGenerator, callback, impl_class_name, class_generator):
    if callback.lifecycle == TLifecycle.copy_semantic:
        out.put_line('~{0}()'.format(impl_class_name))
        generate_callback_implementation_destructor_body(out, class_generator, 'delete_callback')
    elif callback.lifecycle == TLifecycle.reference_counted:
        out.put_line('~{0}()'.format(impl_class_name))
        generate_callback_implementation_destructor_body(out, class_generator, 'release_callback')


def generate_callback_implementation_set_object_pointer_method(out: FileGenerator, callback, class_generator):
    out.put_line('void SetObjectPointer(void* object_pointer)')
    with IndentScope(out):
        out.put_line('mObject = object_pointer;')
        generate_callback_implementation_copy_constructor_body(out, callback, class_generator)


def generate_callback_implementation_get_object_pointer_method(out: FileGenerator):
    out.put_line('void* GetObjectPointer() const')
    with IndentScope(out):
        out.put_line('return mObject;')


def generate_callback_implementation_set_c_functions_for_copy_semantic(out: FileGenerator, class_generator):
    out.put_line('void SetCFunctionForCopy({callback_type} c_function_pointer)'.format(
        callback_type=class_generator.base_class_generator.copy_callback_type))
    with IndentScope(out):
        out.put_line('copy_callback = c_function_pointer;')
    out.put_line('void SetCFunctionForDelete({callback_type} c_function_pointer)'.format(
        callback_type=class_generator.base_class_generator.delete_callback_type))
    with IndentScope(out):
        out.put_line('delete_callback = c_function_pointer;')


def generate_callback_implementation_set_c_functions_for_add_ref_semantic(out: FileGenerator, class_generator):
    out.put_line('void SetCFunctionForAddRef({callback_type} c_function_pointer)'.format(
        callback_type=class_generator.base_class_generator.add_ref_callback_type))
    with IndentScope(out):
        out.put_line('add_ref_callback = c_function_pointer;')
    out.put_line('void SetCFunctionForRelease({callback_type} c_function_pointer)'.format(
        callback_type=class_generator.base_class_generator.release_callback_type))
    with IndentScope(out):
        out.put_line('release_callback = c_function_pointer;')


def generate_callback_implementation_set_c_functions_for_lifecycle(out: FileGenerator, callback, class_generator):
    if callback.lifecycle == TLifecycle.copy_semantic:
        generate_callback_implementation_set_c_functions_for_copy_semantic(out, class_generator)
    elif callback.lifecycle == TLifecycle.reference_counted:
        generate_callback_implementation_set_c_functions_for_add_ref_semantic(out, class_generator)


def generate_callback_implementation_set_c_function_for_method(out: FileGenerator, cur_method_generator):
    out.put_line('void SetCFunctionFor{method_name}({callback_type} c_function_pointer)'.format(
        method_name=cur_method_generator.name, callback_type=cur_method_generator.callback_type))
    with IndentScope(out):
        out.put_line('{method_name}_callback = c_function_pointer;'.format(
            method_name=cur_method_generator.c_name
        ))


def generate_callback_implementation_set_c_function_for_methods(out: FileGenerator, class_generator):
    for cur_method_generator in get_all_methods(class_generator.base_class_generator):
        generate_callback_implementation_set_c_function_for_method(out, cur_method_generator)


def generate_callback_implementation_for_method(out: FileGenerator, cur_method_gen):
    args = [arg_gen.snippet_implementation_declaration() for arg_gen in cur_method_gen.argument_generators]
    out.put_line('{return_type} {method_name}({arguments}){const}'.format(
        return_type=cur_method_gen.return_type_generator.snippet_implementation_declaration(),
        method_name=cur_method_gen.name,
        arguments=', '.join(args),
        const=' const' if cur_method_gen.method_object.const else ''
    ))
    with IndentScope(out):
        arguments_call = [arg_gen.implementation_2_c() for arg_gen in cur_method_gen.c_arguments_list]
        callback_name = '{method_name}_callback'.format(method_name=cur_method_gen.c_name)
        return_expression = cur_method_gen.exception_traits.generate_c_call_from_impl(
            out, cur_method_gen.return_type_generator, callback_name, arguments_call)
        out.put_return_cpp_statement(return_expression)


def generate_callback_implementation_for_methods(out: FileGenerator, class_generator):
    for cur_method_gen in get_all_methods(class_generator.base_class_generator):
        generate_callback_implementation_for_method(out, cur_method_gen)


def generate_callback_implementation_body(out: FileGenerator, callback, class_generator, impl_class_name):
    out.put_line('void* mObject;')
    callback_names = []
    generate_lifecycle_callback_members(out, callback_names, class_generator, callback)
    generate_callback_members(out, callback_names, class_generator)
    with Unindent(out):
        out.put_line('public:')
    generate_callback_implementation_default_constructor(out, callback_names, impl_class_name)
    generate_callback_implementation_copy_constructor(out, callback, callback_names, impl_class_name, class_generator)
    generate_callback_implementation_destructor(out, callback, impl_class_name, class_generator)
    generate_callback_implementation_set_object_pointer_method(out, callback, class_generator)
    generate_callback_implementation_get_object_pointer_method(out)
    generate_callback_implementation_set_c_functions_for_lifecycle(out, callback, class_generator)
    generate_callback_implementation_set_c_function_for_methods(out, class_generator)
    generate_callback_implementation_for_methods(out, class_generator)


def generate_callbacks_on_library_side(class_generator, capi_generator):
    if class_generator.is_callback:
        callback = class_generator.base_class_generator.class_object.callbacks[0]

        if callback.implementation_class_header_filled:
            capi_generator.additional_includes.include_user_header(callback.implementation_class_header)

        callback_impl = FileGenerator(None)
        callback_impl.put_line(class_generator.parent_namespace.one_line_namespace_begin)
        callback_impl.put_line('')

        impl_class_name = get_callback_impl_name(class_generator.base_class_generator)

        callback_impl.put_line('class {0} : public {1}'.format(
            impl_class_name, callback.implementation_class_name))
        with IndentScope(callback_impl, '};'):
            generate_callback_implementation_body(callback_impl, callback, class_generator, impl_class_name)

        callback_impl.put_line('')
        callback_impl.put_line(class_generator.parent_namespace.one_line_namespace_end)
        capi_generator.callback_implementations.append(callback_impl)
