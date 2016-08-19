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


import Parser
from ExceptionTraits import create_exception_traits
from FileGenerator import Indent
from FileGenerator import IndentScope
from FileGenerator import NewFilesScope
from FileGenerator import Unindent
from FileGenerator import FileGenerator
from Constants import Constants
import Helpers


def begin_namespace(cur_namespace, capi_generator):
    capi_generator.cur_namespace_path.append(cur_namespace.m_name)


def end_namespace(cur_namespace, capi_generator):
    capi_generator.cur_namespace_path.pop()


def begin_namespace_gen(cur_namespace, capi_generator):
    begin_namespace(cur_namespace, capi_generator)
    capi_generator.output_header.put_line('namespace {0}'.format(cur_namespace.m_name))
    capi_generator.output_header.put_line('{')
    capi_generator.output_header.increase_indent()


def end_namespace_gen(cur_namespace, capi_generator):
    end_namespace(cur_namespace, capi_generator)
    capi_generator.output_header.decrease_indent()
    capi_generator.output_header.put_line('}')


def get_cur_namespace_id(cur_callback, capi_generator):
    return (capi_generator.get_namespace_id() + '_' + cur_callback.m_name).lower()


def get_copy_object_callback_type(cur_callback, capi_generator):
    return get_cur_namespace_id(cur_callback, capi_generator) + '_copy_object_callback_type'


def get_delete_object_callback_type(cur_callback, capi_generator):
    return get_cur_namespace_id(cur_callback, capi_generator) + '_delete_object_callback_type'


def get_add_ref_object_callback_type(cur_callback, capi_generator):
    return get_cur_namespace_id(cur_callback, capi_generator) + '_add_ref_object_callback_type'


def get_release_object_callback_type(cur_callback, capi_generator):
    return get_cur_namespace_id(cur_callback, capi_generator) + '_release_object_callback_type'


def get_method_callback_type(cur_callback, capi_generator, cur_method):
    return '{ns}_{name}_callback_type'.format(
        ns=get_cur_namespace_id(cur_callback, capi_generator),
        name=cur_method.m_name.lower())


def get_copy_object_callback_name(cur_callback):
    return 'callback_for_{0}_copy_object'.format(cur_callback.m_name.lower())


def get_delete_object_callback_name(cur_callback):
    return 'callback_for_{0}_delete_object'.format(cur_callback.m_name.lower())


def get_add_ref_object_callback_name(cur_callback):
    return 'callback_for_{0}_add_ref_object'.format(cur_callback.m_name.lower())


def get_release_object_callback_name(cur_callback):
    return 'callback_for_{0}_release_object'.format(cur_callback.m_name.lower())


def get_method_callback_name(cur_callback, cur_method):
    return 'callback_for_{callback_name}_{method_name}'.format(
        callback_name=cur_callback.m_name.lower(),
        method_name=cur_method.m_name.lower())


