#!/usr/bin/env python
#
# Beautiful Capi generates beautiful C API wrappers for your C++ classes
# Copyright (C) 2018 Petr Petrovich Petrov
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

import os

import NamespaceGenerator
import CapiGenerator
from ClassGenerator import ClassGenerator
from LifecycleTraits import LifecycleTraits, RawPointerSemantic
from ArgumentGenerator import ArgumentGenerator, MappedTypeGenerator, ClassTypeGenerator
from BuiltinTypeGenerator import BuiltinTypeGenerator
from MethodGenerator import MethodGenerator, ConstructorGenerator, FunctionGenerator
from FileGenerator import FileGenerator, IndentScope
from Helpers import if_required_then_add_empty_line, bool_to_str, replace_template_to_filename
from Parser import TLifecycle, TClass, TMethod
from InheritanceTraits import RequiresCastToBase
from ExceptionTraits import NoHandling
from FileCache import FileCache, OsJoin, PosixJoin


class SharpNamespace(object):
    def __init__(self, namespace_generator: NamespaceGenerator, parent_namespace=None):
        self.namespace_generator = namespace_generator
        self.parent_namespace = parent_namespace
        self.nested_namespaces = [SharpNamespace(ns, self) for ns in namespace_generator.nested_namespaces]
        self.classes = [SharpClass(class_, self) for class_ in namespace_generator.classes]
        self.enums = [SharpEnum(enum, self) for enum in namespace_generator.enum_generators]
        self.functions = [SharpFunction(func, self) for func in namespace_generator.functions]
        self.capi_generator = None
        # TODO add templates
        # TODO check external namespaces and classes

    def __generate_initialisation_class(self):
        file_cache = SharpFileCache(FileCache(self.namespace_generator.params),
                                    self.namespace_generator.params.sharp_output_folder)
        file = file_cache.get_file_for_class(self.namespace_generator.full_name_array + ['Initialisation'])
        file.put_begin_cpp_comments(self.namespace_generator.params)
        file.put_line('using System.Runtime.InteropServices;')
        file.put_line('using System;')
        file.put_line('')
        self.increase_indent_recursively(file)
        file.put_line('public class Initialisation')
        with IndentScope(file):
            file.put_line('const int MAJOR_VERSION = {0};'.format(self.capi_generator.api_root.major_version))
            file.put_line('const int MINOR_VERSION = {0};'.format(self.capi_generator.api_root.minor_version))
            file.put_line('const int PATCH_VERSION = {0};'.format(self.capi_generator.api_root.patch_version))
            file.put_line('')
            file.put_line('public Initialisation()')
            with IndentScope(file):
                file.put_line('int major_version = Functions.GetMajorVersion();')
                file.put_line('int minor_version = Functions.GetMinorVersion();')
                file.put_line('int patch_version = Functions.GetPatchVersion();')
                file.put_line('if (MAJOR_VERSION != {0} || MINOR_VERSION != {1} || PATCH_VERSION != {2})'.format(
                    'major_version', 'minor_version', 'patch_version'))
                with IndentScope(file):
                    file.put_line('string message = "Incorrect version of {0} library.";'.format(
                        self.namespace_generator.params.shared_library_name))
                    file.put_line('message += "Expected version is " + {0} + "." + {1} + "." + {2} + ". ";'.format(
                        'MAJOR_VERSION', 'MINOR_VERSION', 'PATCH_VERSION'))
                    file.put_line('message += "Found version is " + {0} + "." + {1} + "." + {2} + ". ";'.format(
                        'major_version', 'minor_version', 'patch_version'))
                    file.put_line('throw new Exception(message);')
            file.put_line('')
        self.decrease_indent_recursively(file)

    def __generate_functions_class(self):
        file_cache = SharpFileCache(FileCache(self.namespace_generator.params),
                                    self.namespace_generator.params.sharp_output_folder)
        file = file_cache.get_file_for_class(self.namespace_generator.full_name_array[:-1] + ['{0}Functions'.format(
            self.namespace_generator.wrap_name)])
        file.put_begin_cpp_comments(self.namespace_generator.params)
        file.put_line('using System.Runtime.InteropServices;')
        file.put_line('')
        self.increase_indent_recursively(file)
        file.put_line('public static class Functions')
        with IndentScope(file):
            import_string = '[DllImport("{dll_name}.dll", CallingConvention = {calling_convention})]'.format(
                dll_name=self.namespace_generator.params.shared_library_name,
                calling_convention='CallingConvention.Cdecl'  # now used only cdecl convention
            )
            for func in self.functions:
                file.put_line(import_string)
                file.put_line('unsafe static extern {return_type} {name}({arguments});'.format(
                    return_type=func.return_type.c_argument_declaration(),
                    name=func.function_generator.full_c_name,
                    arguments=', '.join(SharpClass.export_function_arguments(func.arguments))
                ))
            file.put_line('')
            for func in self.functions:
                func.generate_wrap_definition(file, self.capi_generator)
        self.decrease_indent_recursively(file)

    def generate(self, cpp_file_cache: FileCache, capi_generator: CapiGenerator):
        self.capi_generator = capi_generator
        if self.enums:
            enums_header = self.enums[0].generate_enums_header(SharpFileCache(
                cpp_file_cache,
                self.namespace_generator.params.sharp_output_folder
            ))
            self.increase_indent_recursively(enums_header)
            for enum in self.enums:
                enum.generate_enum_definition(enums_header)

            self.decrease_indent_recursively(enums_header)
        for nested_namespace in self.nested_namespaces:
            nested_namespace.generate(cpp_file_cache, capi_generator)
        if not self.parent_namespace:
            self.__generate_initialisation_class()
        if self.functions:
            self.__generate_functions_class()
        for class_generator in self.classes:
            class_generator.generate()

        if self.namespace_generator.namespace_object.implementation_header_filled:
            capi_generator.additional_includes.include_user_header(
                self.namespace_generator.namespace_object.implementation_header)

    def increase_indent_recursively(self, out: FileGenerator):
        for namespace in self.namespace_generator.full_name_array:
            out.put_line('namespace {namespace}'.format(namespace=namespace))
            out.put_line('{')
            out.increase_indent()

    def decrease_indent_recursively(self, out: FileGenerator):
        for _ in range(len(self.namespace_generator.full_name_array)):
            out.decrease_indent()
            out.put_line('}')


