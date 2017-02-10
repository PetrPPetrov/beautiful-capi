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


def get_callback_impl_name(class_generator) -> str:
    return '{prefix}{name}Impl'.format(
        prefix=class_generator.params.autogen_prefix_for_internal_implementation,
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
    new_callback_class.callbacks = True
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
