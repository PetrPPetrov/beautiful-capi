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
from FileGenerator import FileGenerator, IndentScope
from BuiltinTypeGenerator import BuiltinTypeGenerator
from Helpers import if_required_then_add_empty_line
from Callbacks import get_all_methods


def get_copy_callback_name(class_generator):
    return '{0}_copy_callback'.format(class_generator.base_class_generator.c_name)


def generate_copy_callback_declaration(first_flag, out: FileGenerator, class_generator, definition) -> bool:
    first_flag = if_required_then_add_empty_line(first_flag, out)
    argument_list = ['void* object_pointer']
    class_generator.callback_lifecycle_traits.init_method_exception_traits.modify_c_arguments(argument_list)
    arguments = ', '.join(argument_list)
    out.put_line('template<typename ImplementationClass>')
    out.put_line('void* {top_ns}_API_CONVENTION {name}({arguments}){semicolon}'.format(
        top_ns=class_generator.full_name_array[0].upper(),
        name=get_copy_callback_name(class_generator),
        arguments=arguments,
        semicolon='' if definition else ';'))
    if definition:
        class_generator.capi_generator.add_c_function_pointer(
            class_generator.full_name_array[:-1],
            'void*', class_generator.base_class_generator.copy_callback_type, arguments)
    return first_flag


def generate_copy_callback_definition(first_flag, out: FileGenerator, class_generator) -> bool:
    first_flag = generate_copy_callback_declaration(first_flag, out, class_generator, True)
    with IndentScope(out):
        copy_instructions = ['ImplementationClass* self = static_cast<ImplementationClass*>(object_pointer);',
                             'return new ImplementationClass(*self);']
        class_generator.callback_lifecycle_traits.init_method_exception_traits.generate_callback_call(
            out, BuiltinTypeGenerator('void*'), copy_instructions)
    return first_flag


def get_delete_callback_name(class_generator):
    return '{0}_delete_callback'.format(class_generator.base_class_generator.c_name)


def generate_delete_callback_declaration(first_flag, out: FileGenerator, class_generator, definition) -> bool:
    first_flag = if_required_then_add_empty_line(first_flag, out)
    argument_list = ['void* object_pointer']
    class_generator.callback_lifecycle_traits.finish_method_exception_traits.modify_c_arguments(argument_list)
    arguments = ', '.join(argument_list)
    out.put_line('template<typename ImplementationClass>')
    out.put_line('void {top_ns}_API_CONVENTION {name}({arguments}){semicolon}'.format(
        top_ns=class_generator.full_name_array[0].upper(),
        name=get_delete_callback_name(class_generator),
        arguments=arguments,
        semicolon='' if definition else ';'))
    if definition:
        class_generator.capi_generator.add_c_function_pointer(
            class_generator.full_name_array[:-1],
            'void', class_generator.base_class_generator.delete_callback_type, arguments)
    return first_flag


def generate_delete_callback_definition(first_flag, out: FileGenerator, class_generator) -> bool:
    first_flag = generate_delete_callback_declaration(first_flag, out, class_generator, True)
    with IndentScope(out):
        delete_instructions = ['ImplementationClass* self = static_cast<ImplementationClass*>(object_pointer);',
                               'delete self;']
        class_generator.callback_lifecycle_traits.finish_method_exception_traits.generate_callback_call(
            out, BuiltinTypeGenerator('void'), delete_instructions)
    return first_flag


def generate_callbacks_declarations_for_copy_semantic(first_flag, out: FileGenerator, class_generator) -> bool:
    first_flag = generate_copy_callback_declaration(first_flag, out, class_generator, False)
    return generate_delete_callback_declaration(first_flag, out, class_generator, False)


def generate_callbacks_definitions_for_copy_semantic(first_flag, out: FileGenerator, class_generator) -> bool:
    first_flag = generate_copy_callback_definition(first_flag, out, class_generator)
    return generate_delete_callback_definition(first_flag, out, class_generator)


def get_add_ref_callback_name(class_generator):
    return '{0}_add_ref_callback'.format(class_generator.base_class_generator.c_name)