class SharpClass(object):
    def __init__(self, class_generator: ClassGenerator, namespace: SharpNamespace):
        self.class_generator = class_generator
        self.namespace = namespace
        self.constructors = [SharpConstructor(ctor, self) for ctor in class_generator.constructor_generators]
        self.methods = [SharpMethod(method, self) for method in class_generator.method_generators]
        # self.functions = [SharpFunction(func, self) for func in class_generator.function_generators]
        self.file_cache = SharpFileCache(class_generator.file_cache, class_generator.params.sharp_output_folder)
        self.lifecycle_traits = create_sharp_lifecycle(class_generator.class_object.lifecycle,
                                                       class_generator.lifecycle_traits)
        self.enums = [SharpEnum(enum, self) for enum in class_generator.enum_generators]
        # TODO add templates

    def __generate_definition(self):
        definition_header = self.file_cache.get_file_for_class(self.class_generator.full_name_array)
        definition_header.put_begin_cpp_comments(self.class_generator.params)
        definition_header.put_line('using System.Runtime.InteropServices;\n')
        self.namespace.increase_indent_recursively(definition_header)
        base_class = self.class_generator.base_class_generator
        definition_header.put_line('public class {class_name}{base} '.format(
            class_name=self.class_generator.wrap_name,
            base=': public {0}'.format(base_class.wrap_name) if base_class else ''
        ))
        with IndentScope(definition_header):
            self.__generate_export_functions()
            definition_header.put_line('')
            definition_header.put_line('public enum ECreateFromRawPointer{ force_creating_from_raw_pointer };')
            definition_header.put_line('')
            definition_header.put_line('protected unsafe void* mObject;')
            definition_header.put_line('')
            if self.enums:
                for enum in self.enums:
                    enum.generate_enum_definition(definition_header)
                definition_header.put_line('')
            first_method = True
            first_method = self.__generate_constructor_definitions(definition_header, first_method)
            self.__generate_method_definitions(definition_header, first_method)
            definition_header.put_line('')
            self.lifecycle_traits.generate_std_methods_definitions(definition_header, self.class_generator)
            definition_header.put_line('')
            if hasattr(self, 'extension_base_class_generator'):
                self.class_generator.generate_cast_name_definition(definition_header)
                definition_header.put_line('')
            generate_set_object_definition(
                self.class_generator.inheritance_traits,
                definition_header,
                self.class_generator
            )
        self.namespace.decrease_indent_recursively(definition_header)

    def __generate_constructor_definitions(self, definition_header, first_method):
        for constructor_generator in self.constructors:
            first_method = if_required_then_add_empty_line(first_method, definition_header)
            constructor_generator.generate_wrap_definition(definition_header, self.class_generator.capi_generator)
        return first_method

    def __generate_method_definitions(self, definition_header, first_method):
        for method in self.methods:
            first_method = if_required_then_add_empty_line(first_method, definition_header)
            method.generate_wrap_definition(definition_header)

    @staticmethod
    def export_function_arguments(argument_generators: []):
        from ArgumentGenerator import MappedTypeGenerator
        result = []
        for argument in argument_generators:
            generator = argument.argument_generator.type_generator
            if isinstance(generator, MappedTypeGenerator):
                result.append(argument.wrap_argument_declaration())
            else:
                result.append(argument.c_argument_declaration())
        return result

    def __generate_export_functions(self):
        from LifecycleTraits import RefCountedSemantic
        header = self.file_cache.get_file_for_class(self.class_generator.full_name_array)
        import_string = '[DllImport("{dll_name}.dll", CallingConvention = {calling_convention})]'.format(
            dll_name=self.class_generator.params.shared_library_name,
            calling_convention='CallingConvention.Cdecl'  # now used only cdecl convention
        )
        for constructor in self.constructors:
            header.put_line(import_string)
            header.put_line('unsafe static extern void* {class_name}({arguments});'.format(
                class_name=constructor.constructor_generator.full_c_name,
                arguments=', '.join(self.export_function_arguments(constructor.arguments))
            ))
        for method in self.methods:
            header.put_line(import_string)
            this_argument = ['void* object_pointer']
            header.put_line('unsafe static extern {return_type} {name}({arguments});'.format(
                return_type=method.return_type.c_argument_declaration(),
                name=method.method_generator.full_c_name,
                arguments=', '.join(this_argument + self.export_function_arguments(method.arguments))
            ))
        if isinstance(self.class_generator.lifecycle_traits, RefCountedSemantic):
            header.put_line(import_string)
            header.put_line('unsafe static extern void {func_name}(void* object_pointer);'.format(
                func_name=self.class_generator.add_ref_method))
            header.put_line(import_string)
            header.put_line('unsafe static extern void {func_name}(void* object_pointer);'.format(
                func_name=self.class_generator.release_method))
        else:
            header.put_line(import_string)
            header.put_line('unsafe static extern void* {func_name}(void* object_pointer);'.format(
                func_name=self.class_generator.copy_method))
            header.put_line(import_string)
            header.put_line('unsafe static extern void {func_name}(void* object_pointer);'.format(
                func_name=self.class_generator.delete_method))

    def generate(self):
        self.__generate_definition()
        # generate_callbacks_on_library_side(self, capi_generator)


