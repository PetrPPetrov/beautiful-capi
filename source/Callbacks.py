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


from Parser import TClass, TConstructor, TMethod, TArgument, TLifecycle
from NamespaceGenerator import NamespaceGenerator
from FileGenerator import FileGenerator, IndentScope, Unindent, Indent
from Helpers import if_required_then_add_empty_line


def get_callback_impl_name(class_generator) -> str:
    return '{prefix}{name}Impl'.format(
        prefix=class_generator.params.autogen_prefix_for_internal_callback_implementation,
        name=class_generator.name)


def get_callback_full_impl_name(class_generator) -> str:
    return '::'.join([class_generator.parent_namespace.full_name, get_callback_impl_name(class_generator)])


def generate_callback_class(class_generator):
    new_callback_class = TClass()
    new_callback_class.name = class_generator.name + 'Callback'
    new_callback_class.base = class_generator.full_name
    new_callback_class.lifecycle = class_generator.class_object.lifecycle
    new_callback_class.implementation_class_name = get_callback_full_impl_name(class_generator)
    new_callback_class.implementation_class_name_filled = True
    return new_callback_class


def generate_default_constructor(new_callback_class):
    new_default_constructor = TConstructor()
    new_default_constructor.name = 'Default'
    new_callback_class.constructors.append(new_default_constructor)


def generate_set_c_function_for_copy(class_generator, new_callback_class):
    set_copy_c_function = TMethod()
    set_copy_c_function.name = 'SetCFunctionForCopy'
    set_copy_c_function.arguments.append(TArgument())
    set_copy_c_function.arguments[0].type_name = class_generator.copy_callback_type
    set_copy_c_function.arguments[0].name = 'c_function_pointer'
    set_copy_c_function.noexcept = True
    set_copy_c_function.noexcept_filled = True
    new_callback_class.methods.append(set_copy_c_function)


def generate_set_c_function_for_delete(class_generator, new_callback_class):
    set_delete_c_function = TMethod()
    set_delete_c_function.name = 'SetCFunctionForDelete'
    set_delete_c_function.arguments.append(TArgument())
    set_delete_c_function.arguments[0].type_name = class_generator.delete_callback_type
    set_delete_c_function.arguments[0].name = 'c_function_pointer'
    set_delete_c_function.noexcept = True
    set_delete_c_function.noexcept_filled = True
    new_callback_class.methods.append(set_delete_c_function)


def generate_set_c_functions_for_copy_semantic(class_generator, new_callback_class):
    generate_set_c_function_for_copy(class_generator, new_callback_class)
    generate_set_c_function_for_delete(class_generator, new_callback_class)


def generate_set_c_function_for_add_ref(class_generator, new_callback_class):
    set_add_ref_c_function = TMethod()
    set_add_ref_c_function.name = 'SetCFunctionForAddRef'
    set_add_ref_c_function.arguments.append(TArgument())
    set_add_ref_c_function.arguments[0].type_name = class_generator.add_ref_callback_type
    set_add_ref_c_function.arguments[0].name = 'c_function_pointer'
    set_add_ref_c_function.noexcept = True
    set_add_ref_c_function.noexcept_filled = True
    new_callback_class.methods.append(set_add_ref_c_function)


def generate_set_c_function_for_release(class_generator, new_callback_class):
    set_release_c_function = TMethod()
    set_release_c_function.name = 'SetCFunctionForRelease'
    set_release_c_function.arguments.append(TArgument())
    set_release_c_function.arguments[0].type_name = class_generator.release_callback_type
    set_release_c_function.arguments[0].name = 'c_function_pointer'
    set_release_c_function.noexcept = True
    set_release_c_function.noexcept_filled = True
    new_callback_class.methods.append(set_release_c_function)


def generate_set_c_functions_for_reference_counted_semantic(class_generator, new_callback_class):
    generate_set_c_function_for_add_ref(class_generator, new_callback_class)
    generate_set_c_function_for_release(class_generator, new_callback_class)