def generate_class_for_callback(cur_callback, base_class, cur_namespace, capi_generator):
    new_callback_class = Parser.TClass()
    new_callback_class.m_name = cur_callback.m_name
    new_callback_class.m_base = cur_callback.m_base
    new_callback_class.m_lifecycle = base_class.m_lifecycle
    new_callback_class.m_implementation_class_name = 'beautiful_capi::' + '::'.join(capi_generator.cur_namespace_path)
    new_callback_class.m_implementation_class_name += '::AutoGen' + cur_callback.m_name + 'Impl'
    new_callback_class.m_implementation_class_name_filled = True

    new_default_constructor = Parser.TConstructor()
    new_default_constructor.m_name = 'Default'
    new_callback_class.m_constructors.append(new_default_constructor)

    if cur_callback.m_lifecycle == Parser.TLifecycle.copy_semantic:

        set_copy_c_function = Parser.TMethod()
        set_copy_c_function.m_name = 'SetCFunctionForCopy'
        set_copy_c_function.m_arguments.append(Parser.TArgument())
        set_copy_c_function.m_arguments[0].m_type = get_copy_object_callback_type(cur_callback, capi_generator)
        set_copy_c_function.m_arguments[0].m_name = 'c_function_pointer'
        new_callback_class.m_methods.append(set_copy_c_function)

        set_delete_c_function = Parser.TMethod()
        set_delete_c_function.m_name = 'SetCFunctionForDelete'
        set_delete_c_function.m_arguments.append(Parser.TArgument())
        set_delete_c_function.m_arguments[0].m_type = get_delete_object_callback_type(cur_callback, capi_generator)
        set_delete_c_function.m_arguments[0].m_name = 'c_function_pointer'
        new_callback_class.m_methods.append(set_delete_c_function)

    elif cur_callback.m_lifecycle == Parser.TLifecycle.reference_counted:
        set_add_ref_c_function = Parser.TMethod()
        set_add_ref_c_function.m_name = 'SetCFunctionForAddRef'
        set_add_ref_c_function.m_arguments.append(Parser.TArgument())
        set_add_ref_c_function.m_arguments[0].m_type = get_add_ref_object_callback_type(cur_callback, capi_generator)
        set_add_ref_c_function.m_arguments[0].m_name = 'c_function_pointer'
        new_callback_class.m_methods.append(set_add_ref_c_function)

        set_release_c_function = Parser.TMethod()
        set_release_c_function.m_name = 'SetCFunctionForRelease'
        set_release_c_function.m_arguments.append(Parser.TArgument())
        set_release_c_function.m_arguments[0].m_type = get_release_object_callback_type(cur_callback, capi_generator)
        set_release_c_function.m_arguments[0].m_name = 'c_function_pointer'
        new_callback_class.m_methods.append(set_release_c_function)

    set_object_pointer_method = Parser.TMethod()
    set_object_pointer_method.m_name = 'SetObjectPointer'
    set_object_pointer_method.m_arguments.append(Parser.TArgument())
    set_object_pointer_method.m_arguments[0].m_type = 'void*'
    set_object_pointer_method.m_arguments[0].m_name = 'custom_object'
    new_callback_class.m_methods.append(set_object_pointer_method)

    get_object_pointer_method = Parser.TMethod()
    get_object_pointer_method.m_name = 'GetObjectPointer'
    get_object_pointer_method.m_return = 'void*'
    new_callback_class.m_methods.append(get_object_pointer_method)

    for cur_method in base_class.m_methods:
        set_c_function_method = Parser.TMethod()
        set_c_function_method.m_name = 'SetCFunctionFor{0}'.format(cur_method.m_name)
        set_c_function_method.m_arguments.append(Parser.TArgument())
        set_c_function_method.m_arguments[0].m_type = get_method_callback_type(cur_callback, capi_generator, cur_method)
        set_c_function_method.m_arguments[0].m_name = 'c_function_pointer'
        new_callback_class.m_methods.append(set_c_function_method)

        exception_traits = create_exception_traits(cur_method, base_class, capi_generator)
        callback_customer_wrap = FileGenerator(None)
        with NewFilesScope(callback_customer_wrap, capi_generator):
            callback_customer_wrap.put_line('template<typename ImplementationClass>')
            callback_customer_wrap.put_line(
                '{return_type} {callback_name}({arguments})'.format(
                    return_type=capi_generator.get_c_type(cur_method.m_return),
                    callback_name=get_method_callback_name(cur_callback, cur_method),
                    arguments=', '.join(exception_traits.get_c_argument_pairs())
                )
            )
            with IndentScope(callback_customer_wrap):
                callback_customer_wrap.put_line(
                    'ImplementationClass* self = static_cast<ImplementationClass*>(object_pointer);'
                )
                method_call = '{0}self->{1}({2});'.format(
                    capi_generator.get_c_return_instruction(cur_method.m_return),
                    cur_method.m_name,
                    ', '.join(capi_generator.get_c_to_original_arguments(cur_method.m_arguments))
                )
                exception_traits.generate_implementation_call(method_call, cur_method.m_return)
        Helpers.save_file_generator_to_code_blocks(callback_customer_wrap,
                                                   new_callback_class.m_code_after_class_definitions)

    callback_customer_lifecycle = FileGenerator(None)
    if cur_callback.m_lifecycle == Parser.TLifecycle.copy_semantic:
        callback_customer_lifecycle.put_line('template<typename ImplementationClass>')
        callback_customer_lifecycle.put_line(
            'void* {0}(void* object_pointer)'.format(get_copy_object_callback_name(cur_callback)))
        with IndentScope(callback_customer_lifecycle):
            callback_customer_lifecycle.put_line(
                'const ImplementationClass* self = static_cast<ImplementationClass*>(object_pointer);'
            )
            callback_customer_lifecycle.put_line('return new ImplementationClass(*self);')
        callback_customer_lifecycle.put_line('template<typename ImplementationClass>')
        callback_customer_lifecycle.put_line(
            'void* {0}(void* object_pointer)'.format(get_delete_object_callback_name(cur_callback)))
        with IndentScope(callback_customer_lifecycle):
            callback_customer_lifecycle.put_line(
                'const ImplementationClass* self = static_cast<ImplementationClass*>(object_pointer);'
            )
            callback_customer_lifecycle.put_line('delete self;')
            callback_customer_lifecycle.put_line('return 0;')
    elif cur_callback.m_lifecycle == Parser.TLifecycle.reference_counted:
        callback_customer_lifecycle.put_line('template<typename ImplementationClass>')
        callback_customer_lifecycle.put_line(
            'void* {0}(void* object_pointer)'.format(get_add_ref_object_callback_name(cur_callback)))
        with IndentScope(callback_customer_lifecycle):
            callback_customer_lifecycle.put_line(
                'const ImplementationClass* self = static_cast<ImplementationClass*>(object_pointer);'
            )
            callback_customer_lifecycle.put_line('intrusive_ptr_add_ref(self);')
            callback_customer_lifecycle.put_line('return object_pointer;')
        callback_customer_lifecycle.put_line('template<typename ImplementationClass>')
        callback_customer_lifecycle.put_line(
            'void* {0}(void* object_pointer)'.format(get_release_object_callback_name(cur_callback)))
        with IndentScope(callback_customer_lifecycle):
            callback_customer_lifecycle.put_line(
                'const ImplementationClass* self = static_cast<ImplementationClass*>(object_pointer);'
            )
            callback_customer_lifecycle.put_line('intrusive_ptr_release(self);')
            callback_customer_lifecycle.put_line('return 0;')
    if not callback_customer_lifecycle.empty():
        Helpers.save_file_generator_to_code_blocks(callback_customer_lifecycle,
                                                   new_callback_class.m_code_after_class_definitions)

    cur_namespace.m_classes.append(new_callback_class)
    capi_generator.callback_2_class.update({cur_callback: new_callback_class})