class SharpEnum(object):
    def __init__(self, enum_generator, parent: SharpNamespace or SharpClass):
        self.parent = parent
        self.enum_generator = enum_generator

    @staticmethod
    def get_enum_definition(enum_object) -> [str]:
        return [item.name + (' = ,' + item.value if item.value_filled else ',') for item in enum_object.items]

    def generate_enums_header(self, file_cache):
        if self.enum_generator:
            enums_header = file_cache.get_file_for_enums(self.enum_generator.parent_generator.full_name_array)
            enums_header.put_begin_cpp_comments(file_cache.file_cache.params)
            return enums_header

    def generate_enum_definition(self, out: FileGenerator):
        out.put_line('enum {name}'.format(name=self.enum_generator.name))
        with IndentScope(out, '};'):
            items_definitions = SharpEnum.get_enum_definition(self.enum_generator.enum_object)
            if items_definitions:
                for item_definition in items_definitions:
                    out.put_line(item_definition)


class SharpArgument(object):
    def __init__(self, argument_generator: ArgumentGenerator):
        self.argument_generator = argument_generator

    def wrap_argument_declaration(self) -> str:
        if isinstance(self.argument_generator.type_generator, ClassTypeGenerator):
            argument_type = self.argument_generator.type_generator.class_argument_generator.wrap_short_name
        elif isinstance(self.argument_generator.type_generator, MappedTypeGenerator):
            if self.argument_generator.type_generator.mapped_type_object.sharp_wrap_type:
                argument_type = self.argument_generator.type_generator.mapped_type_object.sharp_wrap_type
            else:
                argument_type = self.argument_generator.type_generator.wrap_argument_declaration()
        else:
            argument_type = self.argument_generator.type_generator.wrap_argument_declaration()
        return argument_type + ((' ' + self.argument_generator.name) if self.argument_generator.name else '')

    def c_argument_declaration(self) -> str:
        if isinstance(self.argument_generator.type_generator, ClassTypeGenerator):
            argument_type = 'void*'
        elif isinstance(self.argument_generator.type_generator, MappedTypeGenerator):
            if self.argument_generator.type_generator.mapped_type_object.sharp_wrap_type:
                argument_type = self.argument_generator.type_generator.mapped_type_object.sharp_wrap_type
            else:
                argument_type = self.argument_generator.type_generator.wrap_argument_declaration()
        else:
            argument_type = self.argument_generator.type_generator.wrap_argument_declaration()
        return argument_type + ((' ' + self.argument_generator.name) if self.argument_generator.name else '')

    def c_2_wrap_var(self, result_var: str, expression: str) -> ([str], str):
        if isinstance(self.argument_generator.type_generator, MappedTypeGenerator):
            return self.argument_generator.type_generator.format(
                self.argument_generator.type_generator.mapped_type_object.c_2_wrap,
                expression,
                result_var,
                self.argument_generator.type_generator.mapped_type_object.wrap_type
            )
        elif isinstance(self.argument_generator.type_generator, ClassTypeGenerator):
            internal_expression = '{type_name}.{create_from_ptr_expression}, {expression}, {copy_or_add_ref}'.format(
                create_from_ptr_expression='ECreateFromRawPointer.force_creating_from_raw_pointer',
                type_name=self.argument_generator.type_generator.class_argument_generator.wrap_name,
                expression=expression,
                copy_or_add_ref=bool_to_str(self.argument_generator.type_generator.copy_or_add_ref_when_c_2_wrap)
            )
            if result_var:
                return ['new {type_name} {result_var}({internal_expression});'.format(
                    type_name=self.argument_generator.type_generator.wrap_return_type(),
                    result_var=result_var,
                    internal_expression=internal_expression
                )], result_var
            else:
                return [], 'new {type_name}({internal_expression})'.format(
                    type_name=self.argument_generator.type_generator.class_argument_generator.wrap_name,
                    internal_expression=internal_expression
                )
        else:
                return self.argument_generator.type_generator.c_2_wrap_var(result_var, expression)