def generate_add_ref_callback_declaration(first_flag, out: FileGenerator, class_generator, definition) -> bool:
    first_flag = if_required_then_add_empty_line(first_flag, out)
    argument_list = ['void* object_pointer']
    class_generator.callback_lifecycle_traits.init_method_exception_traits.modify_c_arguments(argument_list)
    arguments = ', '.join(argument_list)
    out.put_line('template<typename ImplementationClass>')
    out.put_line('void {top_ns}_API_CONVENTION {name}({arguments}){semicolon}'.format(
        top_ns=class_generator.full_name_array[0].upper(),
        name=get_add_ref_callback_name(class_generator),
        arguments=arguments,
        semicolon='' if definition else ';'))
    if definition:
        class_generator.capi_generator.add_c_function_pointer(
            class_generator.full_name_array[:-1],
            'void', class_generator.base_class_generator.add_ref_callback_type, arguments)
    return first_flag


def generate_add_ref_callback_definition(first_flag, out: FileGenerator, class_generator) -> bool:
    first_flag = generate_add_ref_callback_declaration(first_flag, out, class_generator, True)
    with IndentScope(out):
        add_ref_instructions = ['ImplementationClass* self = static_cast<ImplementationClass*>(object_pointer);',
                                'intrusive_ptr_add_ref(self);']
        class_generator.callback_lifecycle_traits.init_method_exception_traits.generate_callback_call(
            out, BuiltinTypeGenerator('void'), add_ref_instructions)
    return first_flag


def get_release_callback_name(class_generator):
    return '{0}_release_callback'.format(class_generator.base_class_generator.c_name)


def generate_release_callback_declaration(first_flag, out: FileGenerator, class_generator, definition) -> bool:
    first_flag = if_required_then_add_empty_line(first_flag, out)
    argument_list = ['void* object_pointer']
    class_generator.callback_lifecycle_traits.finish_method_exception_traits.modify_c_arguments(argument_list)
    arguments = ', '.join(argument_list)
    out.put_line('template<typename ImplementationClass>')
    out.put_line('void {top_ns}_API_CONVENTION {name}({arguments}){semicolon}'.format(
        top_ns=class_generator.full_name_array[0].upper(),
        name=get_release_callback_name(class_generator),
        arguments=arguments,
        semicolon='' if definition else ';'))
    if definition:
        class_generator.capi_generator.add_c_function_pointer(
            class_generator.full_name_array[:-1],
            'void', class_generator.base_class_generator.release_callback_type, arguments)
    return first_flag


def generate_release_callback_definition(first_flag, out: FileGenerator, class_generator) -> bool:
    first_flag = generate_release_callback_declaration(first_flag, out, class_generator, True)
    with IndentScope(out):
        release_instructions = ['ImplementationClass* self = static_cast<ImplementationClass*>(object_pointer);',
                                'intrusive_ptr_release(self);']
        class_generator.callback_lifecycle_traits.finish_method_exception_traits.generate_callback_call(
            out, BuiltinTypeGenerator('void'), release_instructions)
    return first_flag


def generate_callbacks_declarations_for_reference_counted_semantic(
        first_flag, out: FileGenerator, class_generator) -> bool:
    first_flag = generate_add_ref_callback_declaration(first_flag, out, class_generator, False)
    return generate_release_callback_declaration(first_flag, out, class_generator, False)


def generate_callbacks_definitions_for_reference_counted_semantic(
        first_flag, out: FileGenerator, class_generator) -> bool:
    first_flag = generate_add_ref_callback_definition(first_flag, out, class_generator)
    return generate_release_callback_definition(first_flag, out, class_generator)


def get_method_callback_name(method_generator):
    return '{callback_name}_{method_name}_callback'.format(
        callback_name=method_generator.parent_class_generator.c_name,
        method_name=method_generator.c_name)


def generate_method_callback_declaration(first_flag, out: FileGenerator, cur_method_generator) -> bool:
    first_flag = if_required_then_add_empty_line(first_flag, out)

    c_argument_declaration_list = [
        arg_gen.c_argument_declaration() for arg_gen in cur_method_generator.c_arguments_list]
    cur_method_generator.exception_traits.modify_c_arguments(c_argument_declaration_list)

    out.put_line('template<typename ImplementationClass>')
    out.put_line('{return_type} {top_ns}_API_CONVENTION {callback_name}({arguments});'.format(
        top_ns=cur_method_generator.parent_class_generator.full_name_array[0].upper(),
        return_type=cur_method_generator.return_type_generator.c_argument_declaration(),
        callback_name=get_method_callback_name(cur_method_generator),
        arguments=', '.join(c_argument_declaration_list)
    ))
    return first_flag