def generate_create_functions_for_callback(cur_callback, base_class, cur_namespace, capi_generator):
    callback_class = capi_generator.callback_2_class[cur_callback]
    callback_class_name = capi_generator.extra_info[callback_class].get_class_name()
    callback_class_c_name = capi_generator.extra_info[callback_class].get_c_name()

    if cur_callback.m_lifecycle == Parser.TLifecycle.copy_semantic:
        capi_generator.callback_typedefs.put_line(
            'typedef void* (*{0})(void*);'.format(get_copy_object_callback_type(cur_callback, capi_generator)))
        capi_generator.callback_typedefs.put_line(
            'typedef void* (*{0})(void*);'.format(get_delete_object_callback_type(cur_callback, capi_generator)))
    elif cur_callback.m_lifecycle == Parser.TLifecycle.reference_counted:
        capi_generator.callback_typedefs.put_line(
            'typedef void* (*{0})(void*);'.format(get_add_ref_object_callback_type(cur_callback, capi_generator)))
        capi_generator.callback_typedefs.put_line(
            'typedef void* (*{0})(void*);'.format(get_release_object_callback_type(cur_callback, capi_generator)))

    for cur_method in base_class.m_methods:
        exception_traits = create_exception_traits(cur_method, base_class, capi_generator)
        callback_typedef = 'typedef {return_type} (*{name})({arguments});'.format(
            return_type=capi_generator.get_c_type(cur_method.m_return),
            ns=callback_class_c_name,
            name=get_method_callback_type(cur_callback, capi_generator, cur_method),
            arguments=', '.join(exception_traits.get_c_argument_pairs()))
        capi_generator.callback_typedefs.put_line(callback_typedef)

    create_callback_function = FileGenerator(None)
    with NewFilesScope(create_callback_function, capi_generator):
        create_callback_function.put_line('template<typename ImplementationClass>')
        create_callback_function.put_line(
            '{return_type} create_callback_for_{class_suffix}(ImplementationClass* implementation_class)'.format(
                return_type=callback_class_name,
                class_suffix=callback_class.m_name.lower()))
        with IndentScope(create_callback_function):
            create_callback_function.put_line('{0} result;'.format(callback_class_name))
            if cur_callback.m_lifecycle == Parser.TLifecycle.copy_semantic:
                create_callback_function.put_line(
                    'result.SetCFunctionForCopy(callback_for_{0}_copy_object<ImplementationClass>);'.format(
                        cur_callback.m_name.lower()))
                create_callback_function.put_line(
                    'result.SetCFunctionForDelete(callback_for_{0}_delete_object<ImplementationClass>);'.format(
                        cur_callback.m_name.lower()))
            elif cur_callback.m_lifecycle == Parser.TLifecycle.reference_counted:
                create_callback_function.put_line(
                    'result.SetCFunctionForAddRef(callback_for_{0}_add_ref_object<ImplementationClass>);'.format(
                        cur_callback.m_name.lower()))
                create_callback_function.put_line(
                    'result.SetCFunctionForRelease(callback_for_{0}_release_object<ImplementationClass>);'.format(
                        cur_callback.m_name.lower()
                    ))

            for cur_method in base_class.m_methods:
                cur_callback_name = 'callback_for_{class_suffix}_{method_suffix}'.format(
                    class_suffix=cur_callback.m_name.lower(), method_suffix=cur_method.m_name.lower()
                )
                create_callback_function.put_line(
                    'result.SetCFunctionFor{0}({1}<ImplementationClass>);'.format(cur_method.m_name, cur_callback_name)
                )
                create_callback_function.put_line('result.SetObjectPointer(implementation_class);')
                create_callback_function.put_line('return result;')

        create_callback_function.put_line('template<typename ImplementationClass>')
        create_callback_function.put_line(
            '{return_type} create_callback_for_{class_suffix}(ImplementationClass& implementation_class)'.format(
                return_type=callback_class_name,
                class_suffix=callback_class.m_name.lower()))
        with IndentScope(create_callback_function):
            create_callback_function.put_line(
                'return create_callback_for_{0}(&implementation_class);'.format(callback_class.m_name.lower()))

    Helpers.save_file_generator_to_code_blocks(create_callback_function,
                                               callback_class.m_code_after_class_definitions)