class SharpMethod(object):
    def __init__(self, method_generator: MethodGenerator, class_generator: SharpClass):
        self.method_generator = method_generator
        self.class_generator = class_generator
        self.arguments = [SharpArgument(arg) for arg in method_generator.argument_generators]
        self.return_type = SharpArgument(ArgumentGenerator(method_generator.return_type_generator, ''))
        self.exception_traits = SharpExceptionTraits(method_generator.exception_traits)

    def generate_wrap_definition(self, out: FileGenerator):
        arguments = ', '.join(argument.wrap_argument_declaration() for argument in self.arguments)
        arguments_call = [argument.wrap_2_c() for argument in self.method_generator.c_arguments_list]
        out.put_line('unsafe public {return_type} {name}({arguments})'.format(
            return_type=self.return_type.wrap_argument_declaration(),
            name=self.method_generator.wrap_name,
            arguments=arguments
        ))
        with IndentScope(out):
            return_expression = self.exception_traits.generate_c_call(
                out,
                self.return_type,
                self.method_generator.full_c_name,
                arguments_call
            )
            out.put_return_cpp_statement(return_expression)


class SharpConstructor(object):
    def __init__(self, constructor_generator: ConstructorGenerator, class_generator: SharpClass):
        self.constructor_generator = constructor_generator
        self.class_generator = class_generator
        self.arguments = [SharpArgument(arg) for arg in constructor_generator.argument_generators]

    def generate_wrap_definition(self, out: FileGenerator, capi_generator: CapiGenerator):
        self.constructor_generator.exception_traits = capi_generator.get_exception_traits(
            self.constructor_generator.constructor_object.noexcept)
        arguments = ', '.join(argument.wrap_argument_declaration() for argument in self.arguments)
        arguments_call = [argument.wrap_2_c() for argument in self.constructor_generator.argument_generators]
        out.put_line('unsafe public {class_name}({arguments}){base_init}'.format(
            class_name=self.constructor_generator.parent_class_generator.wrap_short_name,
            arguments=arguments,
            base_init=''#self.constructor_generator.get_base_init(self.constructor_generator.parent_class_generator)
        ))
        with IndentScope(out):
            result_expression = self.constructor_generator.exception_traits.generate_c_call(
                out,
                SharpArgument(ArgumentGenerator(ClassTypeGenerator(
                    self.constructor_generator.parent_class_generator), '')),
                self.constructor_generator.full_c_name,
                arguments_call
            )
            out.put_line('SetObject({result_expression}.{detach}());'.format(
                result_expression=result_expression,
                detach=self.constructor_generator.params.detach_method_name
            ))