def generate_set_object_pointer(new_callback_class):
    set_object_pointer_method = TMethod()
    set_object_pointer_method.name = 'SetObjectPointer'
    set_object_pointer_method.arguments.append(TArgument())
    set_object_pointer_method.arguments[0].type_name = 'void*'
    set_object_pointer_method.arguments[0].name = 'custom_object'
    set_object_pointer_method.noexcept = True
    set_object_pointer_method.noexcept_filled = True
    new_callback_class.methods.append(set_object_pointer_method)


def generate_get_object_pointer(new_callback_class):
    get_object_pointer_method = TMethod()
    get_object_pointer_method.name = 'GetObjectPointer'
    get_object_pointer_method.return_type = 'void*'
    get_object_pointer_method.noexcept = True
    get_object_pointer_method.noexcept_filled = True
    get_object_pointer_method.const = True
    new_callback_class.methods.append(get_object_pointer_method)


def generate_callback_for_method(cur_method_generator, new_callback_class):
    set_c_function_method = TMethod()
    set_c_function_method.name = 'SetCFunctionFor{0}'.format(cur_method_generator.name)
    set_c_function_method.arguments.append(TArgument())
    set_c_function_method.arguments[0].type_name = cur_method_generator.callback_type
    set_c_function_method.arguments[0].name = 'c_function_pointer'
    set_c_function_method.noexcept = True
    set_c_function_method.noexcept_filled = True
    new_callback_class.methods.append(set_c_function_method)


def get_all_methods(class_generator) -> []:
    while class_generator:
        for cur_method_generator in class_generator.method_generators:
            yield cur_method_generator
        class_generator = class_generator.base_class_generator


def generate_set_c_functions_for_lifecycle(callback, class_generator, new_callback_class):
    if callback.lifecycle == TLifecycle.copy_semantic:
        generate_set_c_functions_for_copy_semantic(class_generator, new_callback_class)
    elif callback.lifecycle == TLifecycle.reference_counted:
        generate_set_c_functions_for_reference_counted_semantic(class_generator, new_callback_class)


def process_class(class_generator):
    if class_generator.class_object.callbacks:
        callback = class_generator.class_object.callbacks[0]

        new_callback_class = generate_callback_class(class_generator)

        generate_default_constructor(new_callback_class)
        generate_set_c_functions_for_lifecycle(callback, class_generator, new_callback_class)
        generate_set_object_pointer(new_callback_class)
        generate_get_object_pointer(new_callback_class)

        for cur_method_generator in get_all_methods(class_generator):
            generate_callback_for_method(cur_method_generator, new_callback_class)

        class_generator.parent_namespace.namespace_object.classes.append(new_callback_class)


def process_namespace(namespace_generator: NamespaceGenerator):
    for nested_namespace in namespace_generator.nested_namespaces:
        process_namespace(nested_namespace)
    for class_generator in namespace_generator.classes:
        process_class(class_generator)


def process(namespace_generators: [NamespaceGenerator]):
    for cur_namespace in namespace_generators:
        process_namespace(cur_namespace)


def get_copy_callback_name(class_generator):
    return '{0}_copy_callback'.format(class_generator.base_class_generator.c_name)


def generate_copy_callback_declaration(first_flag, class_generator, out) -> bool:
    first_flag = if_required_then_add_empty_line(first_flag, out)
    out.put_line('template<typename ImplementationClass>')
    out.put_line('void* {top_ns}_API_CONVENTION {name}(void* object_pointer);'.format(
        top_ns=class_generator.full_name_array[0].upper(),
        name=get_copy_callback_name(class_generator)))
    return first_flag


def add_copy_callback_typedef(class_generator):
    class_generator.capi_generator.add_c_function_pointer(
        class_generator.full_name_array,
        'void*', class_generator.copy_callback_type, 'void* object_pointer')