def generate_callbacks_implementations_impl(cur_callback, base_class, cur_namespace, capi_generator):
    impl_class_name = 'AutoGen{0}Impl'.format(cur_callback.m_name)

    ctor_callback_type = ''
    ctor_callback_name = ''
    dtor_callback_type = ''
    dtor_callback_name = ''
    set_ctor_function_name = ''
    set_dtor_function_name = ''
    if cur_callback.m_lifecycle == Parser.TLifecycle.reference_counted:
        ctor_callback_type = get_add_ref_object_callback_type(cur_callback, capi_generator)
        ctor_callback_name = 'copy_callback'
        dtor_callback_type = get_release_object_callback_type(cur_callback, capi_generator)
        dtor_callback_name = 'delete_callback'
        set_ctor_function_name = 'SetCFunctionForAddRef'
        set_dtor_function_name = 'SetCFunctionForRelease'
    elif cur_callback.m_lifecycle == Parser.TLifecycle.copy_semantic:
        ctor_callback_type = get_copy_object_callback_type(cur_callback, capi_generator)
        ctor_callback_name = 'add_ref_callback'
        dtor_callback_type = get_delete_object_callback_type(cur_callback, capi_generator)
        dtor_callback_name = 'release_callback'
        set_ctor_function_name = 'SetCFunctionForCopy'
        set_dtor_function_name = 'SetCFunctionForDelete'

    capi_generator.output_source.put_line('class {0} : public ::{1}'.format(
        impl_class_name,
        cur_callback.m_implementation_class_name if cur_callback.m_implementation_class_name
        else base_class.m_implementation_class_name))
    with IndentScope(capi_generator.output_source, '};'):
        capi_generator.output_source.put_line('void* {0};'.format(Constants.object_var))
        if ctor_callback_type and ctor_callback_name:
            capi_generator.output_source.put_line('{0} {1};'.format(ctor_callback_type, ctor_callback_name))
        if dtor_callback_type and dtor_callback_name:
            capi_generator.output_source.put_line('{0} {1};'.format(dtor_callback_type, dtor_callback_name))
        for cur_method in base_class.m_methods:
            capi_generator.output_source.put_line('{function_p_type} {name}_callback;'.format(
                function_p_type=get_method_callback_type(cur_callback, capi_generator, cur_method),
                name=cur_method.m_name.lower()))
        with Unindent(capi_generator.output_source):
            capi_generator.output_source.put_line('public:')
        capi_generator.output_source.put_line('{0}() :'.format(impl_class_name))
        with Indent(capi_generator.output_source):
            for cur_method in base_class.m_methods:
                capi_generator.output_source.put_line('{0}_callback(0),'.format(cur_method.m_name.lower()))
            if ctor_callback_name:
                capi_generator.output_source.put_line('{0}(0),'.format(ctor_callback_name))
            if dtor_callback_name:
                capi_generator.output_source.put_line('{0}(0),'.format(dtor_callback_name))
            capi_generator.output_source.put_line('{0}(0)'.format(Constants.object_var))
        with IndentScope(capi_generator.output_source):
            pass
        if dtor_callback_name:
            capi_generator.output_source.put_line('~{0}()'.format(impl_class_name))
            with IndentScope(capi_generator.output_source):
                capi_generator.output_source.put_line(
                    'if ({0} && delete_or_release_callback)'.format(Constants.object_var))
                with IndentScope(capi_generator.output_source):
                    capi_generator.output_source.put_line(
                        '{0} = delete_or_release_callback({0});'.format(Constants.object_var))
        capi_generator.output_source.put_line('{0}(const {0}& other)'.format(impl_class_name))
        with IndentScope(capi_generator.output_source):
            if ctor_callback_name:
                capi_generator.output_source.put_line('{0} = other.{0};'.format(ctor_callback_name))
            if dtor_callback_name:
                capi_generator.output_source.put_line('{0} = other.{0};'.format(dtor_callback_name))
            for cur_method in base_class.m_methods:
                capi_generator.output_source.put_line(
                    '{0}_callback = other.{0}_callback;'.format(cur_method.m_name.lower()))
            capi_generator.output_source.put_line('{0} = other.{0};'.format(Constants.object_var))
            if ctor_callback_name:
                capi_generator.output_source.put_line(
                    'if ({0} && copy_or_add_ref_callback)'.format(Constants.object_var))
                with IndentScope(capi_generator.output_source):
                    capi_generator.output_source.put_line(
                        '{0} = copy_or_add_ref_callback(other.{0});'.format(Constants.object_var))
        if ctor_callback_type:
            capi_generator.output_source.put_line('void {0}({1} c_function_pointer)'.format(
                set_ctor_function_name, ctor_callback_type))
            with IndentScope(capi_generator.output_source):
                capi_generator.output_source.put_line(
                    'copy_or_add_ref_callback = c_function_pointer;')
        if dtor_callback_type:
            capi_generator.output_source.put_line('void {0}({1} c_function_pointer)'.format(
                set_dtor_function_name, dtor_callback_type))
            with IndentScope(capi_generator.output_source):
                capi_generator.output_source.put_line(
                    'delete_or_release_callback = c_function_pointer;')
        capi_generator.output_source.put_line('void SetObjectPointer(void* custom_object)')
        with IndentScope(capi_generator.output_source):
            capi_generator.output_source.put_line('if ({0} != custom_object)'.format(Constants.object_var))
            with IndentScope(capi_generator.output_source):
                if dtor_callback_name:
                    capi_generator.output_source.put_line(
                        'if ({0} && delete_or_release_callback)'.format(Constants.object_var))
                    with IndentScope(capi_generator.output_source):
                        capi_generator.output_source.put_line(
                            '{0} = delete_or_release_callback({0});'.format(Constants.object_var))
                capi_generator.output_source.put_line('{0} = custom_object;'.format(Constants.object_var))
                if ctor_callback_name:
                    capi_generator.output_source.put_line(
                        'if ({0} && copy_or_add_ref_callback)'.format(Constants.object_var))
                    with IndentScope(capi_generator.output_source):
                        capi_generator.output_source.put_line(
                            '{0} = copy_or_add_ref_callback({0});'.format(Constants.object_var))
        capi_generator.output_source.put_line('void* GetObjectPointer()')
        with IndentScope(capi_generator.output_source):
            capi_generator.output_source.put_line('return {0};'.format(Constants.object_var))
        for cur_method in base_class.m_methods:
            capi_generator.output_source.put_line(
                'void SetCFunctionFor{0}({1} c_function_pointer)'.format(
                    cur_method.m_name,
                    get_method_callback_type(cur_callback, capi_generator, cur_method)))
            with IndentScope(capi_generator.output_source):
                capi_generator.output_source.put_line(
                    '{0}_callback = c_function_pointer;'.format(cur_method.m_name.lower()))
        for cur_method in base_class.m_methods:
            exception_traits = create_exception_traits(cur_method, base_class, capi_generator)
            capi_generator.output_source.put_line(
                '{return_type} {method_name}({arguments})'.format(
                    return_type=capi_generator.get_original_type(cur_method.m_return),
                    method_name=cur_method.m_name,
                    arguments=', '.join(capi_generator.get_original_argument_pairs(cur_method.m_arguments))))
            with IndentScope(capi_generator.output_source):
                exception_traits.generate_c_call(
                    '{0}_callback'.format(cur_method.m_name.lower()),
                    '{c_function}({arguments})',
                    False
                )