class SharpFunction(object):
    def __init__(self, function_generator: FunctionGenerator, parent: SharpClass or SharpNamespace):
        self.function_generator = function_generator
        self.parent = parent
        self.arguments = [SharpArgument(arg) for arg in function_generator.argument_generators]
        self.return_type = SharpArgument(ArgumentGenerator(function_generator.return_type_generator, ''))
        self.exception_traits = SharpExceptionTraits(function_generator.exception_traits)

    def generate_wrap_definition(self, out: FileGenerator, capi_generator: CapiGenerator):
        self.function_generator.exception_traits = capi_generator.get_exception_traits(
            self.function_generator.function_object.noexcept)
        arguments = ', '.join(argument.wrap_argument_declaration() for argument in self.arguments)
        arguments_call = [argument.wrap_2_c() for argument in self.function_generator.argument_generators]
        out.put_line('public unsafe static {return_type} {name}({arguments})'.format(
            return_type=self.function_generator.return_type_generator.wrap_return_type(),
            name=self.function_generator.wrap_name,
            arguments=arguments
        ))
        with IndentScope(out):
            return_expression = self.exception_traits.generate_c_call(
                out,
                self.function_generator.return_type_generator,
                self.function_generator.full_c_name,
                arguments_call
            )
            out.put_return_cpp_statement(return_expression)


class SharpLifecycleTraits(object):
    def __init__(self, lifecycle_traits: LifecycleTraits):
        self.lifecycle_traits = lifecycle_traits
        self.params = lifecycle_traits.params

    def generate_std_methods_definitions(self, out: FileGenerator, class_generator):
        out.put_line('unsafe public {class_name} {null_method}()'.format(
            class_name=class_generator.wrap_name,
            null_method=self.params.null_method_name))
        with IndentScope(out):
            out.put_line('return new {class_name}({class_name}.{force_create}, null, false);'.format(
                force_create='ECreateFromRawPointer.force_creating_from_raw_pointer',
                class_name=class_generator.wrap_name))
        out.put_line('')
        out.put_line('unsafe public bool {is_null_method}()'.format(
            is_null_method=self.params.is_null_method_name))
        with IndentScope(out):
            out.put_line('return {get_raw}() != null;'.format(get_raw=self.params.get_raw_pointer_method_name))
        out.put_line('')
        out.put_line('unsafe public bool {is_not_null_method}()'.format(
            is_not_null_method=self.params.is_not_null_method_name))
        with IndentScope(out):
            out.put_line('return {get_raw}() != null;'.format(get_raw=self.params.get_raw_pointer_method_name))
        out.put_line('')
        out.put_line('unsafe public static bool operator!({class_name} obj)'.format(
            class_name=class_generator.wrap_name))
        with IndentScope(out):
            out.put_line('return obj.{get_raw}() != null;'.format(get_raw=self.params.get_raw_pointer_method_name))
        out.put_line('')
        out.put_line('unsafe public void* {detach_method}()'.format(
            detach_method=self.params.detach_method_name))
        with IndentScope(out):
            out.put_line('void* result = {get_raw}();'.format(get_raw=self.params.get_raw_pointer_method_name))
            out.put_line('SetObject(null);')
            out.put_line('return result;')
        out.put_line('')
        out.put_line('unsafe public void* {get_raw_pointer_method}()'.format(
             get_raw_pointer_method=self.params.get_raw_pointer_method_name))
        with IndentScope(out):
            out.put_line('return mObject != null ? mObject: null;')