def add_method_callback_typedef(cur_method_generator):
    c_argument_declaration_list = [
        arg_gen.c_argument_declaration() for arg_gen in cur_method_generator.c_arguments_list]
    cur_method_generator.exception_traits.modify_c_arguments(c_argument_declaration_list)

    cur_method_generator.parent_class_generator.capi_generator.add_c_function_pointer(
        cur_method_generator.parent_class_generator.full_name_array[:-1],
        cur_method_generator.return_type_generator.c_argument_declaration(),
        cur_method_generator.callback_type,
        ', '.join(c_argument_declaration_list))


def generate_method_callback_definition(first_flag, out: FileGenerator, cur_method_generator) -> bool:
    add_method_callback_typedef(cur_method_generator)
    first_flag = if_required_then_add_empty_line(first_flag, out)

    c_argument_declaration_list = [
        arg_gen.c_argument_declaration() for arg_gen in cur_method_generator.c_arguments_list]
    cur_method_generator.exception_traits.modify_c_arguments(c_argument_declaration_list)

    out.put_line('template<typename ImplementationClass>')
    out.put_line('{return_type} {top_ns}_API_CONVENTION {callback_name}({arguments})'.format(
        top_ns=cur_method_generator.parent_class_generator.full_name_array[0].upper(),
        return_type=cur_method_generator.return_type_generator.c_argument_declaration(),
        callback_name=get_method_callback_name(cur_method_generator),
        arguments=', '.join(c_argument_declaration_list)
    ))
    with IndentScope(out):
        out.put_line(
            '{const}ImplementationClass* self = static_cast<ImplementationClass*>(object_pointer);'.format(
                const='const ' if cur_method_generator.method_object.const else ''
            ))
        wrap_arg_call = [arg_gen.c_2_wrap() for arg_gen in cur_method_generator.argument_generators]
        method_call = 'self->{0}({1})'.format(
            cur_method_generator.wrap_name,
            ', '.join(wrap_arg_call))
        calling_instructions, return_expression = cur_method_generator.return_type_generator.wrap_2_c_var(
            '', method_call)
        if return_expression:
            calling_instructions.append('return {0};'.format(return_expression))

        cur_method_generator.exception_traits.generate_callback_call(
            out,
            cur_method_generator.return_type_generator,
            calling_instructions)
    return first_flag


def generate_create_callback_declaration(first_flag, out: FileGenerator, class_generator):
    first_flag = if_required_then_add_empty_line(first_flag, out)

    out.put_line('template<typename ImplementationClass>')
    out.put_line(
        'inline {return_type} create_callback_for_{class_suffix}(ImplementationClass* implementation_class);'.format(
            return_type=class_generator.full_wrap_name,
            class_suffix=class_generator.base_class_generator.c_name))

    out.put_line('')

    out.put_line('template<typename ImplementationClass>')
    out.put_line(
        'inline {return_type} create_callback_for_{class_suffix}(ImplementationClass& implementation_class);'.format(
            return_type=class_generator.full_wrap_name,
            class_suffix=class_generator.base_class_generator.c_name))

    return first_flag


def generate_set_callbacks_for_copy_semantic(out: FileGenerator, class_generator):
    out.put_line(
        'result.SetCFunctionForCopy({0}<ImplementationClass>);'.format(get_copy_callback_name(class_generator)))
    out.put_line(
        'result.SetCFunctionForDelete({0}<ImplementationClass>);'.format(get_delete_callback_name(class_generator)))


def generate_set_callbacks_for_reference_counted_semantic(out: FileGenerator, class_generator):
    out.put_line(
        'result.SetCFunctionForAddRef({0}<ImplementationClass>);'.format(get_add_ref_callback_name(class_generator)))
    out.put_line(
        'result.SetCFunctionForRelease({0}<ImplementationClass>);'.format(get_release_callback_name(class_generator)))