def generate_copy_callback_definition(first_flag, class_generator, out) -> bool:
    add_copy_callback_typedef(class_generator)
    first_flag = if_required_then_add_empty_line(first_flag, out)
    out.put_line('template<typename ImplementationClass>')
    out.put_line('void* {top_ns}_API_CONVENTION {name}(void* object_pointer)'.format(
        top_ns=class_generator.full_name_array[0].upper(),
        name=get_copy_callback_name(class_generator)))
    with IndentScope(out):
        out.put_line('ImplementationClass* self = static_cast<ImplementationClass*>(object_pointer);')
        out.put_line('return new ImplementationClass(*self);')
    return first_flag


def get_delete_callback_name(class_generator):
    return '{0}_delete_callback'.format(class_generator.base_class_generator.c_name)


def generate_delete_callback_declaration(first_flag, class_generator, out) -> bool:
    first_flag = if_required_then_add_empty_line(first_flag, out)
    out.put_line('template<typename ImplementationClass>')
    out.put_line('void {top_ns}_API_CONVENTION {name}(void* object_pointer);'.format(
        top_ns=class_generator.full_name_array[0].upper(),
        name=get_delete_callback_name(class_generator)))
    return first_flag


def add_delete_callback_typedef(class_generator):
    class_generator.capi_generator.add_c_function_pointer(
        class_generator.full_name_array,
        'void', class_generator.delete_callback_type, 'void* object_pointer')


def generate_delete_callback_definition(first_flag, class_generator, out) -> bool:
    add_delete_callback_typedef(class_generator)
    first_flag = if_required_then_add_empty_line(first_flag, out)
    out.put_line('template<typename ImplementationClass>')
    out.put_line('void {top_ns}_API_CONVENTION {name}(void* object_pointer)'.format(
        top_ns=class_generator.full_name_array[0].upper(),
        name=get_delete_callback_name(class_generator)))
    with IndentScope(out):
        out.put_line('ImplementationClass* self = static_cast<ImplementationClass*>(object_pointer);')
        out.put_line('delete self;')
    return first_flag


def generate_callbacks_declarations_for_copy_semantic(first_flag, class_generator, out) -> bool:
    first_flag = generate_copy_callback_declaration(first_flag, class_generator, out)
    return generate_delete_callback_declaration(first_flag, class_generator, out)


def generate_callbacks_definitions_for_copy_semantic(first_flag, class_generator, out) -> bool:
    first_flag = generate_copy_callback_definition(first_flag, class_generator, out)
    return generate_delete_callback_definition(first_flag, class_generator, out)


def get_add_ref_callback_name(class_generator):
    return '{0}_add_ref_callback'.format(class_generator.base_class_generator.c_name)


def generate_add_ref_callback_declaration(first_flag, class_generator, out) -> bool:
    first_flag = if_required_then_add_empty_line(first_flag, out)
    out.put_line('template<typename ImplementationClass>')
    out.put_line('void {top_ns}_API_CONVENTION {name}(void* object_pointer);'.format(
        top_ns=class_generator.full_name_array[0].upper(),
        name=get_add_ref_callback_name(class_generator)))
    return first_flag


def add_add_ref_callback_typedef(class_generator):
    class_generator.capi_generator.add_c_function_pointer(
        class_generator.full_name_array,
        'void', class_generator.add_ref_callback_type, 'void* object_pointer')


def generate_add_ref_callback_definition(first_flag, class_generator, out) -> bool:
    add_add_ref_callback_typedef(class_generator)
    first_flag = if_required_then_add_empty_line(first_flag, out)
    out.put_line('template<typename ImplementationClass>')
    out.put_line('void {top_ns}_API_CONVENTION {name}(void* object_pointer)'.format(
        top_ns=class_generator.full_name_array[0].upper(),
        name=get_add_ref_callback_name(class_generator)))
    with IndentScope(out):
        out.put_line('ImplementationClass* self = static_cast<ImplementationClass*>(object_pointer);')
        out.put_line('intrusive_ptr_add_ref(self);')
    return first_flag