class SharpCopySemantic(SharpLifecycleTraits):
    def __init__(self, lifecycle_traits: LifecycleTraits):
        super().__init__(lifecycle_traits)

    def __generate_copy_constructor_definition(self, out: FileGenerator, class_generator):
        out.put_line('unsafe public {class_name}({class_name} other){base_init}'.format(

            class_name=class_generator.wrap_short_name,
            base_init=get_base_init(class_generator))
        )
        with IndentScope(out):
            out.put_line('new {class_name}(ECreateFromRawPointer.force_creating_from_raw_pointer, null, false);'.format(
                class_name=class_generator.wrap_short_name, ))
            out.put_line('if (other.{get_raw}() != null)'.format(get_raw=self.params.get_raw_pointer_method_name))
            with IndentScope(out):
                copy_result = self.lifecycle_traits.init_method_exception_traits.generate_c_call(
                    out, BuiltinTypeGenerator('void*'), class_generator.copy_method,
                    ['other.{get_raw}()'.format(get_raw=self.params.get_raw_pointer_method_name)])
                out.put_line('SetObject({copy_result});'.format(copy_result=copy_result))
            out.put_line('else')
            with IndentScope(out):
                out.put_line('SetObject(null);')

    def generate_raw_copy_constructor_body_definition(self, out: FileGenerator, class_generator, copy_object):
        out.put_line('if (object_pointer != null && {copy_object})'.format(copy_object=copy_object))
        with IndentScope(out):
            copy_result = self.lifecycle_traits.init_method_exception_traits.generate_c_call(
                out, BuiltinTypeGenerator('void*'), class_generator.copy_method, ['object_pointer'])
            out.put_line('SetObject({copy_result});'.format(copy_result=copy_result))
        out.put_line('else')
        with IndentScope(out):
            out.put_line('SetObject(object_pointer);')

    def __generate_raw_copy_constructor_definition(self, out: FileGenerator, class_generator):
        constructor_arguments = 'ECreateFromRawPointer e, void *object_pointer, bool copy_object'.format(
            class_name=class_generator.wrap_name
        )
        out.put_line('unsafe public {class_name}({arguments}){base_init}'.format(
            class_name=class_generator.wrap_short_name,
            arguments=constructor_arguments,
            base_init=get_base_init(class_generator))
        )
        with IndentScope(out):
            self.generate_raw_copy_constructor_body_definition(out, class_generator, 'copy_object')

    def __generate_deallocate(self, out: FileGenerator, class_generator):
        out.put_line('if ({get_raw}() != null)'.format(
            get_raw=self.params.get_raw_pointer_method_name))
        with IndentScope(out):
            self.lifecycle_traits.finish_method_exception_traits.generate_c_call(
                out, BuiltinTypeGenerator('void'), class_generator.delete_method,
                ['{get_raw}()'.format(get_raw=self.params.get_raw_pointer_method_name)])
            out.put_line('SetObject(null);')

    def __generate_destructor(self, out: FileGenerator, class_generator):
        out.put_line('unsafe ~{class_name}()'.format(
            class_name=class_generator.wrap_short_name)
        )
        with IndentScope(out):
            self.__generate_deallocate(out, class_generator)

    def generate_std_methods_definitions(self, out: FileGenerator, class_generator):
        if self.lifecycle_traits.generate_copy_constructor(class_generator):
            self.__generate_copy_constructor_definition(out, class_generator)
            out.put_line('')
        self.__generate_raw_copy_constructor_definition(out, class_generator)
        out.put_line('')
        self.__generate_destructor(out, class_generator)
        out.put_line('')
        super().generate_std_methods_definitions(out, class_generator)


class SharpRawPointerSemantic(SharpLifecycleTraits):
    def __init__(self, lifecycle_traits: LifecycleTraits):
        super().__init__(lifecycle_traits)

    def __generate_copy_constructor_definition(self, out: FileGenerator, class_generator):
        out.put_line('unsafe public {class_short_name}({class_name} other){base_init}'.format(
            class_short_name=class_generator.wrap_short_name,
            class_name=class_generator.wrap_name,
            base_init=get_base_init(class_generator))
        )
        with IndentScope(out):
            out.put_line('SetObject(other.{get_raw}());'.format(get_raw=self.params.get_raw_pointer_method_name))

    @staticmethod
    def generate_raw_copy_constructor_body_definition(out: FileGenerator, class_generator, copy_object):
        RawPointerSemantic.generate_raw_copy_constructor_body_definition(out, class_generator, copy_object)

    @staticmethod
    def __generate_raw_copy_constructor_definition(out: FileGenerator, class_generator):
        out.put_line('unsafe public {class_name}({arguments}){base_init}'.format(
            class_name=class_generator.wrap_short_name,
            arguments='ECreateFromRawPointer e, void *object_pointer, bool copy',
            base_init=get_base_init(class_generator))
        )
        with IndentScope(out):
            RawPointerSemantic.generate_raw_copy_constructor_body_definition(out, class_generator, '')

    def __generate_delete_method(self, out: FileGenerator, class_generator):
        out.put_line('unsafe public void {delete_method}()'.format(
            delete_method=self.params.delete_method_name
        ))
        with IndentScope(out):
            out.put_line('if ({get_raw}() != null)'.format(
                get_raw=self.params.get_raw_pointer_method_name))
            with IndentScope(out):
                self.lifecycle_traits.finish_method_exception_traits.generate_c_call(
                    out, BuiltinTypeGenerator('void'), class_generator.delete_method,
                    ['{get_raw}()'.format(get_raw=self.params.get_raw_pointer_method_name)])
                out.put_line('SetObject(null);')

    def generate_std_methods_definitions(self, out: FileGenerator, class_generator):
        self.__generate_copy_constructor_definition(out, class_generator)
        out.put_line('')
        self.__generate_raw_copy_constructor_definition(out, class_generator)
        out.put_line('')
        self.__generate_delete_method(out, class_generator)
        out.put_line('')
        super().generate_std_methods_definitions(out, class_generator)