def generate_set_callback_for_method(out: FileGenerator, cur_method_generator):
    out.put_line('result.SetCFunctionFor{0}({1}<ImplementationClass>);'.format(
        cur_method_generator.name,
        get_method_callback_name(cur_method_generator)))


def generate_create_callback_from_reference(out: FileGenerator, class_generator):
    out.put_line('template<typename ImplementationClass>')
    out.put_line(
        'inline {return_type} create_callback_for_{class_suffix}(ImplementationClass& implementation_class)'.format(
            return_type=class_generator.full_wrap_name,
            class_suffix=class_generator.base_class_generator.c_name))
    with IndentScope(out):
        out.put_line('return create_callback_for_{class_suffix}(&implementation_class);'.format(
            class_suffix=class_generator.base_class_generator.c_name))


def generate_set_callbacks_for_lifecycle(out: FileGenerator, callback, class_generator):
    if callback.lifecycle == TLifecycle.copy_semantic:
        generate_set_callbacks_for_copy_semantic(out, class_generator)
    elif callback.lifecycle == TLifecycle.reference_counted:
        generate_set_callbacks_for_reference_counted_semantic(out, class_generator)


def generate_create_callback_definition(first_flag, out: FileGenerator, class_generator):
    first_flag = if_required_then_add_empty_line(first_flag, out)

    callback = class_generator.base_class_generator.class_object.callbacks[0]
    out.put_line('template<typename ImplementationClass>')
    out.put_line(
        '{return_type} create_callback_for_{class_suffix}(ImplementationClass* implementation_class)'.format(
            return_type=class_generator.full_wrap_name,
            class_suffix=class_generator.base_class_generator.c_name))
    with IndentScope(out):
        out.put_line('{callback_class} result;'.format(callback_class=class_generator.full_wrap_name))

        generate_set_callbacks_for_lifecycle(out, callback, class_generator)
        for cur_method_generator in get_all_methods(class_generator.base_class_generator):
            generate_set_callback_for_method(out, cur_method_generator)

        out.put_line('result.SetObjectPointer(implementation_class);')
        out.put_line('return result;')

    out.put_line('')

    generate_create_callback_from_reference(out, class_generator)

    return first_flag


def generate_callbacks_on_client_side_declarations(out: FileGenerator, class_generator):
    if class_generator.is_callback:
        out.put_line('')
        generate_create_callback_declaration(True, out, class_generator)


def generate_callback_declarations_for_lifecycle(out: FileGenerator, callback, class_generator, first_flag):
    if callback.lifecycle == TLifecycle.copy_semantic:
        first_flag = generate_callbacks_declarations_for_copy_semantic(first_flag, out, class_generator)
    elif callback.lifecycle == TLifecycle.reference_counted:
        first_flag = generate_callbacks_declarations_for_reference_counted_semantic(first_flag, out, class_generator)
    return first_flag


def generate_callback_definitions_for_lifecycle(out: FileGenerator, callback, class_generator, first_flag):
    first_flag = generate_create_callback_definition(first_flag, out, class_generator)
    if callback.lifecycle == TLifecycle.copy_semantic:
        first_flag = generate_callbacks_definitions_for_copy_semantic(first_flag, out, class_generator)
    elif callback.lifecycle == TLifecycle.reference_counted:
        first_flag = generate_callbacks_definitions_for_reference_counted_semantic(first_flag, out, class_generator)
    return first_flag


def generate_callbacks_on_client_side_definitions(out: FileGenerator, class_generator):
    if class_generator.is_callback:
        callback = class_generator.base_class_generator.class_object.callbacks[0]
        out.put_line('')
        out.put_line(class_generator.parent_namespace.one_line_namespace_begin)
        out.put_line('')
        first_flag = True

        first_flag = generate_callback_declarations_for_lifecycle(out, callback, class_generator, first_flag)

        for cur_method_generator in get_all_methods(class_generator.base_class_generator):
            first_flag = generate_method_callback_declaration(first_flag, out, cur_method_generator)

        first_flag = generate_callback_definitions_for_lifecycle(out, callback, class_generator, first_flag)

        for cur_method_generator in get_all_methods(class_generator.base_class_generator):
            first_flag = generate_method_callback_definition(first_flag, out, cur_method_generator)

        out.put_line('')
        out.put_line(class_generator.parent_namespace.one_line_namespace_end)