def get_release_callback_name(class_generator):
    return '{0}_release_callback'.format(class_generator.base_class_generator.c_name)


def generate_release_callback_declaration(first_flag, class_generator, out) -> bool:
    first_flag = if_required_then_add_empty_line(first_flag, out)
    out.put_line('template<typename ImplementationClass>')
    out.put_line('void {top_ns}_API_CONVENTION {name}(void* object_pointer);'.format(
        top_ns=class_generator.full_name_array[0].upper(),
        name=get_release_callback_name(class_generator)))
    return first_flag


def add_release_callback_typedef(class_generator):
    class_generator.capi_generator.add_c_function_pointer(
        class_generator.full_name_array,
        'void', class_generator.release_callback_type, 'void* object_pointer')


def generate_release_callback_definition(first_flag, class_generator, out) -> bool:
    add_release_callback_typedef(class_generator)
    first_flag = if_required_then_add_empty_line(first_flag, out)
    out.put_line('template<typename ImplementationClass>')
    out.put_line('void {top_ns}_API_CONVENTION {name}(void* object_pointer)'.format(
        top_ns=class_generator.full_name_array[0].upper(),
        name=get_release_callback_name(class_generator)))
    with IndentScope(out):
        out.put_line('ImplementationClass* self = static_cast<ImplementationClass*>(object_pointer);')
        out.put_line('intrusive_ptr_release(self);')
    return first_flag


def generate_callbacks_declarations_for_reference_counted_semantic(first_flag, class_generator, out) -> bool:
    first_flag = generate_add_ref_callback_declaration(first_flag, class_generator, out)
    return generate_release_callback_declaration(first_flag, class_generator, out)


def generate_callbacks_definitions_for_reference_counted_semantic(first_flag, class_generator, out) -> bool:
    first_flag = generate_add_ref_callback_definition(first_flag, class_generator, out)
    return generate_release_callback_definition(first_flag, class_generator, out)


def get_method_callback_name(method_generator):
    return '{callback_name}_{method_name}_callback'.format(
        callback_name=method_generator.parent_class_generator.c_name,
        method_name=method_generator.c_name)


def generate_method_callback_declaration(first_flag, cur_method_generator, out) -> bool:
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
        cur_method_generator.parent_class_generator.full_name_array,
        cur_method_generator.return_type_generator.c_argument_declaration(),
        cur_method_generator.callback_type,
        ', '.join(c_argument_declaration_list))


def generate_method_callback_definition(first_flag, cur_method_generator, out) -> bool:
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


def generate_set_callbacks_for_copy_semantic(class_generator, out):
    out.put_line(
        'result.SetCFunctionForCopy({0}<ImplementationClass>);'.format(get_copy_callback_name(class_generator)))
    out.put_line(
        'result.SetCFunctionForDelete({0}<ImplementationClass>);'.format(get_delete_callback_name(class_generator)))


def generate_set_callbacks_for_reference_counted_semantic(class_generator, out):
    out.put_line(
        'result.SetCFunctionForAddRef({0}<ImplementationClass>);'.format(get_add_ref_callback_name(class_generator)))
    out.put_line(
        'result.SetCFunctionForRelease({0}<ImplementationClass>);'.format(get_release_callback_name(class_generator)))


def generate_set_callback_for_method(cur_method_generator, out):
    out.put_line('result.SetCFunctionFor{0}({1}<ImplementationClass>);'.format(
        cur_method_generator.name,
        get_method_callback_name(cur_method_generator)))


def generate_create_callback_from_reference(class_generator, out):
    out.put_line('template<typename ImplementationClass>')
    out.put_line(
        'inline {return_type} create_callback_for_{class_suffix}(ImplementationClass& implementation_class)'.format(
            return_type=class_generator.full_wrap_name,
            class_suffix=class_generator.base_class_generator.c_name))
    with IndentScope(out):
        out.put_line('return create_callback_for_{class_suffix}(&implementation_class);'.format(
            class_suffix=class_generator.base_class_generator.c_name))