class SharpRefCountedSemantic(SharpLifecycleTraits):
    def __init__(self, lifecycle_traits: LifecycleTraits):
        super().__init__(lifecycle_traits)

    def __generate_copy_constructor_definition(self, out: FileGenerator, class_generator):
        out.put_line('unsafe public {class_short_name}({class_name} other){base_init}'.format(
            class_short_name=class_generator.wrap_short_name,
            class_name=class_generator.wrap_name,
            base_init=get_base_init(class_generator))
        )
        with IndentScope(out):
            out.put_line('SetObject(other.{get_raw}());'.format(get_raw=self.params.get_raw_pointer_method_name))
            out.put_line('if (other.{get_raw}() != null)'.format(get_raw=self.params.get_raw_pointer_method_name))
            with IndentScope(out):
                self.lifecycle_traits.init_method_exception_traits.generate_c_call(
                    out, BuiltinTypeGenerator('void'), class_generator.add_ref_method,
                    ['other.{get_raw}()'.format(get_raw=self.params.get_raw_pointer_method_name)])

    def generate_raw_copy_constructor_body_definition(self, out: FileGenerator, class_generator, add_ref_object):
        out.put_line('SetObject(object_pointer);')
        out.put_line('if ({add_ref_object} && object_pointer != null)'.format(add_ref_object=add_ref_object))
        with IndentScope(out):
            self.lifecycle_traits.init_method_exception_traits.generate_c_call(
                out, BuiltinTypeGenerator('void'), class_generator.add_ref_method, ['object_pointer'])

    def __generate_raw_copy_constructor_definition(self, out: FileGenerator, class_generator):
        constructor_arguments = 'ECreateFromRawPointer e, void *object_pointer, bool add_ref_object'
        out.put_line('unsafe public {class_name}({arguments}){base_init}'.format(
            class_name=class_generator.wrap_short_name,
            arguments=constructor_arguments,
            base_init=get_base_init(class_generator))
        )
        with IndentScope(out):
            self.generate_raw_copy_constructor_body_definition(out, class_generator, 'add_ref_object')

    def __generate_deallocate(self, out: FileGenerator, class_generator):
        out.put_line('if ({get_raw}() != null)'.format(
            get_raw=self.params.get_raw_pointer_method_name))
        with IndentScope(out):
            self.lifecycle_traits.finish_method_exception_traits.generate_c_call(
                out, BuiltinTypeGenerator('void'), class_generator.release_method,
                ['{get_raw}()'.format(get_raw=self.params.get_raw_pointer_method_name)])
            out.put_line('SetObject(null);')

    def __generate_destructor(self, out: FileGenerator, class_generator):
        out.put_line('unsafe ~{class_name}()'.format(
            class_name=class_generator.wrap_short_name)
        )
        with IndentScope(out):
            self.__generate_deallocate(out, class_generator)

    def generate_std_methods_definitions(self, out: FileGenerator, class_generator):
        self.__generate_copy_constructor_definition(out, class_generator)
        out.put_line('')
        self.__generate_raw_copy_constructor_definition(out, class_generator)
        out.put_line('')
        self.__generate_destructor(out, class_generator)
        out.put_line('')
        super().generate_std_methods_definitions(out, class_generator)


class SharpExceptionTraits(object):
    def __init__(self, exception_traits):
        self.exception_traits = exception_traits

    @staticmethod
    def generate_c_call(out: FileGenerator, return_type, c_function_name: str, arguments: [str]) -> str:
        casting_instructions, return_expression = return_type.c_2_wrap_var(
            '', NoHandling.get_c_function_call(c_function_name, arguments))
        out.put_lines(casting_instructions)
        return return_expression