def process_namespace_impl(namespace, capi_generator, process_method, begin_ns_method, end_ns_method):
    begin_ns_method(namespace, capi_generator)
    for cur_callback in namespace.m_callbacks:
        base_class = capi_generator.get_class_type(cur_callback.base)
        if base_class:
            process_method(cur_callback, base_class, namespace, capi_generator)
        else:
            print('Error: base class {0} is not found'.format(cur_callback.base))
    for nested_namespace in namespace.m_namespaces:
        process_namespace_impl(nested_namespace, capi_generator, process_method, begin_ns_method, end_ns_method)
    end_ns_method(namespace, capi_generator)


def process_callback_classes_impl(root_node, capi_generator, process_method, begin_ns_method, end_ns_method):
    for cur_namespace in root_node.m_namespaces:
        process_namespace_impl(cur_namespace, capi_generator, process_method, begin_ns_method, end_ns_method)


def generate_callback_classes(root_node, capi_generator):
    process_callback_classes_impl(
        root_node, capi_generator,
        generate_class_for_callback, begin_namespace, end_namespace)


def generate_custom_callbacks(root_node, capi_generator):
    process_callback_classes_impl(
        root_node, capi_generator,
        generate_create_functions_for_callback, begin_namespace, end_namespace)


def generate_callbacks_implementations(root_node, capi_generator):
    if not capi_generator.callback_typedefs.empty():
        with NewFilesScope(capi_generator.callbacks_implementations, capi_generator):
            capi_generator.output_header.put_line('namespace beautiful_capi')
            with IndentScope(capi_generator.output_header):
                process_callback_classes_impl(
                    root_node, capi_generator,
                    generate_callbacks_implementations_impl, begin_namespace_gen, end_namespace_gen)
            capi_generator.output_header.put_line('')