def generate_set_callbacks_for_lifecycle(callback, class_generator, out):
    if callback.lifecycle == TLifecycle.copy_semantic:
        generate_set_callbacks_for_copy_semantic(class_generator, out)
    elif callback.lifecycle == TLifecycle.reference_counted:
        generate_set_callbacks_for_reference_counted_semantic(class_generator, out)


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

        generate_set_callbacks_for_lifecycle(callback, class_generator, out)
        for cur_method_generator in get_all_methods(class_generator.base_class_generator):
            generate_set_callback_for_method(cur_method_generator, out)

        out.put_line('result.SetObjectPointer(implementation_class);')
        out.put_line('return result;')

    out.put_line('')

    generate_create_callback_from_reference(class_generator, out)

    return first_flag


def generate_callbacks_on_client_side_declarations(out: FileGenerator, class_generator):
    if class_generator.base_class_generator and class_generator.base_class_generator.class_object.callbacks:
        out.put_line('')
        generate_create_callback_declaration(True, out, class_generator)


def generate_callback_declarations_for_lifecycle(callback, class_generator, first_flag, out):
    if callback.lifecycle == TLifecycle.copy_semantic:
        first_flag = generate_callbacks_declarations_for_copy_semantic(first_flag, class_generator, out)
    elif callback.lifecycle == TLifecycle.reference_counted:
        first_flag = generate_callbacks_declarations_for_reference_counted_semantic(
            first_flag, class_generator, out)
    return first_flag


def generate_callback_definitions_for_lifecycle(callback, class_generator, first_flag, out):
    first_flag = generate_create_callback_definition(first_flag, out, class_generator)
    if callback.lifecycle == TLifecycle.copy_semantic:
        first_flag = generate_callbacks_definitions_for_copy_semantic(first_flag, class_generator, out)
    elif callback.lifecycle == TLifecycle.reference_counted:
        first_flag = generate_callbacks_definitions_for_reference_counted_semantic(first_flag, class_generator, out)
    return first_flag


def generate_callbacks_on_client_side_definitions(out: FileGenerator, class_generator):
    if class_generator.base_class_generator and class_generator.base_class_generator.class_object.callbacks:
        callback = class_generator.base_class_generator.class_object.callbacks[0]
        out.put_line('')
        out.put_line(class_generator.parent_namespace.one_line_namespace_begin)
        out.put_line('')
        first_flag = True

        first_flag = generate_callback_declarations_for_lifecycle(callback, class_generator, first_flag, out)

        for cur_method_generator in get_all_methods(class_generator.base_class_generator):
            first_flag = generate_method_callback_declaration(first_flag, cur_method_generator, out)

        first_flag = generate_callback_definitions_for_lifecycle(callback, class_generator, first_flag, out)

        for cur_method_generator in get_all_methods(class_generator.base_class_generator):
            first_flag = generate_method_callback_definition(first_flag, cur_method_generator, out)

        out.put_line('')
        out.put_line(class_generator.parent_namespace.one_line_namespace_end)


def generate_copy_semantic_callback_members(callback_impl, callback_names, class_generator):
    callback_impl.put_line('{0} copy_callback;'.format(class_generator.copy_callback_type))
    callback_names.append('copy_callback')
    callback_impl.put_line('{0} delete_callback;'.format(class_generator.delete_callback_type))
    callback_names.append('delete_callback')


def generate_reference_counted_semantic_callback_members(callback_impl, callback_names, class_generator):
    callback_impl.put_line('{0} add_ref_callback;'.format(class_generator.add_ref_callback_type))
    callback_names.append('add_ref_callback')
    callback_impl.put_line('{0} release_callback;'.format(class_generator.release_callback_type))
    callback_names.append('release_callback')