class SharpFileCache(object):
    def __init__(self, file_cache, base_path: str):
        self.file_cache = file_cache
        self.base_path = base_path

    def join_to_base(self, path: str) -> str:
        result = self.base_path
        for cur_path in path:
            result = os.path.join(result, cur_path)
        return result

    @staticmethod
    def __get_file_name_base_for_namespace_common(namespace_path: [str], join_traits: PosixJoin or OsJoin) -> str:
        result_folder = join_traits.join_to_base(namespace_path)
        join_traits.create_if_required(result_folder)
        return result_folder

    def __get_file_name_for_class(self, namespace_path: [str], join_traits: PosixJoin or OsJoin) -> str:
        return join_traits.join(
            self.__get_file_name_base_for_namespace_common(namespace_path[:-1], join_traits),
            replace_template_to_filename(namespace_path[-1]) + '.cs'
        )

    def get_file_for_class(self, path_to_class: [str]) -> FileGenerator:
        output_file_name = self.__get_file_name_for_class(path_to_class, OsJoin(self.base_path))
        return self.file_cache.get_cached_generator(output_file_name)

    def __get_file_name_base_for_namespace(self, namespace_path: [str], join_traits: PosixJoin or OsJoin) -> str:
        if self.file_cache.params.namespace_header_at_parent_folder:
            return SharpFileCache.__get_file_name_base_for_namespace_common(namespace_path[:-1], join_traits)
        else:
            return SharpFileCache.__get_file_name_base_for_namespace_common(namespace_path, join_traits)

    def __get_file_name_for_enums(self, namespace_path: [str], join_traits: PosixJoin or OsJoin) -> str:
        return join_traits.join(
            self.__get_file_name_base_for_namespace(namespace_path, join_traits),
            namespace_path[-1] + self.file_cache.params.enums_header_suffix + '.cs'
        )

    def get_file_for_enums(self, path_to_namespace: [str]) -> FileGenerator:
        output_file_name = self.__get_file_name_for_enums(path_to_namespace, OsJoin(self.base_path))
        return self.file_cache.get_cached_generator(output_file_name)


def generate_requires_cast_to_base_set_object_definition(out: FileGenerator, class_generator):
    out.put_line('unsafe protected void SetObject(void* object_pointer)'.format(
        namespace=class_generator.full_wrap_name))
    with IndentScope(out):
        out.put_line('mObject = object_pointer;')
        if class_generator.base_class_generator:
            base_class = class_generator.get_base_class_wrap_name
            out.put_line('if (mObject)')
            with IndentScope(out):
                out.put_line('{base_class}.SetObject({cast_to_base}(mObject));'.format(
                    base_class=base_class,
                    cast_to_base=class_generator.cast_to_base
                ))
            out.put_line('else')
            with IndentScope(out):
                out.put_line('{base_class}.SetObject(null);'.format(base_class=base_class))


def generate_simple_case_set_object_definition(out: FileGenerator, class_generator):
    out.put_line('unsafe protected void {class_name}.SetObject(void* object_pointer)'.format(
        class_name=class_generator.full_wrap_name))
    with IndentScope(out):
        if class_generator.base_class_generator:
            out.put_line('{base_class}.SetObject(object_pointer);'.format(
                base_class=class_generator.base_class_generator.full_wrap_name))
        else:
            out.put_line('mObject = object_pointer;')


def generate_set_object_definition(inheritance_traits, out: FileGenerator, class_generator):
    if isinstance(inheritance_traits, RequiresCastToBase):
        generate_requires_cast_to_base_set_object_definition(out, class_generator)
    else:
        generate_simple_case_set_object_definition(out, class_generator)


def get_base_init(class_generator):
    if class_generator.base_class_generator:
        return ' : {0}({0}.{1}, null, false)'.format(
            class_generator.base_class_generator.full_wrap_name,
            'ECreateFromRawPointer.force_creating_from_raw_pointer'
        )
    else:
        return ''


sharp_lifecycles = {}

str_to_sharp_lifecycle = {
    TLifecycle.copy_semantic: SharpCopySemantic,
    TLifecycle.raw_pointer_semantic: SharpRawPointerSemantic,
    TLifecycle.reference_counted: SharpRefCountedSemantic
}


def create_sharp_lifecycle(lifecycle: TLifecycle, lifecycle_traits: LifecycleTraits) -> SharpLifecycleTraits:
    if lifecycle not in sharp_lifecycles:
        result = str_to_sharp_lifecycle[lifecycle](lifecycle_traits)
        sharp_lifecycles[lifecycle] = result
    else:
        result = sharp_lifecycles[lifecycle]
    return result


def generate(file_cache: FileCache, capi_generator: CapiGenerator, namespace_generators: []):
    for namespace_generator in namespace_generators:
        namespace = SharpNamespace(namespace_generator)
        namespace.generate(file_cache, capi_generator)