def generate_lifecycle_callback_members(callback_impl, callback_names, class_generator, callback):
    if callback.lifecycle == TLifecycle.copy_semantic:
        generate_copy_semantic_callback_members(callback_impl, callback_names, class_generator)
    elif callback.lifecycle == TLifecycle.reference_counted:
        generate_reference_counted_semantic_callback_members(callback_impl, callback_names, class_generator)


def generate_callback_member(callback_impl, callback_names, cur_method_generator):
    callback_impl.put_line('{callback_type} {method_name}_callback;'.format(
        callback_type=cur_method_generator.callback_type,
        method_name=cur_method_generator.c_name
    ))
    callback_names.append('{method_name}_callback'.format(method_name=cur_method_generator.c_name))


def generate_callback_members(callback_impl, callback_names, class_generator):
    for cur_method_generator in get_all_methods(class_generator.base_class_generator):
        generate_callback_member(callback_impl, callback_names, cur_method_generator)


def generate_callback_implementation_default_constructor(callback_impl, callback_names, impl_class_name):
    callback_impl.put_line('{0}() :'.format(impl_class_name))
    with Indent(callback_impl):
        for callback_name in callback_names:
            callback_impl.put_line('{callback_name}(0),'.format(callback_name=callback_name))
        callback_impl.put_line('mObject(0)')
    with IndentScope(callback_impl):
        pass


def generate_callback_implementation_copy_impl(callback_impl):
    callback_impl.put_line('if (mObject && copy_callback)')
    with IndentScope(callback_impl):
        callback_impl.put_line('mObject = copy_callback(mObject);')


def generate_callback_implementation_add_ref_impl(callback_impl):
    callback_impl.put_line('if (mObject && add_ref_callback)')
    with IndentScope(callback_impl):
        callback_impl.put_line('add_ref_callback(mObject);')


def generate_callback_implementation_copy_constructor_body(callback, callback_impl):
    if callback.lifecycle == TLifecycle.copy_semantic:
        generate_callback_implementation_copy_impl(callback_impl)
    elif callback.lifecycle == TLifecycle.reference_counted:
        generate_callback_implementation_add_ref_impl(callback_impl)


def generate_callback_implementation_copy_constructor(callback, callback_impl, callback_names, impl_class_name):
    callback_impl.put_line('{0}(const {0}& other) :'.format(impl_class_name))
    with Indent(callback_impl):
        for callback_name in callback_names:
            callback_impl.put_line('{0}(other.{0}),'.format(callback_name))
        callback_impl.put_line('mObject(other.mObject)')
    with IndentScope(callback_impl):
        generate_callback_implementation_copy_constructor_body(callback, callback_impl)


def generate_callback_implementation_destructor(callback, callback_impl, impl_class_name):
    if callback.lifecycle == TLifecycle.copy_semantic:
        callback_impl.put_line('~{0}()'.format(impl_class_name))
        with IndentScope(callback_impl):
            callback_impl.put_line('if (mObject && delete_callback)')
            with IndentScope(callback_impl):
                callback_impl.put_line('delete_callback(mObject);')
    elif callback.lifecycle == TLifecycle.reference_counted:
        callback_impl.put_line('~{0}()'.format(impl_class_name))
        with IndentScope(callback_impl):
            callback_impl.put_line('if (mObject && release_callback)')
            with IndentScope(callback_impl):
                callback_impl.put_line('release_callback(mObject);')


def generate_callback_implementation_set_object_pointer_method(callback, callback_impl):
    callback_impl.put_line('void SetObjectPointer(void* object_pointer)')
    with IndentScope(callback_impl):
        callback_impl.put_line('mObject = object_pointer;')
        generate_callback_implementation_copy_constructor_body(callback, callback_impl)


def generate_callback_implementation_get_object_pointer_method(callback_impl):
    callback_impl.put_line('void* GetObjectPointer() const')
    with IndentScope(callback_impl):
        callback_impl.put_line('return mObject;')


def generate_callback_implementation_set_c_function_for_method(callback_impl, cur_method_generator):
    callback_impl.put_line('void SetCFunctionFor{method_name}({callback_type} c_function_pointer)'.format(
        method_name=cur_method_generator.name, callback_type=cur_method_generator.callback_type))
    with IndentScope(callback_impl):
        callback_impl.put_line('{method_name}_callback = c_function_pointer;'.format(
            method_name=cur_method_generator.c_name
        ))


def generate_callback_implementation_set_c_function_for_methods(callback_impl, class_generator):
    for cur_method_generator in get_all_methods(class_generator.base_class_generator):
        generate_callback_implementation_set_c_function_for_method(callback_impl, cur_method_generator)


def generate_callback_implementation_for_method(callback_impl, cur_method_gen):
    args = [arg_gen.snippet_implementation_declaration() for arg_gen in cur_method_gen.argument_generators]
    callback_impl.put_line('{return_type} {method_name}({arguments}){const}'.format(
        return_type=cur_method_gen.return_type_generator.snippet_implementation_declaration(),
        method_name=cur_method_gen.name,
        arguments=', '.join(args),
        const=' const' if cur_method_gen.method_object.const else ''
    ))
    with IndentScope(callback_impl):
        arguments_call = [arg_gen.implementation_2_c() for arg_gen in cur_method_gen.c_arguments_list]
        callback_name = '{method_name}_callback'.format(method_name=cur_method_gen.c_name)
        return_expression = cur_method_gen.exception_traits.generate_c_call_from_impl(
            callback_impl, cur_method_gen.return_type_generator, callback_name, arguments_call)
        callback_impl.put_return_cpp_statement(return_expression)


def generate_callback_implementation_for_methods(callback_impl, class_generator):
    for cur_method_gen in get_all_methods(class_generator.base_class_generator):
        generate_callback_implementation_for_method(callback_impl, cur_method_gen)


def generate_callback_implementation_body(callback, callback_impl, class_generator, impl_class_name):
    callback_impl.put_line('void* mObject;')
    callback_names = []
    generate_lifecycle_callback_members(callback_impl, callback_names, class_generator, callback)
    generate_callback_members(callback_impl, callback_names, class_generator)
    with Unindent(callback_impl):
        callback_impl.put_line('public:')
    generate_callback_implementation_default_constructor(callback_impl, callback_names, impl_class_name)
    generate_callback_implementation_copy_constructor(callback, callback_impl, callback_names, impl_class_name)
    generate_callback_implementation_destructor(callback, callback_impl, impl_class_name)
    generate_callback_implementation_set_object_pointer_method(callback, callback_impl)
    generate_callback_implementation_get_object_pointer_method(callback_impl)
    generate_callback_implementation_set_c_function_for_methods(callback_impl, class_generator)
    generate_callback_implementation_for_methods(callback_impl, class_generator)


def generate_callbacks_on_library_side(class_generator, capi_generator):
    if class_generator.base_class_generator and class_generator.base_class_generator.class_object.callbacks:
        callback = class_generator.base_class_generator.class_object.callbacks[0]

        if class_generator.class_object.implementation_class_header_filled:
            capi_generator.loader_traits.add_impl_header(class_generator.class_object.implementation_class_header)

        callback_impl = FileGenerator(None)
        callback_impl.put_line(class_generator.parent_namespace.one_line_namespace_begin)
        callback_impl.put_line('')

        impl_class_name = get_callback_impl_name(class_generator)

        callback_impl.put_line('class {0} : public {1}'.format(
            impl_class_name, class_generator.base_class_generator.class_object.implementation_class_name))
        with IndentScope(callback_impl, '};'):
            generate_callback_implementation_body(callback, callback_impl, class_generator, impl_class_name)

        callback_impl.put_line('')
        callback_impl.put_line(class_generator.parent_namespace.one_line_namespace_end)
        capi_generator.callback_implementations.append(callback_impl)
