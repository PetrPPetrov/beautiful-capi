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

import copy
import os

import ExceptionTraits
import ExternalClassGenerator
import ExternalNamespaceGenerator
from NamespaceGenerator import NamespaceGenerator
import CapiGenerator
from ClassGenerator import ClassGenerator
from LifecycleTraits import LifecycleTraits, RawPointerSemantic, RefCountedSemantic
from ArgumentGenerator import ArgumentGenerator, MappedTypeGenerator, ClassTypeGenerator, ExternalClassTypeGenerator, \
    EnumTypeGenerator
from BuiltinTypeGenerator import BuiltinTypeGenerator
from MethodGenerator import MethodGenerator, ConstructorGenerator, FunctionGenerator, IndexerGenerator
from FileGenerator import FileGenerator, IndentScope, Indent, WatchdogScope
from Helpers import if_required_then_add_empty_line, bool_to_str, replace_template_to_filename, BeautifulCapiException
from Helpers import get_template_name, pascal_to_stl
from Parser import TLifecycle, TMappedType
from InheritanceTraits import RequiresCastToBase
from ExceptionTraits import NoHandling
from FileCache import FileCache, OsJoin, PosixJoin
from TemplateGenerator import TemplateGenerator
from ThisArgumentGenerator import ThisArgumentGenerator


class SharpCapiGenerator(object):
    def __init__(self, file_cache, capi_generator: CapiGenerator):
        self.file_cache = file_cache
        self.capi_generator = capi_generator
        self.params = capi_generator.params
        self.no_handling_exception_traits = SharpExceptionTraits(capi_generator.no_handling_exception_traits,
                                                                 self.params)
        self.main_exception_traits = SharpExceptionTraits(capi_generator.main_exception_traits, self.params)
        self.root_namespaces = []
        self.full_name_2_sharp_object = {}
        self.generate_string_marshaler = False

    def get_exception_traits(self, no_except: bool):
        if no_except:
            return self.no_handling_exception_traits
        return self.main_exception_traits

    def export_function_arguments(self, argument_generators: []):
        result = []
        for argument in argument_generators:
            generator = argument.argument_generator.type_generator
            arg = argument.get_marshaling()
            if isinstance(generator, MappedTypeGenerator):
                mapped_type = self.get_or_gen_mapped_type(generator.name, generator.mapped_type_object)
                arg += mapped_type.wrap_argument_declaration() + ' ' + argument.argument_generator.name
            else:
                arg += argument.c_argument_declaration()
            result.append(arg)
        return result

    def get_or_gen_namespace(self, fullname: str, generator: NamespaceGenerator):
        if fullname in self.full_name_2_sharp_object:
            return self.full_name_2_sharp_object[fullname]
        else:
            if generator.parent_namespace:
                parent = self.get_or_gen_namespace('.'.join(generator.parent_namespace.full_name_array),
                                                   generator.parent_namespace)
                result = SharpNamespace(generator, parent, self)
            else:
                result = SharpNamespace(generator, None, self)
            self.full_name_2_sharp_object[fullname] = result
            return result

    def get_or_gen_class(self, fullname: str, generator: ClassGenerator):
        if fullname in self.full_name_2_sharp_object:
            return self.full_name_2_sharp_object[fullname]
        else:
            namespace = self.get_or_gen_namespace('.'.join(generator.parent_namespace.full_name_array),
                                                  generator.parent_namespace)
            result = SharpClass(generator, namespace, self)
            self.full_name_2_sharp_object[fullname] = result
            return result

    def get_or_gen_template(self, fullname: str, template_generator: TemplateGenerator):
        result = self.full_name_2_sharp_object.get(fullname, None)
        if not result:
            namespace = self.get_or_gen_namespace('.'.join(template_generator.parent_namespace.full_name_array),
                                                  template_generator.parent_namespace)
            result = SharpTemplate(template_generator, namespace, self)
            self.full_name_2_sharp_object[fullname] = result
        return result

    def get_or_gen_external_namespace(self, fullname: str, generator: ExternalNamespaceGenerator):
        if fullname in self.full_name_2_sharp_object:
            return self.full_name_2_sharp_object[fullname]
        else:
            if generator.parent_namespace:
                parent = self.get_or_gen_external_namespace(generator.parent_namespace.full_wrap_name,
                                                            generator.parent_namespace)
                result = SharpExternalNamespace(generator, parent, self)
            else:
                result = SharpExternalNamespace(generator, None, self)
            self.full_name_2_sharp_object[fullname] = result
            return result

    def get_or_gen_external_class(self, fullname: str, external_class_generator: ExternalClassGenerator):
        if fullname in self.full_name_2_sharp_object:
            return self.full_name_2_sharp_object[fullname]
        else:
            namespace = self.get_or_gen_external_namespace(
                '.'.join(external_class_generator.parent_namespace.full_name_array),
                external_class_generator.parent_namespace)
            result = SharpExternalClass(external_class_generator, namespace, self)
            self.full_name_2_sharp_object[fullname] = result
            namespace.classes.append(result)
            return result

    def get_or_gen_mapped_type(self, name: str, mapped_type_object: TMappedType):
        result = self.full_name_2_sharp_object.get(name, None)
        if not result:
            result = SharpMappedType(mapped_type_object)
            self.full_name_2_sharp_object[name] = result
        return result

    def generate__check_and_throw_exception__function(self, out: FileGenerator):
        exception_traits = self.main_exception_traits.exception_traits
        if not isinstance(exception_traits, ExceptionTraits.ByFirstArgument):
            return
        out.put_line('')
        out.put_line('public static unsafe void check_and_throw_exception(uint exception_code, IntPtr exception_object)')
        with IndentScope(out):
            out.put_line('switch (exception_code)')
            with IndentScope(out):
                out.put_line('case 0:')
                with Indent(out):
                    out.put_line('return;')
                out.put_line('case 1:')
                with Indent(out):
                    out.put_line('throw new System.Exception("unknown exception");')
                out.put_line('case 2:')
                with Indent(out):
                    out.put_line('throw new System.Exception("exception during copying exception object");')
                code_to_exception = {class_.exception_code: class_ for class_ in exception_traits.exception_classes}
                for code, exception_class in code_to_exception.items():
                    sharp_class = self.get_or_gen_class('.'.join(exception_class.full_template_name_array),
                                                        exception_class)
                    out.put_line('case {0}:'.format(code))
                    with Indent(out):
                        out.put_line('throw new {0}({0}.{1}, exception_object, false);'.format(
                            sharp_class.full_wrap_name,
                            'ECreateFromRawPointer.force_creating_from_raw_pointer'))
                out.put_line('default:')
                with Indent(out):
                    out.put_line('throw new System.Exception("unknown exception code");')

    def generate_exception_traits(self):
        params = self.params
        if isinstance(self.main_exception_traits.exception_traits, NoHandling):
            return

        project_name = pascal_to_stl(self.capi_generator.api_root.project_name)
        filename = params.sharp_output_folder + '/' + params.check_and_throw_exception_filename.format(
            project_name=project_name).replace('.h', '.cs')
        out = FileGenerator(filename)
        out.put_line('using System;')
        out.put_line('')
        self.main_exception_traits.generate_exception_info(out)
        self.main_exception_traits.generate_exception_code(self, out)
        out.put_line('namespace {}'.format(self.params.beautiful_capi_namespace))
        with IndentScope(out):
            out.put_line('public static partial class Functions')
            with IndentScope(out):
                self.generate__check_and_throw_exception__function(out)

    def __generate(self, namespace_generators):
        namespaces = []
        for namespace in namespace_generators:
            sharp_namespace = self.get_or_gen_namespace('.'.join(namespace.full_name_array), namespace)
            sharp_namespace.generate()
            namespaces.append(sharp_namespace)
        self.root_namespaces = namespaces

    def __generate_string_marshaler(self):
        if self.generate_string_marshaler:
            namespace = self.params.beautiful_capi_namespace
            definition_header = self.file_cache.get_file_for_class([namespace, 'StringMarshaler'])
            definition_header.put_begin_cpp_comments(self.params)
            definition_header.put_line('using System;')
            definition_header.put_line('using System.Runtime.InteropServices;\n')
            definition_header.put_line('namespace {}'.format(namespace))
            with IndentScope(definition_header):
                definition_header.put_line('class StringMarshaler : ICustomMarshaler')
                with IndentScope(definition_header):
                    definition_header.put_line('public object MarshalNativeToManaged(IntPtr pNativeData)')
                    with IndentScope(definition_header, ending='}\n'):
                        definition_header.put_line('return Marshal.PtrToStringAnsi(pNativeData);')
                    definition_header.put_line('public IntPtr MarshalManagedToNative(object ManagedObj)')
                    with IndentScope(definition_header, ending='}\n'):
                        definition_header.put_line('return IntPtr.Zero;')
                    definition_header.put_line('public void CleanUpNativeData(IntPtr pNativeData)')
                    with IndentScope(definition_header, ending='}\n'):
                        pass
                    definition_header.put_line(' public void CleanUpManagedData(object ManagedObj)')
                    with IndentScope(definition_header, ending='}\n'):
                        pass
                    definition_header.put_line('public int GetNativeDataSize()')
                    with IndentScope(definition_header, ending='}\n'):
                        definition_header.put_line('return IntPtr.Size;')
                    definition_header.put_line('static readonly StringMarshaler instance = new StringMarshaler();\n')
                    definition_header.put_line('public static ICustomMarshaler GetInstance(string cookie)')
                    with IndentScope(definition_header):
                        definition_header.put_line('return instance;')

    def generate_string_marshaling(self, out: FileGenerator, return_type: str,):
        if return_type == 'string':
            self.generate_string_marshaler = True
            expr = '[return: MarshalAs(UnmanagedType.CustomMarshaler, MarshalTypeRef = typeof({}.StringMarshaler))]'
            out.put_line(expr.format(self.params.beautiful_capi_namespace))

    def generate_definition(self):
        for namespace in self.root_namespaces:
            namespace.generate_definition()
        self.__generate_string_marshaler()

    def generate(self, root_namespaces: [NamespaceGenerator]):
        self.__generate(root_namespaces)
        self.generate_definition()


class SharpNamespace(object):
    def __init__(self, namespace_generator: NamespaceGenerator, parent_namespace, capi_generator: SharpCapiGenerator):
        self.namespace_generator = namespace_generator
        self.parent_namespace = parent_namespace
        self.nested_namespaces = {}
        self.classes = {}
        self.enums = []
        self.functions = []
        self.capi_generator = capi_generator
        self.wrap_name = namespace_generator.wrap_name
        self.full_wrap_name = '.'.join(namespace_generator.full_name_array)
        self.mapped_types = {}
        self.templates = {}
        self.external_namespaces = []

    def get_object(self, name: str):
        if name in self.classes:
            return self.classes[name]
        if name in self.mapped_types:
            return self.mapped_types[name]
        if name in self.templates:
            return self.templates[name]
        if name in self.nested_namespaces:
            return self.nested_namespaces[name]
        return None

    def find_object(self, name_array: [str]):
        if name_array:
            result = self.get_object(name_array[0])
            if len(name_array) == 1:
                if not result and self.parent_namespace:
                    result = self.parent_namespace.find_object(name_array)
            else:
                # if length > 1 then result - namespace
                if result:
                    result = result.find_object(name_array[1:])
                else:
                    if self.parent_namespace:
                        if name_array[0] == self.parent_namespace.wrap_name:
                            result = self.parent_namespace.find_object(name_array[1:])
                        else:
                            result = self.parent_namespace.find_object(name_array)
            return result

    @property
    def full_name_array(self):
        return self.namespace_generator.full_name_array

    def get_class(self, name: str):
        result = self.classes.get(name, None)
        if not result and self.parent_namespace:
            result = self.parent_namespace.get_class(name)
        return result

    def get_namespace(self, name: str):
        result = self.nested_namespaces.get(name, None)
        if not result and self.parent_namespace:
            result = self.parent_namespace.get_namespace(name)
        return result

    def get_mapped_type(self, name: str):
        result = self.mapped_types.get(name, None)
        if not result and self.parent_namespace:
            result = self.parent_namespace.get_mapped_type(name)
        return result

    def get_template(self, name: str):
        result = self.templates.get(name, None)
        if not result and self.parent_namespace:
            result = self.parent_namespace.get_template(name)
        return result

    def __generate_initialisation_class(self):
        file = self.capi_generator.file_cache.get_file_for_class(self.full_name_array + [self.wrap_name + 'Init'])
        file.put_begin_cpp_comments(self.namespace_generator.params)
        file.put_line('using System.Runtime.InteropServices;')
        file.put_line('using System;')
        file.put_line('')
        self.increase_indent_recursively(file)
        file.put_line('public class Initialization')
        with IndentScope(file):
            api_root = self.capi_generator.capi_generator.api_root
            file.put_line('const int MAJOR_VERSION = {0};'.format(api_root.major_version))
            file.put_line('const int MINOR_VERSION = {0};'.format(api_root.minor_version))
            file.put_line('const int PATCH_VERSION = {0};'.format(api_root.patch_version))
            file.put_line('')
            file.put_line('public Initialization()')
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
                    file.put_line('throw new System.Exception(message);')
            file.put_line('')
        self.decrease_indent_recursively(file)

    def __generate_functions_class(self):
        file_name = self.full_name_array[:-1] + [self.wrap_name + 'Functions']
        out = self.capi_generator.file_cache.get_file_for_class(file_name)
        out.put_begin_cpp_comments(self.namespace_generator.params)
        out.put_line('using System;\n')
        out.put_line('using System.Reflection;\n')
        out.put_line('using System.Runtime.InteropServices;')
        out.put_line('')
        self.increase_indent_recursively(out)
        out.put_line('public static partial class Functions')
        with IndentScope(out):
            import_string = '[DllImport("{dll_name}.dll", CallingConvention = {calling_convention})]'.format(
                dll_name=self.namespace_generator.params.shared_library_name,
                calling_convention='CallingConvention.Cdecl'  # now used only cdecl convention
            )
            for func in self.functions:
                out.put_line(import_string)
                return_type_marshaling = func.get_return_marshaling()
                if return_type_marshaling:
                    out.put_line(return_type_marshaling)
                arguments = self.capi_generator.export_function_arguments(func.arguments)
                exception_traits = self.capi_generator.get_exception_traits(
                    func.generator.function_object.noexcept)
                exception_traits.modify_c_arguments(arguments)
                self.capi_generator.generate_string_marshaling(out,
                                                               return_type=func.return_type.wrap_argument_declaration())
                out.put_line('unsafe static extern {return_type} {name}({arguments});'.format(
                    return_type=func.return_type.c_argument_declaration(),
                    name=func.generator.full_c_name,
                    arguments=', '.join(arguments)
                ))
            out.put_line('')
            for func in self.functions:
                func.generate_wrap_definition(out)
            for class_ in self.classes.values():
                if class_.class_generator.is_callback:
                    class_.generate__create_callback__method(out)
        self.decrease_indent_recursively(out)

    def generate_enums_header(self):
        file_cache = self.capi_generator.file_cache
        enums_header = file_cache.get_file_for_enums(self.full_name_array)
        enums_header.put_begin_cpp_comments(file_cache.file_cache.params)
        return enums_header

    def generate(self):
        self.enums = [SharpEnum(enum, self) for enum in self.namespace_generator.enum_generators]
        for mapped_type in self.namespace_generator.namespace_object.mapped_types:
            name = mapped_type.name
            self.mapped_types[name] = self.capi_generator.get_or_gen_mapped_type(name, mapped_type)
        self.external_namespaces = []
        for ns in self.namespace_generator.external_namespaces:
            external_namespace = self.capi_generator.get_or_gen_external_namespace('.'.join(ns.full_name_array), ns)
            self.external_namespaces.append(external_namespace)
            external_namespace.generate()
        template_generators = []
        for template_generator in self.namespace_generator.templates:
            template_generators.append(template_generator)
            for extension in template_generator.template_object.classes[0].lifecycle_extensions:
                new_class = copy.deepcopy(template_generator.template_object.classes[0])
                new_class.name = extension.name[:extension.name.find('<')]
                new_class.lifecycle = extension.lifecycle
                new_class.lifecycle_filled = True
                new_class.wrap_name = extension.wrap_name
                new_class.wrap_name_filled = extension.wrap_name_filled
                new_class.cast_tos = copy.deepcopy(extension.cast_tos)
                new_class.lifecycle_extensions = []
                new_class.lifecycle_extension = extension
                new_class.extension_base_class_name = '::'.join(self.full_name_array)
                new_class.down_cast = extension.down_cast
                new_class.down_cast_filled = True
                new_template_object = copy.deepcopy(template_generator.template_object)
                new_template_object.classes[0] = new_class
                new_template_generator = TemplateGenerator(new_template_object, template_generator.parent_namespace,
                                                           template_generator.params)
                template_generators.append(new_template_generator)
        for template_generator in template_generators:
            if template_generator.template_object.wrap_csharp_templates:
                generator = template_generator.template_class_generator
                template = self.capi_generator.get_or_gen_template(
                    '.'.join(generator.full_name_array), template_generator)
                self.templates[generator.name] = template
        for cur_class in self.namespace_generator.classes:
            full_class_name = '.'.join(cur_class.full_template_name_array).replace('::', '.')
            sharp_class = self.capi_generator.get_or_gen_class(full_class_name, cur_class)
            if sharp_class.is_template:
                template_name = get_template_name(cur_class.name)
                template = self.get_template(template_name)
                if template:
                    template.classes.append(sharp_class)
                    self.templates[template_name] = template
            else:
                self.classes['.'.join(cur_class.full_template_name_array)] = sharp_class
            sharp_class.generate()
        for template in self.templates.values():
            template.generate()
        self.functions = [SharpFunction(func, self) for func in self.namespace_generator.functions]
        for namespace in self.namespace_generator.nested_namespaces:
            sharp_namespace = self.capi_generator.get_or_gen_namespace('.'.join(namespace.full_name_array), namespace)
            self.nested_namespaces[namespace.name] = sharp_namespace
            sharp_namespace.generate()

    def generate_definition(self):
        if self.enums:
            enums_header = self.generate_enums_header()
            self.increase_indent_recursively(enums_header)
            for enum in self.enums:
                enum.generate_enum_definition(enums_header)
            self.decrease_indent_recursively(enums_header)
        if not self.parent_namespace:
            self.__generate_initialisation_class()
        if self.functions:
            for func in self.functions:
                func.generate()
        self.__generate_functions_class()
        for class_generator in self.classes.values():
            class_generator.generate_definition()
        for template in self.templates.values():
            template.generate_definition()
        for nested_namespace in self.nested_namespaces.values():
            nested_namespace.generate_definition()

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
    def __init__(self, class_generator: ClassGenerator, namespace: SharpNamespace, capi_generator: SharpCapiGenerator):
        self.class_generator = class_generator
        self.namespace = namespace
        self.constructors = []
        self.methods = []
        self.indexers = []
        self.capi_generator = capi_generator
        self.copy_or_add_ref_when_c_2_wrap = False
        self.lifecycle_traits = create_sharp_lifecycle(class_generator.class_object.lifecycle,
                                                       class_generator.lifecycle_traits,
                                                       namespace.capi_generator)
        self.enums = []
        self.base = None
        self.force_typedef_as_name = False
        if hasattr(self.class_generator.class_object, 'wrap_csharp_templates'):
            if not self.class_generator.class_object.wrap_csharp_templates:
                self.force_typedef_as_name = True
        self.__template_arguments = []

    @property
    def is_template(self):
        if self.force_typedef_as_name:
            return False
        return self.class_generator.is_template

    @staticmethod
    def template_2_wrap(name: str) -> str:
        result = name
        result = result.replace('<', '_')
        result = result.replace('>', '')
        result = result.replace('::', '_')
        result = result.replace(' ', '')
        result = result.replace(',', '_')
        return result

    @property
    def wrap_name(self):
        previous_wrap_name = self.template_2_wrap(self.template_name) if self.is_template else self.class_generator.wrap_name
        if self.force_typedef_as_name:
            return self.class_generator.class_object.typedef_name
        return previous_wrap_name

    @property
    def wrap_short_name(self):
        previous_wrap_name = self.class_generator.wrap_short_name if self.is_template else self.class_generator.wrap_name
        if self.force_typedef_as_name:
            return self.class_generator.class_object.typedef_name
        return previous_wrap_name

    @property
    def full_name_array(self):
        return self.namespace.full_name_array + [self.wrap_name]

    @property
    def full_wrap_name(self):
        return self.namespace.full_wrap_name + '.' + self.wrap_name

    @property
    def c_name(self):
        return self.class_generator.c_name

    @property
    def template_name(self):
        result = self.class_generator.class_object.typedef_name
        if not result:
            base_path = self.namespace.full_name_array
            arguments = ', '.join(arg.wrap_argument_declaration(base_path) for arg in self.template_arguments)
            result = '{name}<{arguments}>'.format(name=self.class_generator.wrap_short_name, arguments=arguments)
        else:
            result += self.class_generator.lifecycle_traits.suffix
        return result

    @property
    def full_template_name(self):
        return '.'.join([self.namespace.full_wrap_name, self.template_name])

    @staticmethod
    def get_relative_name_array(base: [str], name: [str]) -> [str]:
        if base and name:
            for index, (item1, item2) in enumerate(zip(base, name)):
                if item1 != item2:
                    return name[index:]
        return name[len(base):]

    @staticmethod
    def get_relative_name(base: [str], name: [str]) -> str:
        name_array = SharpClass.get_relative_name_array(base, name)
        return '.'.join(name_array)

    def gen_base_class(self):
        base = self.class_generator.base_class_generator
        if base:
            base_class_name = '.'.join(base.full_template_name_array).replace('::', '.')
            self.base = self.capi_generator.get_or_gen_class(base_class_name, base)

    def wrap_argument_declaration(self) -> str:
        return self.full_wrap_name

    @staticmethod
    def c_argument_declaration() -> str:
        return 'IntPtr'

    def c_2_wrap_var(self, result_var: str, expression: str) -> ([str], str):
        parent_full_name = '.'.join(self.namespace.full_name_array)
        internal_expression = '{type_name}.{create_from_ptr_expression}, {expression}, {copy_or_add_ref}'.format(
            create_from_ptr_expression='ECreateFromRawPointer.force_creating_from_raw_pointer',
            type_name=parent_full_name + '.' + self.wrap_name,
            expression=expression,
            copy_or_add_ref=bool_to_str(self.copy_or_add_ref_when_c_2_wrap)
        )
        if result_var:
            return ['var {result_var} = new {type_name}({internal_expression});'.format(
                type_name=parent_full_name + '.' + self.wrap_name,
                result_var=result_var,
                internal_expression=internal_expression
            )], result_var
        else:
            return [], 'new {type_name}({internal_expression})'.format(
                type_name=parent_full_name + '.' + self.wrap_name,
                internal_expression=internal_expression
            )

    def wrap_2_c_var(self, result_var: str, expression: str) -> ([str], str):
        internal_expression = '{expression}.{get_raw_pointer_method}()'.format(
            expression=expression,
            get_raw_pointer_method=self.class_generator.get_raw_pointer_method_name)
        if result_var:
            return ['IntPtr {result_var} = {internal_expression};'.format(
                result_var=result_var,
                internal_expression=internal_expression
            )], result_var
        else:
            return [], internal_expression

    def __generate_callback_delegates(self, out: FileGenerator):
        if self.class_generator.is_callback:
            for method in self.base.methods:
                name = method.generator.full_c_name + '_callback_type'
                # [arg.c_argument_declaration() for arg in method.arguments]
                arguments = ['IntPtr object_pointer'] + self.capi_generator.export_function_arguments(method.arguments)
                method.exception_traits.modify_c_arguments(arguments)
                return_type = method.return_type.c_argument_declaration()
                out.put_line('[UnmanagedFunctionPointer(CallingConvention.Cdecl)]')
                return_type_marshaling = method.get_return_marshaling()
                if return_type_marshaling:
                    out.put_line(return_type_marshaling)
                out.put_line('unsafe public delegate {0} {1}({2});'.format(return_type, name, ', '.join(arguments)))
                out.put_line('public {0} {1}_callback;'.format(name, method.generator.c_name))
            if isinstance(self.lifecycle_traits, SharpRefCountedSemantic):
                add_ref_func_name = self.base.class_generator.full_c_name + '_add_ref_callback_type'
                release_func_name = self.base.class_generator.full_c_name + '_release_callback_type'
                out.put_line('[UnmanagedFunctionPointer(CallingConvention.Cdecl)]')
                out.put_line('unsafe public delegate void {}(IntPtr object_pointer);'.format(add_ref_func_name))
                out.put_line('[UnmanagedFunctionPointer(CallingConvention.Cdecl)]')
                out.put_line('unsafe public delegate void {}(IntPtr object_pointer);'.format(release_func_name))

            out.put_line('')

    def __generate_down_cast(self, out: FileGenerator):
        class_ = self
        while class_.base:
            out.put_line('')
            base_name = class_.base.full_wrap_name
            out.put_line('new unsafe static public {0} DownCast({1} source_object)'.format(self.wrap_name, base_name))
            with IndentScope(out):
                out.put_line('return new {0}({0}.{1}, {2}(source_object.{3}()), true);'.format(
                    self.wrap_name,
                    'ECreateFromRawPointer.force_creating_from_raw_pointer',
                    '{0}_cast_to_{1}'.format(class_.base.class_generator.full_c_name, self.class_generator.full_c_name),
                    class_.base.class_generator.get_raw_pointer_method_name))
            class_ = class_.base

    def __generate_cast_name_declaration(self, out: FileGenerator):
        def generate_cast(from_operand, to_operand, implicit: bool):
            out.put_line('')
            out.put_line('unsafe public static {implicit} operator {target_type}({source_type} value)'.format(
                target_type=to_operand,
                source_type=from_operand,
                implicit='implicit' if implicit else 'explicit'
            ))
            with IndentScope(out):
                expr = 'return new {0}({0}.ECreateFromRawPointer.force_creating_from_raw_pointer, value.{1}(), true);'
                out.put_line(expr.format(to_operand, self.capi_generator.params.get_raw_pointer_method_name))
        base_name = self.namespace.full_name_array
        for cast in self.class_generator.class_object.lifecycle_extension.cast_tos:
            target = cast.target_generator
            target_type = (target.parent_namespace.full_wrap_name + '.' + target.template_name).replace('::', '.')
            sharp_class = self.capi_generator.get_or_gen_class(target_type, cast.target_generator)
            generate_cast(self.wrap_name,
                          SharpClass.get_relative_name(base_name, sharp_class.full_name_array),
                          cast.implicit)
        for cast in self.class_generator.class_object.lifecycle_extension.cast_froms:
            source = cast.source_generator
            source_type = (source.parent_namespace.full_wrap_name + '.' + source.template_name).replace('::', '.')
            sharp_class = self.capi_generator.get_or_gen_class(source_type, cast.source_generator)
            generate_cast(SharpClass.get_relative_name(base_name, sharp_class.full_name_array), self.wrap_name, True)

    def __generate_definition(self, out: FileGenerator):
        out.put_begin_cpp_comments(self.class_generator.params)
        out.put_line('using System;\n')
        out.put_line('using System.Runtime.InteropServices;\n')
        self.namespace.increase_indent_recursively(out)
        base = ': {}'.format(self.base.full_wrap_name) if self.base else ''
        if not base and self.class_generator.class_object.exception:
            base = ': System.Exception'
        out.put_line('public class {class_name}{base} '.format(class_name=self.wrap_name, base=base))
        with IndentScope(out):
            self.__generate_callback_delegates(out)
            self.__generate_extern_functions(out)
            out.put_line('')
            new = 'new ' if self.base else ''
            out.put_line('%spublic enum ECreateFromRawPointer{force_creating_from_raw_pointer};' % new)
            out.put_line('')
            generate_object_field_definition(self.class_generator.inheritance_traits, out, self)
            out.put_line('')
            for enum in self.enums:
                enum.generate_enum_definition(out)
            first_method = True
            first_method = self.__generate_constructor_definitions(out, first_method)
            self.__generate_method_definitions(out, first_method)
            out.put_line('')
            self.__generate_indexer_definitions(out, first_method)
            out.put_line('')
            self.lifecycle_traits.generate_std_methods_definitions(out, self)
            out.put_line('')
            if hasattr(self, 'extension_base_class_generator'):
                self.class_generator.generate_cast_name_definition(out)
                out.put_line('')
            generate_set_object_definition(self.class_generator.inheritance_traits, out, self)
            self.__generate_down_cast(out)
            if hasattr(self.class_generator, 'extension_base_class_generator'):
                self.__generate_cast_name_declaration(out)
            if self.is_template:
                out.put_line('')
                template_name = self.namespace.full_wrap_name + '.' + self.wrap_short_name
                template_name += '<' + ', '.join(
                    arg.wrap_argument_declaration() for arg in self.template_arguments) + '>'
                out.put_line('unsafe public static implicit operator {0}({1} certain_class)'.format(
                        template_name, self.full_wrap_name))
                with IndentScope(out):
                    out.put_line('return new {0}({0}.ECreateFromObject.create_from_object, certain_class);'.format(
                        template_name))
                out.put_line('')
                out.put_line('unsafe public static implicit operator {0}({1} generic)'.format(
                    self.full_wrap_name, template_name))
                with IndentScope(out):
                    out.put_line('return ({})generic.GetCertainClass();'.format(self.full_wrap_name))
        self.namespace.decrease_indent_recursively(out)

    def __generate_constructor_definitions(self, definition_header, first_method):
        for constructor_generator in self.constructors:
            first_method = if_required_then_add_empty_line(first_method, definition_header)
            constructor_generator.generate_wrap_definition(definition_header, self.class_generator.capi_generator)
        return first_method

    def __generate_method_definitions(self, definition_header, first_method):
        for method in self.methods:
            first_method = if_required_then_add_empty_line(first_method, definition_header)
            method.generate_wrap_definition(definition_header)

    def __generate_indexer_definitions(self, definition_header, first_indexer):
        for indexer in self.indexers:
            first_indexer = if_required_then_add_empty_line(first_indexer, definition_header)
            indexer.generate_wrap_definition(definition_header)

    def __generate_init_deinit_externs(self, out: FileGenerator):
        import_string = '[DllImport("{dll_name}.dll", CallingConvention = {calling_convention})]'.format(
            dll_name=self.class_generator.params.shared_library_name,
            calling_convention='CallingConvention.Cdecl')  # now used only cdecl convention
        sharp_capi = self.namespace.capi_generator
        class_object = self.class_generator.class_object
        if class_object.copy_or_add_ref_noexcept_filled:
            init_traits = sharp_capi.get_exception_traits(class_object.copy_or_add_ref_noexcept)
            deinit_traits = sharp_capi.get_exception_traits(class_object.delete_or_release_noexcept)
        else:
            lifecycle_traits = self.class_generator.lifecycle_traits
            init_traits = sharp_capi.get_exception_traits(lifecycle_traits.default_value_for_init_noexcept)
            deinit_traits = sharp_capi.get_exception_traits(lifecycle_traits.default_value_for_finish_noexcept)

        if isinstance(self.class_generator.lifecycle_traits, RefCountedSemantic):
            out.put_line(import_string)
            arguments = ['IntPtr object_pointer']
            init_traits.modify_c_arguments(arguments)
            out.put_line('unsafe static extern void {func_name}({arguments});'.format(
                func_name=self.class_generator.add_ref_method, arguments=', '.join(arguments)))
            out.put_line(import_string)
            arguments = ['IntPtr object_pointer']
            deinit_traits.modify_c_arguments(arguments)
            out.put_line('unsafe static extern void {func_name}({arguments});'.format(
                func_name=self.class_generator.release_method, arguments=', '.join(arguments)))
        else:
            out.put_line(import_string)
            arguments = ['IntPtr object_pointer']
            init_traits.modify_c_arguments(arguments)
            out.put_line('unsafe static extern IntPtr {func_name}({arguments});'.format(
                func_name=self.class_generator.copy_method, arguments=', '.join(arguments)))
            out.put_line(import_string)
            arguments = ['IntPtr object_pointer']
            deinit_traits.modify_c_arguments(arguments)
            out.put_line('unsafe static extern void {func_name}({arguments});'.format(
                func_name=self.class_generator.delete_method, arguments=', '.join(arguments)))

    def __generate_extern_functions(self, out: FileGenerator):
        import_string = '[DllImport("{dll_name}.dll", CallingConvention = {calling_convention})]'.format(
            dll_name=self.class_generator.params.shared_library_name,
            calling_convention='CallingConvention.Cdecl')  # now used only cdecl convention
        for constructor in self.constructors:
            out.put_line(import_string)
            arguments = self.capi_generator.export_function_arguments(constructor.arguments)
            constructor.exception_traits.modify_c_arguments(arguments)
            out.put_line('unsafe static extern IntPtr {class_name}({arguments});'.format(
                class_name=constructor.generator.full_c_name,
                arguments=', '.join(arguments)))
        for method in self.methods:
            out.put_line(import_string)
            return_type_marshaling = method.get_return_marshaling()
            if return_type_marshaling:
                out.put_line(return_type_marshaling)
            arguments = ['IntPtr object_pointer'] + self.capi_generator.export_function_arguments(method.arguments)
            method.exception_traits.modify_c_arguments(arguments)
            self.capi_generator.generate_string_marshaling(out,
                                                           return_type=method.return_type.wrap_argument_declaration())
            out.put_line('unsafe static extern {return_type} {name}({arguments});'.format(
                return_type=method.return_type.c_argument_declaration(),
                name=method.generator.full_c_name,
                arguments=', '.join(arguments)))
        for indexer in self.indexers:
            return_type_marshaling = indexer.get_return_marshaling()
            if return_type_marshaling:
                out.put_line(return_type_marshaling)
            arguments = ['IntPtr object_pointer'] + self.capi_generator.export_function_arguments(indexer.arguments)
            indexer.exception_traits.modify_c_arguments(arguments)
            self.capi_generator.generate_string_marshaling(out,
                                                           return_type=indexer.set_type.wrap_argument_declaration())
            out.put_line(import_string)
            out.put_line('unsafe static extern {return_type} {name}({arguments});'.format(
                return_type=indexer.set_type.c_argument_declaration(),
                name=indexer.generator.full_c_name(True),
                arguments=', '.join(arguments)))
            self.capi_generator.generate_string_marshaling(out,
                                                           return_type=indexer.get_type.wrap_argument_declaration())
            out.put_line(import_string)
            out.put_line('unsafe static extern {return_type} {name}({arguments});'.format(
                return_type=indexer.get_type.c_argument_declaration(),
                name=indexer.generator.full_c_name(False),
                arguments=', '.join(arguments)))
        self.__generate_init_deinit_externs(out)
        if self.base:
            out.put_line(import_string)
            out.put_line('unsafe static extern IntPtr {func_name}(IntPtr object_pointer);'.format(
                func_name=self.class_generator.cast_to_base))
        class_ = self
        while class_.base:
            out.put_line(import_string)
            func = '{0}_cast_to_{1}'.format(class_.base.class_generator.full_c_name, self.class_generator.full_c_name,)
            out.put_line('unsafe static extern IntPtr {}(IntPtr object_pointer);'.format(func))
            class_ = class_.base

    @staticmethod
    def __sort_exceptions(exceptions: []):
        result = []

        def add_exception(element):
            if element not in result:
                if element.base:
                    if element.base in exceptions:
                        add_exception(element.base)
                        result.insert(result.index(element.base), element)
                else:
                    result.append(element)

        for exception in exceptions:
            add_exception(exception)
        return result

    def __generate_method_callback(self, method, out: FileGenerator):
        if not method.return_type:
            method.generate()
        class_name = self.base.class_generator.c_name
        impl_class = 'ImplementationClass'
        return_type = method.return_type.c_argument_declaration()
        out.put_line('unsafe static {0} {1}<{2}>(out {3} exception_info, {4})'.format(
            return_type,
            '{0}_{1}_callback'.format(class_name, method.generator.c_name),
            impl_class,
            method.exception_traits.exception_info_t(),
            ', '.join(['IntPtr object_pointer'] + [arg.c_argument_declaration() for arg in method.arguments])))
        with IndentScope(out):
            out.put_line('try')
            with IndentScope(out):
                out.put_line('exception_info.code = 0;')
                out.put_line('exception_info.object_pointer = IntPtr.Zero;')
                out.put_line('Type impl_type = typeof({});'.format(impl_class))
                out.put_line('GCHandle handle = (GCHandle)(IntPtr) object_pointer;')
                out.put_line('{0} self = ({0})handle.Target;'.format(impl_class))

                out.put_line('MethodInfo method = impl_type.GetMethod("{}");'.format(method.wrap_name))
                out.put_line('try')
                with IndentScope(out):
                    out.put_line('{}method.Invoke(self, new object[] {{ {} }});'.format(
                        'return ({})'.format(return_type) if return_type != 'void' else '',
                        ', '.join(arg.c_2_wrap_var('', arg.argument_generator.name)[1] for arg in method.arguments)))
                out.put_line('catch(TargetInvocationException tiex) ')
                with IndentScope(out):
                    out.put_line('throw tiex.InnerException;')
            exception_classes = self.__sort_exceptions(method.exception_traits.classes)
            for exception in exception_classes:
                out.put_line('catch ({} exception_object)'.format(exception.full_wrap_name))
                with IndentScope(out):
                    out.put_line('exception_info.code = {};'.format(exception.class_generator.exception_code))
                    out.put_line('exception_info.object_pointer = exception_object.{detach}();'.format(
                        detach=exception.capi_generator.params.detach_method_name))
            out.put_line('catch')
            with IndentScope(out):
                out.put_line('exception_info.code = 1;')
                out.put_line('exception_info.object_pointer = IntPtr.Zero;')
            if return_type != 'void':
                out.put_line('return ({})new object();'.format(return_type))
        out.put_line('')

    def generate__create_callback__method(self, out: FileGenerator):
        return_type = self.full_wrap_name
        class_name = self.base.class_generator.c_name
        impl_class = 'ImplementationClass'
        out.put_line('unsafe public static {0} {1}<{2}>({2} implementation_class)'.format(
            return_type, 'create_callback_for_' + class_name, impl_class))
        with IndentScope(out):
            out.put_line('var result = new {0}();'.format(return_type))
            for method in self.base.methods:
                out.put_line('result.{0}_callback = {1}_callback<{2}>;'.format(
                    method.generator.c_name,
                    class_name + '_' + method.generator.c_name,
                    impl_class
                ))
                out.put_line('result.SetCFunctionFor{0}(result.{1}_callback);'.format(
                    method.wrap_name,
                    method.generator.c_name))
            out.put_line('GCHandle handle = GCHandle.Alloc(implementation_class);')
            out.put_line('IntPtr ptr = (IntPtr)handle;')
            out.put_line('result.SetObjectPointer(ptr);')
            # out.put_line('result.SetObjectPointer(Pointer.Unbox(implementation_class));')
            out.put_line('return result;')
        for method in self.base.methods:
            self.__generate_method_callback(method, out)

    def generate(self):
        self.gen_base_class()
        self.enums = [SharpEnum(enum, self) for enum in self.class_generator.enum_generators]
        if self.class_generator.class_object.exception:
            exception_traits = self.namespace.capi_generator.main_exception_traits
            if self not in exception_traits.classes:
                exception_traits.classes.append(self)
        self.constructors = [SharpConstructor(ctor, self) for ctor in self.class_generator.constructor_generators]
        self.methods = [SharpMethod(method, self) for method in self.class_generator.method_generators]
        self.indexers = [SharpIndexer(indexer, self) for indexer in self.class_generator.indexer_generators]
        self.lifecycle_traits.lifecycle_traits.create_exception_traits(self.class_generator.class_object,
                                                                       self.capi_generator.capi_generator)

    def copy_or_add_ref_noexcept(self):
        if self.class_generator.class_object.copy_or_add_ref_noexcept_filled:
            return self.class_generator.class_object.copy_or_add_ref_noexcept
        else:
            return self.lifecycle_traits.lifecycle_traits.default_value_for_init_noexcept

    def delete_or_release_noexcept(self):
        if self.class_generator.class_object.delete_or_release_noexcept_filled:
            return self.class_generator.class_object.delete_or_release_noexcept
        else:
            return self.lifecycle_traits.lifecycle_traits.default_value_for_finish_noexcept

    @property
    def template_arguments(self):
        if not self.__template_arguments:
            if self.is_template:
                self.__template_arguments = []
                for arg in self.class_generator.template_argument_generators:
                    sharp_argument = SharpArgument(ArgumentGenerator(arg, ""), self.namespace.capi_generator)
                    sharp_argument.generate()
                    self.__template_arguments.append(sharp_argument)
        return self.__template_arguments

    def generate_definition(self):
        for ctor in self.constructors:
            ctor.generate()
        for method in self.methods:
            method.generate()
        for indexer in self.indexers:
            indexer.generate()
        name_array = self.namespace.full_name_array + [self.wrap_short_name, self.wrap_name]
        file_cache = self.capi_generator.file_cache
        definition_header = file_cache.get_file_for_class(name_array if self.is_template else self.full_name_array)
        self.__generate_definition(definition_header)


class SharpTemplate(object):
    def __init__(self,
                 template_generator: TemplateGenerator,
                 namespace: SharpNamespace,
                 capi_generator: SharpCapiGenerator):
        self.template_generator = template_generator
        self.namespace = namespace
        self.constructors = []
        self.methods = []
        self.indexers = []
        self.classes = []
        self.explicit_arguments = []
        self.arguments = []
        self.copy_or_add_ref_when_c_2_wrap = False
        self.non_types = ('template', 'typename', 'class')
        self.base = None
        self.capi_generator = capi_generator

    @property
    def wrap_short_name(self):
        return self.template_generator.template_class_generator.wrap_short_name

    @property
    def get_arguments(self):
        return [arg[1] if arg[0] in self.non_types else arg[0] for arg in self.arguments]

    @property
    def wrap_name(self):
        return self.wrap_short_name + '<' + ', '.join(self.get_arguments) + '>'

    def __generate_constructor_definitions(self, out: FileGenerator):
        self.__generate__ctor_from_object(out)
        out.put_line('')
        for ctor in self.constructors:
            arguments_names = ', '.join([arg[1] for arg in self.explicit_arguments])
            certain = 'Activator.CreateInstance(GetCertainType({0}), new object[] {{{0}}})'.format(arguments_names)
            arguments = [argument.wrap_argument_declaration() for argument in ctor.arguments]
            out.put_line('public {class_name}({arguments}){base_init}'.format(
                class_name=self.wrap_short_name,
                arguments=', '.join([arg[0] + ' ' + arg[1] for arg in self.explicit_arguments] + arguments),
                base_init=' :this(ECreateFromObject.create_from_object, {obj})'.format(obj=certain)))
            out.put_line('{}')
            out.put_line('')

    def __generate_methods_definitions(self, out: FileGenerator):
        for method in self.methods:
            new = 'new ' if method.is_overload() else ''
            return_type = method.return_type.wrap_argument_declaration(self.namespace.full_name_array)
            arguments = [arg.wrap_argument_declaration(self.namespace.full_name_array) for arg in method.arguments]
            out.put_line('{new}public unsafe {return_type} {method_name}({arguments})'.format(
                method_name=method.wrap_name, new=new,
                arguments=', '.join(arguments), return_type=return_type))
            if return_type == 'void':
                return_expression = ''
            else:
                if return_type in [arg.name for arg in self.template_generator.template_object.arguments]:
                    return_expression = 'return Certain2Template<{return_type}>('
                else:
                    return_expression = 'return ({return_type})('

            with IndentScope(out):
                out.put_line('{return_expr}ExecuteMethod("{name}", new object[] {{{arguments}}}){bracket};'.format(
                    return_expr=return_expression.format(return_type=return_type),
                    name=method.wrap_name,
                    bracket=')' if return_expression else '',
                    arguments=', '.join(argument.argument_generator.name for argument in method.arguments)
                ))
            out.put_line('')

    def __generate_indexers_definitions(self, out: FileGenerator):
        for indexer in self.indexers:
            new = 'new ' if indexer.is_overload() else ''
            get_type = indexer.get_type.wrap_argument_declaration(self.namespace.full_name_array)
            set_type = indexer.set_type.wrap_argument_declaration(self.namespace.full_name_array)
            arguments = [arg.wrap_argument_declaration(self.namespace.full_name_array) for arg in indexer.arguments]
            out.put_line('{new}public unsafe {get_type} this[{arguments}]'.format(
                new=new, arguments=', '.join(arguments), get_type=get_type))
            if get_type == 'void':
                get_expression = ''
            else:
                if get_type in [arg.name for arg in self.template_generator.template_object.arguments]:
                    get_expression = 'return Certain2Template<{get_type}>('
                else:
                    get_expression = 'return ({get_type})('
            if set_type == 'void':
                set_expression = ''
            else:
                if set_type in [arg.name for arg in self.template_generator.template_object.arguments]:
                    set_expression = 'Certain2Template<{set_type}>('
                else:
                    set_expression = '({set_type})('

            with IndentScope(out):
                out.put_line('get')
                with IndentScope(out):
                    out.put_line('{get_expr}ExecuteMethod("{name}", new object[] {{{arguments}}}){bracket};'.format(
                        get_expr=get_expression.format(get_type=get_type),
                        name='get_Item',
                        bracket=')' if get_expression else '',
                        arguments=', '.join(argument.argument_generator.name for argument in indexer.arguments)
                    ))
                out.put_line('set')
                with IndentScope(out):
                    out.put_line(indexer.indexer_object.set_impl.format(
                        expression='{set_expr}ExecuteMethod("{name}", new object[] {{{arguments}}}){bracket}'.format(
                            set_expr=set_expression.format(set_type=set_type),
                            name='set_Item',
                            bracket=')' if set_expression else '',
                            arguments=', '.join(argument.argument_generator.name for argument in indexer.arguments)
                        )
                    ))
                out.put_line('')

    def __generate_type_map(self, out: FileGenerator):
        new = 'new ' if self.base else ''
        out.put_line('{0}static protected Dictionary{1} TypeMap = new Dictionary{1}()'.format(new, '< string, Type >'))
        with IndentScope(out, '};'):
            template_arguments = {arg.name: arg.type_name for arg in self.template_generator.template_object.arguments}
            type_map = []
            for instantiation in self.template_generator.template_object.instantiations:
                class_name_array = [self.wrap_short_name]
                inst_arguments = []
                for arg in instantiation.arguments:
                    argument = arg.value
                    if '::' in arg.value:
                        argument = argument.replace('::', '.')
                    argument_generator = self.capi_generator.full_name_2_sharp_object.get(argument, None)
                    if not argument_generator:
                        argument_generator = SharpBuiltinType(BuiltinTypeGenerator(argument))
                    argument = argument_generator.full_wrap_name
                    class_name_array.append(argument_generator.wrap_name)
                    if template_arguments[arg.name] not in self.non_types:
                        inst_arguments.append(argument)
                    else:
                        inst_arguments.append('typeof({0}).FullName'.format(argument))
                if instantiation.typedef_name:
                    suffix = self.template_generator.template_class_generator.lifecycle_traits.suffix
                    certain_class = self.namespace.full_wrap_name + '.' + instantiation.typedef_name + suffix
                else:
                    certain_class = '_'.join(class_name_array)
                type_map.append((' + "_" + '.join(inst_arguments), certain_class))

            out.put_lines(['{{ {0}, typeof({1}) }}'.format(value[0], value[1]) for value in type_map[:-1]], ',\n')
            out.put_line('{{ {0}, typeof({1}) }}'.format(type_map[-1][0], type_map[-1][1]))
        out.put_line('')

    def __generate__type_2_name(self, out: FileGenerator):
        new = 'new ' if self.base else ''
        out.put_line('{0}private static string Type2Name(Type type)'.format(new))
        with IndentScope(out):
            out.put_line('string name = "";')
            out.put_line('MethodInfo method = type.GetMethod("GetCertainType", new Type[] { });')
            out.put_line('if (method != null)')
            with Indent(out):
                out.put_line('name = ((Type)method.Invoke(null, null)).Name;')
            out.put_line('else')
            with Indent(out):
                out.put_line('name = type.Name;')
            out.put_line('int index = name.IndexOf("`");')
            out.put_line('if (index != -1)')
            with Indent(out):
                out.put_line('return name.Substring(0, index);')
            out.put_line('return name;')
        out.put_line('')

    def __generate__get_certain_type_(self, out: FileGenerator):
        def is_type(argument: str) -> bool:
            return argument in ['class', 'template', 'typename']

        new = 'new ' if self.base else ''
        arguments_str = ', '.join(arg[0] + ' ' + arg[1] for arg in self.explicit_arguments)
        out.put_line('{0}public static Type GetCertainType({1})'.format(new, arguments_str))
        with IndentScope(out):
            out.put_line('try')
            with IndentScope(out):
                arguments = []
                for arg in self.arguments:
                    arguments.append('Type2Name(typeof(' + arg[0] + '))' if is_type(arg[1]) else arg[0])
                out.put_line('return TypeMap["" + {arguments}];'.format(arguments=' + "_" + '.join(arguments)))
            out.put_line('catch(KeyNotFoundException)')
            with IndentScope(out):
                out.put_line('throw new ArgumentException("Incorrect generic argument. '
                             'Instantiation with these parameters was not found.");')
        out.put_line('')

    def __generate__execute_method_(self, out: FileGenerator):
        new = 'new ' if self.base else ''
        out.put_line('{0}private object ExecuteMethod(string name, object[] method_args)'.format(new))
        with IndentScope(out):
            out.put_line('int args_count = method_args.Length;')
            out.put_line('var args_types = new Type[args_count];')
            out.put_line('var calling_args = new object[args_count];')
            out.put_line('for (int i = 0; i < args_count; ++i)')
            with IndentScope(out):
                out.put_line('Type type = method_args[i].GetType();')
                out.put_line('MethodInfo get_type_method = type.GetMethod("GetCertainType");')
                out.put_line('if (get_type_method != null)')
                with IndentScope(out):
                    out.put_line('calling_args[i] = type.GetMethod("GetCertainClass").Invoke(method_args[i], null);')
                    out.put_line('type = (Type)get_type_method.Invoke(null, null);')
                out.put_line('else')
                with IndentScope(out):
                    out.put_line('calling_args[i] = method_args[i];')
                out.put_line('args_types[i] = type;')
            out.put_line('MethodInfo method = mObject.GetType().GetMethod(name, args_types);')
            out.put_line('return method.Invoke(mObject, calling_args);')
        out.put_line('')

    def __generate__get_certain_class(self, out: FileGenerator):
        out.put_line('{new}public object GetCertainClass()'.format(new='new ' if self.base else ''))
        with IndentScope(out):
            out.put_line('return mObject;')
        out.put_line('')

    def __generate__certain_2_template(self, out: FileGenerator):
        new = 'new ' if self.base else ''
        out.put_line('private static TemplateArgument Certain2Template<TemplateArgument>(object obj)'.format(new))
        with IndentScope(out):
            out.put_line('Type type = typeof(TemplateArgument);')
            out.put_line('if (type.GetMethod("GetCertainType") != null)')
            with IndentScope(out):
                out.put_line('var enumeration = System.Enum.Parse(type.GetNestedType("ECreateFromObject"), '
                             '"create_from_object");')
                out.put_line('return (TemplateArgument)type.GetConstructors()[0].Invoke(new object[] '
                             '{ enumeration, obj });')
            out.put_line('return (TemplateArgument)obj;')
        out.put_line('')

    def __generate__ctor_from_object(self, out: FileGenerator):
        out.put_line('public {name}(ECreateFromObject e, object obj){base}'.format(
            base=get_template_base_init(self), name=self.wrap_short_name))
        with IndentScope(out):
            out.put_line('if (TypeMap.Values.Any(value => value.IsAssignableFrom(obj.GetType())))')
            with IndentScope(out):
                out.put_line('mObject = obj;')
            out.put_line('else')
            with IndentScope(out):
                out.put_line('throw new ArgumentException("Incorrect generic argument. '
                             'Instantiation with these parameters was not found.");')

    def __generate_std_method_definition(self, out: FileGenerator, name: str, return_type: str = 'void',
                                         arguments=(), keywords=('unsafe', 'public',)):
        if self.base:
            keywords = (('new',) + keywords)
        out.put_line('{keywords} {return_type} {name}({arguments})'.format(
            keywords=' '.join(keywords),
            return_type=return_type,
            name=name,
            arguments=', '.join([arg[0] + ' ' + arg[1] for arg in arguments])
        ))
        with IndentScope(out):
            out.put_line('{return_expr}(ExecuteMethod("{name}", new object[] {{{arguments}}}));'.format(
                return_expr='return ({0})'.format(return_type) if return_type != 'void' else '',
                name=name,
                arguments=', '.join(arg[1] for arg in arguments)
            ))
            out.put_line('')

    def __generate_std_methods_definitions(self, out: FileGenerator):
        self.__generate_std_method_definition(out, 'IsNull', return_type='bool')
        self.__generate_std_method_definition(out, 'IsNotNull', return_type='bool')

    def __generate_definition(self, out: FileGenerator):
        base_class = ''
        if self.base:
            if isinstance(self.base, SharpTemplate):
                base_class = ': {0}<{1}>'.format(self.base.wrap_short_name, ', '.join(self.get_arguments))
            else:
                base_class = ': ' + self.base.wrap_short_name
        out.put_begin_cpp_comments(self.namespace.namespace_generator.params)
        out.put_line('using System;')
        out.put_line('using System.Reflection;')
        out.put_line('using System.Collections.Generic;')
        out.put_line('using System.Runtime.InteropServices;')
        out.put_line('using System.Linq;')
        out.put_line('')
        self.namespace.increase_indent_recursively(out)
        out.put_line('public class {class_name}{base}'.format(class_name=self.wrap_name, base=base_class))
        with IndentScope(out):
            new = 'new ' if self.base else ''
            self.__generate_type_map(out)
            out.put_line('{new}public enum ECreateFromObject {{create_from_object}};'.format(new=new))
            out.put_line('')
            self.__generate_constructor_definitions(out)
            self.__generate_std_methods_definitions(out)
            self.__generate_methods_definitions(out)
            self.__generate_indexers_definitions(out)
            self.__generate__type_2_name(out)
            self.__generate__get_certain_type_(out)
            self.__generate__execute_method_(out)
            self.__generate__get_certain_class(out)
            self.__generate__certain_2_template(out)
            out.put_line('{new}private object mObject;'.format(new=new))
        self.namespace.decrease_indent_recursively(out)

    def generate(self):
        base_name = self.template_generator.template_class.base
        if base_name:
            base_name = get_template_name(base_name)
            base_name_array = SharpClass.get_relative_name_array(self.namespace.full_name_array, base_name.split('::'))
            self.base = self.namespace.find_object(base_name_array)
        for argument in self.template_generator.template_object.arguments:
            if argument.type_name not in ['template', 'class', 'typename']:
                self.explicit_arguments.append((argument.type_name, argument.name))
            type_name = self.capi_generator.full_name_2_sharp_object.get(argument.type_name.replace('::', '.'), None)
            self.arguments.append((argument.name, type_name if type_name else argument.type_name,))
        for constructor in self.template_generator.template_class_generator.constructor_generators:
            self.constructors.append(SharpConstructor(constructor, self))
        for method in self.template_generator.template_class_generator.method_generators:
            self.methods.append(SharpMethod(method, self))
        for indexer in self.template_generator.template_class_generator.indexer_generators:
            self.indexers.append(SharpIndexer(indexer, self))
        for class_ in self.classes:
            class_.generate()
        if not self.classes:
            raise BeautifulCapiException('Template {name} has no classes'.format(name=self.wrap_short_name))

    def generate_definition(self):
        for constructor in self.constructors:
            constructor.generate()
        for method in self.methods:
            method.generate()
        for indexer in self.indexers:
            indexer.generate()
        file_cache = self.capi_generator.file_cache
        header = file_cache.get_file_for_class(self.namespace.full_name_array + [self.wrap_short_name])
        self.__generate_definition(header)
        for class_ in self.classes:
            class_.generate_definition()


class SharpEnum(object):
    def __init__(self, enum_generator, parent: SharpNamespace or SharpClass):
        self.parent = parent
        self.enum_generator = enum_generator
        full_name = enum_generator.full_name.replace('::', '.')
        parent.capi_generator.full_name_2_sharp_object[full_name] = self

    def wrap_argument_declaration(self) -> str:
        return self.enum_generator.full_wrap_name.replace('::', '.')

    @property
    def wrap_name(self):
        return self.enum_generator.wrap_name

    @property
    def full_wrap_name(self):
        return self.parent.full_wrap_name + '.' + self.wrap_name

    @staticmethod
    def get_enum_definition(enum_object) -> [str]:
        return [item.name + (' = {},'.format(item.value) if item.value_filled else ',') for item in enum_object.items]

    def generate_enum_definition(self, out: FileGenerator):
        out.put_line('public enum {name}'.format(name=self.enum_generator.name))
        with IndentScope(out, '};'):
            items_definitions = SharpEnum.get_enum_definition(self.enum_generator.enum_object)
            if items_definitions:
                for item_definition in items_definitions:
                    out.put_line(item_definition)
        out.put_line('')

    @staticmethod
    def c_argument_declaration() -> str:
        return 'int'

    def implementation_2_c_var(self, result_var: str, expression: str) -> ([str], str):
        casting_expression = '({c_type}){expression}'.format(
            c_type=self.c_argument_declaration(), expression=expression
        )
        if result_var:
            return ['{type_name} {result_var} = {expression};'.format(
                type_name=self.c_argument_declaration(),
                result_var=result_var,
                expression=casting_expression)], result_var
        else:
            return [], casting_expression

    def wrap_return_type(self) -> str:
        return self.parent.full_wrap_name + '.' + self.enum_generator.wrap_name

    def wrap_2_c_var(self, result_var: str, expression: str) -> ([str], str):
        return self.implementation_2_c_var(result_var, expression)

    def c_2_wrap_var(self, result_var: str, expression: str) -> ([str], str):
        if result_var:
            return ['{type_name} {result_var} = ({type_name}){expression};'.format(
                type_name=self.wrap_return_type(),
                result_var=result_var,
                expression=expression
            )], result_var
        else:
            return [], '({type_name}){expression}'.format(
                type_name=self.wrap_return_type(), expression=expression)


class SharpMappedType(object):
    def __init__(self, mapped_type_object):
        self.mapped_type_object = mapped_type_object
        self.name = self.mapped_type_object.name
        self.wrap_type = mapped_type_object.wrap_type
        self.argument_wrap_type = mapped_type_object.argument_wrap_type
        self.argument_wrap_type_filled = mapped_type_object.argument_wrap_type_filled
        self.wrap_2_c = mapped_type_object.wrap_2_c
        self.c_2_wrap = mapped_type_object.c_2_wrap
        self.include_headers = mapped_type_object.include_headers
        if mapped_type_object.sharps:
            sharp_type = mapped_type_object.sharps[0]
            self.wrap_type = sharp_type.wrap_type
            self.argument_wrap_type = sharp_type.argument_wrap_type
            self.argument_wrap_type_filled = sharp_type.argument_wrap_type_filled
            self.wrap_2_c = sharp_type.wrap_2_c
            self.c_2_wrap = sharp_type.c_2_wrap
            self.include_headers = sharp_type.include_headers
            self.marshal_as = sharp_type.marshal_as

    def marshal_type(self) -> str:
        return self.marshal_as if self.marshal_as else ''

    def format(self, casting_expression: str, expression_to_cast: str, result_var: str, type_name: str) -> ([str], str):
        result_expression = casting_expression.format(
            expression=expression_to_cast,
            c_type=self.mapped_type_object.c_type,
            implementation_type=self.mapped_type_object.implementation_type,
            wrap_type=self.wrap_type,
            argument_wrap_type=self.argument_wrap_type
        )
        if result_var:
            return ['{type_name} {result_var} = {expression};'.format(
                type_name=type_name,
                expression=result_expression,
                result_var=result_var
            )], result_var
        else:
            return [], result_expression

    def wrap_argument_declaration(self):
        return self.argument_wrap_type if self.argument_wrap_type_filled else self.wrap_type

    def c_argument_declaration(self) -> str:
        return self.wrap_argument_declaration()

    def wrap_2_c_var(self, result_var: str, expression: str):
        return self.format(self.wrap_2_c, expression, result_var, self.mapped_type_object.c_type)

    def c_2_wrap_var(self, result_var: str, expression: str):
        return self.format(self.c_2_wrap, expression, result_var, self.wrap_type)

    @property
    def wrap_name(self):
        return self.wrap_type

    @property
    def full_wrap_name(self):
        return self.wrap_type


class SharpBuiltinType(object):
    def __init__(self, builtin_generator: BuiltinTypeGenerator):
        self.builtin_generator = builtin_generator

    @property
    def is_void(self):
        return True if self.builtin_generator.type_name == 'void' or not self.builtin_generator.type_name else False

    @property
    def wrap_name(self):
        return self.builtin_generator.type_name

    @property
    def full_wrap_name(self):
        return self.wrap_name

    def wrap_argument_declaration(self) -> str:
        return '{type_name}'.format(type_name='void' if self.is_void else self.builtin_generator.type_name)

    def c_argument_declaration(self) -> str:
        return self.builtin_generator.type_name if not self.is_void else 'void'

    def wrap_return_type(self) -> str:
        return self.wrap_argument_declaration()

    def c_2_wrap_var(self, result_var: str, expression: str) -> ([str], str):
        if not self.is_void:
            if result_var:
                return ['{type_name} {result_var} = {expression};'.format(
                    type_name=self.wrap_return_type(),
                    result_var=result_var,
                    expression=expression)], result_var
            else:
                return [], expression
        else:
            return [expression + ';'], ''

    def implementation_2_c_var(self, result_var: str, expression: str) -> ([str], str):
        if not self.is_void:
            if result_var:
                return ['{type_name} {result_var} = {expression};'.format(
                    type_name=self.builtin_generator.type_name,
                    result_var=result_var,
                    expression=expression)], result_var
            else:
                return [], expression
        else:
            return [expression + ';'], ''

    def wrap_2_c_var(self, result_var: str, expression: str) -> ([str], str):
        return self.implementation_2_c_var(result_var, expression)


class SharpArgument(object):
    def __init__(self, argument_generator: ArgumentGenerator, capi_generator: SharpCapiGenerator):
        self.argument_generator = argument_generator
        self.capi_generator = capi_generator
        self.type_generator = None

    def marshal_type(self) -> str:
        if self.argument_generator.argument_object and self.argument_generator.argument_object.sharp_marshal_as_filled:
            return self.argument_generator.argument_object.sharp_marshal_as
        elif self.type_generator and isinstance(self.type_generator, SharpMappedType):
            return self.type_generator.marshal_type()
        return ''

    def get_marshaling(self) -> str:
        marshal_type = self.marshal_type()
        return '[MarshalAs({})]'.format(marshal_type) if marshal_type else ''

    def wrap_argument_declaration(self, base=()) -> str:
        declaration = self.type_generator.wrap_argument_declaration().replace('::', '.').split('.')
        type_name = SharpClass.get_relative_name(base, declaration)
        argument = ' ' + self.argument_generator.name if self.argument_generator.name else ''
        return '{0}{1}'.format(type_name, argument)

    def c_argument_declaration(self) -> str:
        return '{0}{1}'.format(self.type_generator.c_argument_declaration(),
                               ' ' + self.argument_generator.name if self.argument_generator.name else '')

    def c_2_wrap_var(self, result_var: str, expression: str) -> ([str], str):
        return self.type_generator.c_2_wrap_var(result_var, expression)

    def wrap_2_c(self) -> str:
        return self.type_generator.wrap_2_c_var('', self.argument_generator.name)[1]

    def generate(self):
        generator = self.argument_generator.type_generator
        if isinstance(generator, BuiltinTypeGenerator):
            self.type_generator = SharpBuiltinType(generator)
        elif isinstance(generator, MappedTypeGenerator):
            self.type_generator = SharpMappedType(generator.mapped_type_object)
        elif isinstance(generator, ExternalClassTypeGenerator):
            sharp_external_class = self.capi_generator.get_or_gen_external_class(
                '.'.join(generator.class_argument_generator.full_name_array).replace('::', '.'),
                generator.class_argument_generator)
            self.type_generator = sharp_external_class
        elif isinstance(generator, ClassTypeGenerator):
            class_name = '.'.join(generator.class_argument_generator.full_template_name_array).replace('::', '.')
            self.type_generator = self.capi_generator.full_name_2_sharp_object[class_name]
        elif isinstance(generator, EnumTypeGenerator):
            self.type_generator = self.capi_generator.full_name_2_sharp_object[
                generator.enum_argument_generator.full_name.replace('::', '.')]
        else:
            self.type_generator = generator


class SharpRoutine(object):
    def __init__(self, generator, parent: SharpClass or SharpTemplate or SharpNamespace):
        self.generator = generator
        self.parent = parent
        self.arguments = []

    def generate(self):
        arguments = []
        for arg in self.generator.argument_generators:
            sharp_argument = SharpArgument(arg, self.parent.capi_generator)
            sharp_argument.generate()
            arguments.append(sharp_argument)
        self.arguments = arguments


class SharpMethod(SharpRoutine):
    def __init__(self, method_generator: MethodGenerator, generator: SharpClass or SharpTemplate):
        super().__init__(method_generator, generator)
        self.return_type = None
        self.wrap_name = method_generator.wrap_name
        self.exception_traits = generator.namespace.capi_generator.get_exception_traits(
            method_generator.method_object.noexcept)

    def get_return_marshaling(self) -> str:
        if self.generator.method_object.sharp_marshal_return_as_filled:
            return '[return:MarshalAs({})]'.format(self.generator.method_object.sharp_marshal_return_as)
        marshal_type = self.return_type.marshal_type()
        return '[return:MarshalAs({})]'.format(marshal_type) if marshal_type else ''

    def is_overload(self):
        if self.parent.base:
            for method in self.parent.base.methods:
                if self.generator.name != method.generator.name:
                    continue
                return_type = self.generator.return_type_generator.type_name
                if return_type != method.generator.return_type_generator.type_name:
                    continue
                result = True
                for arg in self.generator.argument_generators:
                    if arg.type_generator != method.generator.argument_generators.type_generator:
                        result = False
                        break
                if result:
                    return True
        return False

    def c_arguments_list(self):
        result = [ThisArgumentGenerator(self.generator)]
        for argument in self.arguments:
                result.append(argument)
        return result

    def generate_wrap_definition(self, out: FileGenerator):
        new = ''
        if self.is_overload:
            new = 'new '
        arguments = ', '.join(argument.wrap_argument_declaration() for argument in self.arguments)
        arguments_call = [argument.wrap_2_c() for argument in self.c_arguments_list()]
        out.put_line('{new}unsafe public {return_type} {name}({arguments})'.format(
            return_type=self.return_type.wrap_argument_declaration(), new=new,
            name=self.wrap_name, arguments=arguments))

        saved_copy_or_add_ref = False
        return_type_generator = self.return_type.type_generator
        if isinstance(return_type_generator, SharpClass) or isinstance(return_type_generator, SharpTemplate):
            saved_copy_or_add_ref = return_type_generator.copy_or_add_ref_when_c_2_wrap
            return_type_generator.copy_or_add_ref_when_c_2_wrap = self.generator.method_object.return_copy_or_add_ref
        with IndentScope(out):
            return_expression = self.exception_traits.generate_c_call(out, self.return_type,
                                                                      self.generator.full_c_name, arguments_call)
            out.put_return_cpp_statement(return_expression)

        if isinstance(return_type_generator, SharpClass) or isinstance(return_type_generator, SharpTemplate):
            return_type_generator.copy_or_add_ref_when_c_2_wrap = saved_copy_or_add_ref

    def generate(self):
        super().generate()
        argument_generator = ArgumentGenerator(self.generator.return_type_generator, '')
        self.return_type = SharpArgument(argument_generator, self.parent.capi_generator)
        self.return_type.generate()
        if self.generator.method_object.const:
            for method in self.parent.methods:
                if method.generator.name == self.generator.name and not method.generator.method_object.const:
                    self.wrap_name += 'Const'
                    break


class SharpIndexer(object):
    def __init__(self, generator: IndexerGenerator, parent: SharpClass or SharpTemplate):
        self.generator = generator
        self.parent = parent
        self.arguments = []
        self.set_type = None
        self.get_type = None
        self.wrap_name = self.generator.wrap_name
        self.exception_traits = self.parent.namespace.capi_generator.get_exception_traits(
            self.generator.indexer_object.noexcept)

    def get_return_marshaling(self) -> str:
        if self.generator.indexer_object.sharp_marshal_return_as_filled:
            return '[return:MarshalAs({})]'.format(self.generator.indexer_object.sharp_marshal_return_as)
        marshal_type = self.get_type.marshal_type()
        return '[return:MarshalAs({})]'.format(marshal_type) if marshal_type else ''

    def is_overload(self):
        if self.parent.base:
            for indexer in self.parent.base.indexers:
                if self.generator.name != indexer.generator.name:
                    continue
                set_type = self.generator.set_type_generator.type_name
                if set_type != indexer.generator.set_type_generator.type_name:
                    continue
                get_type = self.generator.get_type_generator.type_name
                if get_type != indexer.generator.get_type_generator.type_name:
                    continue
                result = True
                for arg in self.generator.argument_generators:
                    if arg.type_generator != indexer.generator.argument_generators.type_generator:
                        result = False
                        break
                if result:
                    return True
        return False

    def c_arguments_list(self):
        result = [ThisArgumentGenerator(self.generator)]
        for argument in self.arguments:
                result.append(argument)
        return result

    def generate_wrap_definition(self, out: FileGenerator):
        new = ''
        if self.is_overload:
            new = 'new '
        arguments = ', '.join(argument.wrap_argument_declaration() for argument in self.arguments)
        out.put_line('{new}unsafe public {return_type} this[{arguments}]'.format(
            return_type=self.get_type.wrap_argument_declaration(), new=new, arguments=arguments))

        saved_copy_or_add_ref = False
        return_type_generator = self.get_type.type_generator
        if isinstance(return_type_generator, SharpClass) or isinstance(return_type_generator, SharpTemplate):
            saved_copy_or_add_ref = return_type_generator.copy_or_add_ref_when_c_2_wrap
            return_type_generator.copy_or_add_ref_when_c_2_wrap = self.generator.indexer_object.return_copy_or_add_ref
        with IndentScope(out):
            out.put_line('get')
            with IndentScope(out):
                arguments_call = [argument.wrap_2_c() for argument in self.c_arguments_list()]
                return_expression = self.exception_traits.generate_c_call(out, self.get_type,
                                                                          self.generator.full_c_name(False),
                                                                          arguments_call)
                out.put_return_cpp_statement(return_expression)
            out.put_line('set')
            with IndentScope(out):
                arguments_call = [argument.wrap_2_c() for argument in self.c_arguments_list()]
                return_expression = self.exception_traits.generate_c_call(out, self.set_type,
                                                                          self.generator.full_c_name(True),
                                                                          arguments_call)
                out.put_line(self.generator.indexer_object.set_impl.format(expression=return_expression))

        if isinstance(return_type_generator, SharpClass) or isinstance(return_type_generator, SharpTemplate):
            return_type_generator.copy_or_add_ref_when_c_2_wrap = saved_copy_or_add_ref

    def generate(self):
        self.arguments = []
        for arg in self.generator.argument_generators:
            sharp_argument = SharpArgument(arg, self.parent.capi_generator)
            sharp_argument.generate()
            self.arguments.append(sharp_argument)
        set_argument_generator = ArgumentGenerator(self.generator.set_type_generator, '')
        get_argument_generator = ArgumentGenerator(self.generator.get_type_generator, '')
        self.set_type = SharpArgument(set_argument_generator, self.parent.capi_generator)
        self.get_type = SharpArgument(get_argument_generator, self.parent.capi_generator)
        self.set_type.generate()
        self.get_type.generate()


class SharpConstructor(SharpRoutine):
    def __init__(self, constructor_generator: ConstructorGenerator, generator: SharpClass or SharpTemplate):
        super().__init__(constructor_generator, generator)
        self.exception_traits = generator.namespace.capi_generator.get_exception_traits(
            constructor_generator.constructor_object.noexcept)

    def c_arguments_list(self):
        result = []
        for argument in self.generator.argument_generators:
            generator = argument.type_generator
            if isinstance(generator, MappedTypeGenerator):
                capi_generator = self.parent.capi_generator
                mapped_type = capi_generator.get_or_gen_mapped_type(generator.name, generator.mapped_type_object)
                result.append(ArgumentGenerator(mapped_type, argument.name))
            elif isinstance(generator, EnumTypeGenerator):
                full_name = generator.enum_argument_generator.full_name.replace('::', '.')
                sharp_enum = self.parent.capi_generator.full_name_2_sharp_object[full_name]
                result.append(ArgumentGenerator(sharp_enum, argument.name))
            else:
                result.append(argument)
        return result

    def generate_wrap_definition(self, out: FileGenerator, capi_generator: CapiGenerator):
        if self.generator.constructor_object.noexcept_filled:
            self.parent.exception_traits = capi_generator.get_exception_traits(
                self.generator.constructor_object.noexcept)
        else:
                self.generator.exception_traits = self.parent.copy_or_add_ref_noexcept
        arguments = ', '.join(argument.wrap_argument_declaration() for argument in self.arguments)
        arguments_call = [argument.wrap_2_c() for argument in self.c_arguments_list()]
        out.put_line('unsafe public {class_name}({arguments}){base_init}'.format(
            class_name=self.parent.wrap_name,
            arguments=arguments,
            base_init=get_base_init(self.parent) if self.parent.base else ''))
        result = SharpArgument(ArgumentGenerator(ClassTypeGenerator(
            self.generator.parent_class_generator), ''),
            self.parent.capi_generator)
        result.generate()

        saved_copy_or_add_ref = self.parent.copy_or_add_ref_when_c_2_wrap
        self.parent.copy_or_add_ref_when_c_2_wrap = self.generator.constructor_object.return_copy_or_add_ref
        with IndentScope(out):
            result_expression = self.exception_traits.generate_c_call(
                out,
                result,
                self.generator.full_c_name,
                arguments_call
            )
            out.put_line('SetObject({result_expression}.{detach}());'.format(
                result_expression=result_expression,
                detach=self.generator.params.detach_method_name))
        self.parent.copy_or_add_ref_when_c_2_wrap = saved_copy_or_add_ref


class SharpFunction(SharpRoutine):
    def __init__(self, function_generator: FunctionGenerator, parent: SharpNamespace):
        super().__init__(function_generator, parent)
        self.return_type = None
        self.exception_traits = parent.capi_generator.get_exception_traits(function_generator.function_object.noexcept)

    def get_return_marshaling(self) -> str:
        if self.generator.function_object.sharp_marshal_return_as_filled:
            return '[return:MarshalAs({})]'.format(self.generator.function_object.sharp_marshal_return_as)
        marshal_type = self.return_type.marshal_type()
        return '[return:MarshalAs({})]'.format(marshal_type) if marshal_type else ''

    @property
    def get_namespace(self):
        if isinstance(self.parent, SharpNamespace):
            return self.parent
        return self.parent.parent_namespace

    def generate_wrap_definition(self, out: FileGenerator):
        arguments = ', '.join(argument.wrap_argument_declaration() for argument in self.arguments)
        arguments_call = [argument.wrap_2_c() for argument in self.arguments]
        out.put_line('public unsafe static {return_type} {name}({arguments})'.format(
            return_type=self.return_type.wrap_argument_declaration(),
            name=self.generator.wrap_name,
            arguments=arguments))
        saved_copy_or_add_ref = False
        return_type_generator = self.return_type.type_generator
        if isinstance(return_type_generator, SharpClass) or isinstance(return_type_generator, SharpTemplate):
            saved_copy_or_add_ref = return_type_generator.copy_or_add_ref_when_c_2_wrap
            return_type_generator.copy_or_add_ref_when_c_2_wrap = self.generator.function_object.return_copy_or_add_ref
        with IndentScope(out):
            return_expression = self.exception_traits.generate_c_call(
                out, self.return_type, self.generator.full_c_name, arguments_call)
            out.put_return_cpp_statement(return_expression)
        if isinstance(return_type_generator, SharpClass) or isinstance(return_type_generator, SharpTemplate):
            return_type_generator.copy_or_add_ref_when_c_2_wrap = saved_copy_or_add_ref

    def generate(self):
        super().generate()
        argument_generator = ArgumentGenerator(self.generator.return_type_generator, '')
        self.return_type = SharpArgument(argument_generator, self.parent.capi_generator)
        self.return_type.generate()


class SharpLifecycleTraits(object):
    def __init__(self, lifecycle_traits: LifecycleTraits, capi_generator: SharpCapiGenerator):
        self.lifecycle_traits = lifecycle_traits
        self.params = lifecycle_traits.params
        self.capi_generator = capi_generator

    def generate_std_methods_definitions(self, out: FileGenerator, sharp_class: SharpClass):
        new = 'new ' if sharp_class.base else ''
        out.put_line('{new}unsafe public static {class_name} {null_method}()'.format(
            class_name=sharp_class.wrap_name,
            null_method=self.params.null_method_name,
            new=new))
        with IndentScope(out):
            out.put_line('return new {class_name}({class_name}.{force_create}, IntPtr.Zero, false);'.format(
                force_create='ECreateFromRawPointer.force_creating_from_raw_pointer',
                class_name=sharp_class.wrap_name))
        out.put_line('')
        out.put_line('{new}unsafe public bool {is_null_method}()'.format(
            is_null_method=self.params.is_null_method_name, new=new))
        with IndentScope(out):
            out.put_line('return {get_raw}() == IntPtr.Zero;'.format(get_raw=self.params.get_raw_pointer_method_name))
        out.put_line('')
        out.put_line('{new}unsafe public bool {is_not_null_method}()'.format(
            is_not_null_method=self.params.is_not_null_method_name, new=new))
        with IndentScope(out):
            out.put_line('return {get_raw}() != IntPtr.Zero;'.format(get_raw=self.params.get_raw_pointer_method_name))
        out.put_line('')
        out.put_line('unsafe public static bool operator!({class_name} obj)'.format(
            class_name=sharp_class.wrap_name))
        with IndentScope(out):
            out.put_line('return obj.{get_raw}() != IntPtr.Zero;'.format(
                get_raw=self.params.get_raw_pointer_method_name))
        out.put_line('')
        out.put_line('{new}unsafe public IntPtr {detach_method}()'.format(
            detach_method=self.params.detach_method_name, new=new))
        with IndentScope(out):
            out.put_line('IntPtr result = {get_raw}();'.format(get_raw=self.params.get_raw_pointer_method_name))
            out.put_line('SetObject(IntPtr.Zero);')
            out.put_line('return result;')
        out.put_line('')
        out.put_line('{new}unsafe public IntPtr {get_raw_pointer_method}()'.format(
            get_raw_pointer_method=self.params.get_raw_pointer_method_name, new=new))
        with IndentScope(out):
            out.put_line('return mObject != IntPtr.Zero ? mObject: IntPtr.Zero;')


class SharpCopySemantic(SharpLifecycleTraits):
    def __generate_copy_constructor_definition(self, out: FileGenerator, sharp_class):
        out.put_line('unsafe public {class_name}({class_name} other){base_init}'.format(
            class_name=sharp_class.wrap_name,
            base_init=get_base_init(sharp_class))
        )
        with IndentScope(out):
            expr = 'new {class_name}(ECreateFromRawPointer.force_creating_from_raw_pointer, IntPtr.Zero, false);'
            out.put_line(expr.format(
                class_name=sharp_class.wrap_name, ))
            out.put_line('if (other.{get_raw}() != IntPtr.Zero)'.format(
                get_raw=self.params.get_raw_pointer_method_name))
            with IndentScope(out):
                self.lifecycle_traits.create_exception_traits(sharp_class.class_generator.class_object,
                                                              self.capi_generator.capi_generator)
                exception_traits = SharpExceptionTraits(self.lifecycle_traits.init_method_exception_traits,
                                                        self.capi_generator.params)
                copy_result = exception_traits.generate_c_call(
                    out, SharpBuiltinType(BuiltinTypeGenerator('IntPtr')), sharp_class.class_generator.copy_method,
                    ['other.{get_raw}()'.format(get_raw=self.params.get_raw_pointer_method_name)])
                out.put_line('SetObject({copy_result});'.format(copy_result=copy_result))
            out.put_line('else')
            with IndentScope(out):
                out.put_line('SetObject(IntPtr.Zero);')

    def generate_raw_copy_constructor_body_definition(self, out: FileGenerator, sharp_class, copy_object):
        out.put_line('if (object_pointer != IntPtr.Zero && {copy_object})'.format(copy_object=copy_object))
        with IndentScope(out):
            self.lifecycle_traits.create_exception_traits(sharp_class.class_generator.class_object,
                                                          self.capi_generator.capi_generator)
            exception_traits = SharpExceptionTraits(self.lifecycle_traits.init_method_exception_traits,
                                                    self.capi_generator.params)
            copy_result = exception_traits.generate_c_call(
                out, SharpBuiltinType(BuiltinTypeGenerator('IntPtr')), sharp_class.class_generator.copy_method,
                ['object_pointer'])
            out.put_line('SetObject({copy_result});'.format(copy_result=copy_result))
        out.put_line('else')
        with IndentScope(out):
            out.put_line('SetObject(object_pointer);')

    def __generate_raw_copy_constructor_definition(self, out: FileGenerator, sharp_class):
        constructor_arguments = 'ECreateFromRawPointer e, IntPtr object_pointer, bool copy_object'
        out.put_line('unsafe public {class_name}({arguments}){base_init}'.format(
            class_name=sharp_class.wrap_name,
            arguments=constructor_arguments,
            base_init=get_base_init(sharp_class))
        )
        with IndentScope(out):
            self.generate_raw_copy_constructor_body_definition(out, sharp_class, 'copy_object')

    def __generate_deallocate(self, out: FileGenerator, sharp_class):
        out.put_line('if ({get_raw}() != IntPtr.Zero)'.format(
            get_raw=self.params.get_raw_pointer_method_name))
        with IndentScope(out):
            self.lifecycle_traits.finish_method_exception_traits.generate_c_call(
                out, BuiltinTypeGenerator('void'), sharp_class.class_generator.delete_method,
                ['{get_raw}()'.format(get_raw=self.params.get_raw_pointer_method_name)])
            out.put_line('SetObject(IntPtr.Zero);')

    def __generate_destructor(self, out: FileGenerator, sharp_class):
        out.put_line('unsafe ~{class_name}()'.format(
            class_name=sharp_class.wrap_name)
        )
        with IndentScope(out):
            self.__generate_deallocate(out, sharp_class)

    def generate_std_methods_definitions(self, out: FileGenerator, sharp_class):
        if self.lifecycle_traits.generate_copy_constructor(sharp_class.class_generator):
            self.__generate_copy_constructor_definition(out, sharp_class)
            out.put_line('')
        self.__generate_raw_copy_constructor_definition(out, sharp_class)
        out.put_line('')
        self.__generate_destructor(out, sharp_class)
        out.put_line('')
        super().generate_std_methods_definitions(out, sharp_class)


class SharpRawPointerSemantic(SharpLifecycleTraits):
    def __generate_copy_constructor_definition(self, out: FileGenerator, sharp_class):
        out.put_line('unsafe public {class_name}({class_name} other){base_init}'.format(
            class_name=sharp_class.wrap_name,
            base_init=get_base_init(sharp_class))
        )
        with IndentScope(out):
            out.put_line('SetObject(other.{get_raw}());'.format(get_raw=self.params.get_raw_pointer_method_name))

    @staticmethod
    def generate_raw_copy_constructor_body_definition(out: FileGenerator, sharp_class, copy_object):
        RawPointerSemantic.generate_raw_copy_constructor_body_definition(out, sharp_class, copy_object)

    @staticmethod
    def __generate_raw_copy_constructor_definition(out: FileGenerator, sharp_class):
        out.put_line('unsafe public {class_name}({arguments}){base_init}'.format(
            class_name=sharp_class.wrap_name,
            arguments='ECreateFromRawPointer e, IntPtr object_pointer, bool copy',
            base_init=get_base_init(sharp_class))
        )
        with IndentScope(out):
            RawPointerSemantic.generate_raw_copy_constructor_body_definition(out, sharp_class, '')

    def __generate_delete_method(self, out: FileGenerator, sharp_class):
        out.put_line('{new} unsafe public void {delete_method}()'.format(
            new='new ' if sharp_class.base else '',
            delete_method=self.params.delete_method_name
        ))
        with IndentScope(out):
            out.put_line('if ({get_raw}() != IntPtr.Zero)'.format(
                get_raw=self.params.get_raw_pointer_method_name))
            with IndentScope(out):
                self.lifecycle_traits.finish_method_exception_traits.generate_c_call(
                    out, BuiltinTypeGenerator('void'), sharp_class.class_generator.delete_method,
                    ['{get_raw}()'.format(get_raw=self.params.get_raw_pointer_method_name)])
                out.put_line('SetObject(IntPtr.Zero);')

    def generate_std_methods_definitions(self, out: FileGenerator, sharp_class):
        self.__generate_copy_constructor_definition(out, sharp_class)
        out.put_line('')
        self.__generate_raw_copy_constructor_definition(out, sharp_class)
        out.put_line('')
        self.__generate_delete_method(out, sharp_class)
        out.put_line('')
        super().generate_std_methods_definitions(out, sharp_class)


class SharpRefCountedSemantic(SharpLifecycleTraits):
    def __generate_copy_constructor_definition(self, out: FileGenerator, sharp_class):
        out.put_line('unsafe public {class_short_name}({class_name} other){base_init}'.format(
            class_short_name=sharp_class.wrap_name,
            class_name=sharp_class.wrap_name,
            base_init=get_base_init(sharp_class))
        )
        with IndentScope(out):
            out.put_line('SetObject(other.{get_raw}());'.format(get_raw=self.params.get_raw_pointer_method_name))
            out.put_line('if (other.{get_raw}() != IntPtr.Zero)'.format(
                get_raw=self.params.get_raw_pointer_method_name))
            with IndentScope(out):
                self.lifecycle_traits.create_exception_traits(sharp_class.class_generator.class_object,
                                                              self.capi_generator.capi_generator)
                exception_traits = SharpExceptionTraits(self.lifecycle_traits.init_method_exception_traits,
                                                        self.capi_generator.params)
                exception_traits.generate_c_call(
                    out, SharpBuiltinType(BuiltinTypeGenerator('void')), sharp_class.class_generator.add_ref_method,
                    ['other.{get_raw}()'.format(get_raw=self.params.get_raw_pointer_method_name)])

    def generate_raw_copy_constructor_body_definition(self, out: FileGenerator, sharp_class, add_ref_object):
        out.put_line('SetObject(object_pointer);')
        out.put_line('if ({add_ref_object} && object_pointer != IntPtr.Zero)'.format(add_ref_object=add_ref_object))
        with IndentScope(out):
            self.lifecycle_traits.create_exception_traits(sharp_class.class_generator.class_object,
                                                          self.capi_generator.capi_generator)
            exception_traits = SharpExceptionTraits(self.lifecycle_traits.init_method_exception_traits,
                                                    self.capi_generator.params)
            exception_traits.generate_c_call(
                out, SharpBuiltinType(BuiltinTypeGenerator('void')),
                sharp_class.class_generator.add_ref_method, ['object_pointer'])

    def __generate_raw_copy_constructor_definition(self, out: FileGenerator, sharp_class):
        constructor_arguments = 'ECreateFromRawPointer e, IntPtr object_pointer, bool add_ref_object'
        out.put_line('unsafe public {class_name}({arguments}){base_init}'.format(
            class_name=sharp_class.wrap_name,
            arguments=constructor_arguments,
            base_init=get_base_init(sharp_class))
        )
        with IndentScope(out):
            self.generate_raw_copy_constructor_body_definition(out, sharp_class, 'add_ref_object')

    def __generate_deallocate(self, out: FileGenerator, sharp_class):
        out.put_line('if ({get_raw}() != IntPtr.Zero)'.format(
            get_raw=self.params.get_raw_pointer_method_name))
        with IndentScope(out):
            self.lifecycle_traits.finish_method_exception_traits.generate_c_call(
                out, BuiltinTypeGenerator('void'), sharp_class.class_generator.release_method,
                ['{get_raw}()'.format(get_raw=self.params.get_raw_pointer_method_name)])
            out.put_line('SetObject(IntPtr.Zero);')

    def __generate_destructor(self, out: FileGenerator, sharp_class):
        out.put_line('unsafe ~{class_name}()'.format(
            class_name=sharp_class.wrap_name)
        )
        with IndentScope(out):
            self.__generate_deallocate(out, sharp_class)

    def generate_std_methods_definitions(self, out: FileGenerator, sharp_class):
        self.__generate_copy_constructor_definition(out, sharp_class)
        out.put_line('')
        self.__generate_raw_copy_constructor_definition(out, sharp_class)
        out.put_line('')
        self.__generate_destructor(out, sharp_class)
        out.put_line('')
        super().generate_std_methods_definitions(out, sharp_class)


class SharpWatchdogScope(WatchdogScope):
    def __enter__(self):
        self.file_generator.put_line('#if !{}'.format(self.watchdog_string))
        self.file_generator.put_line('#define {}'.format(self.watchdog_string))
        self.file_generator.put_line('')


class SharpExceptionTraits(object):
    def __init__(self, exception_traits, params):
        self.exception_traits = exception_traits
        self.params = params
        self.classes = []
        self.check_and_throw_exception_filename = self.get_exception_filename(params)

    @staticmethod
    def get_exception_filename(params):
        result = params.check_and_throw_exception_filename
        reversed_name = result[::-1]
        dot = reversed_name.find('.')
        if -1 < dot < 6:
            result = result[:-dot - 1]
        return params.sharp_output_folder + '/' + result + '.cs'

    def __get_c_function_call(self, c_function_name: str, arguments: [str]) -> str:
        arguments.insert(0, 'out {exception_info}'.format(exception_info=self.params.exception_info_argument_name))
        return '{function_name}({arguments})'.format(function_name=c_function_name, arguments=', '.join(arguments))

    def __generate_c_call(self, out: FileGenerator, instructions: ([str], str)) -> str:
        out.put_line('{exception_info_type} {exception_info};'.format(
            exception_info_type=self.exception_info_t(),
            exception_info=self.params.exception_info_argument_name))
        casting_instructions, return_expression = instructions
        out.put_lines(casting_instructions)
        out.put_line('{0}.Functions.check_and_throw_exception({1}.code, {1}.object_pointer);'.format(
            self.params.beautiful_capi_namespace,
            self.params.exception_info_argument_name))
        return return_expression

    def generate_c_call(self, out: FileGenerator, return_type, c_function_name: str, arguments: [str]) -> str:
        if isinstance(self.exception_traits, NoHandling):
            casting_instructions, return_expression = return_type.c_2_wrap_var(
                '', NoHandling.get_c_function_call(c_function_name, arguments))
            out.put_lines(casting_instructions)
            return return_expression
        casting_instructions, return_expression = return_type.c_2_wrap_var(
            'result', self.__get_c_function_call(c_function_name, arguments))
        return self.__generate_c_call(out, (casting_instructions, return_expression))

    def exception_info_t(self):
        return self.params.beautiful_capi_namespace.lower() + '_exception_info_t'

    def __exception_code_t(self):
        return self.params.beautiful_capi_namespace.lower() + '_exception_code_t'

    @staticmethod
    def __generate_throw_wrap(out, exception_class):
        throw_str = 'throw new {0}({0}.ECreateFromRawPointer.force_creating_from_raw_pointer, exception_object, false);'
        out.put_line(throw_str.format(exception_class.full_wrap_name))

    def generate_exception_info(self, out: FileGenerator):
        out.put_line('unsafe public struct {}_exception_info_t'.format(self.params.beautiful_capi_namespace.lower()))
        with IndentScope(out):
            out.put_line('public System.UInt32 code;')
            out.put_line('public IntPtr object_pointer;')
        out.put_line('')

    def generate_exception_code(self, sharp_capi_generator, out: FileGenerator):
        prefix = self.params.beautiful_capi_namespace.lower()
        out.put_line('public enum {}_exception_code_t'.format(prefix))
        with IndentScope(out, '};'):
            out.put_line('{}_no_exception = 0,'.format(prefix))
            out.put_line('{}_unknown_exception = 1,'.format(prefix))
            code_to_exception = [[exception_class.class_generator.exception_code, exception_class] for exception_class
                                 in sharp_capi_generator.main_exception_traits.classes]
            if code_to_exception:
                out.put_line('{}_copy_exception_error = 2,'.format(prefix))
                code_to_exception.sort(key=lambda except_info: except_info[0])
                for exception_info in code_to_exception[:-1]:
                    out.put_line('{2}_{0} = {1},'.format(
                        exception_info[1].c_name, exception_info[0], prefix))
                exception_info = code_to_exception[-1]
                out.put_line('{2}_{0} = {1}'.format(
                    exception_info[1].c_name, exception_info[0], prefix))
            else:
                out.put_line('{}_copy_exception_error = 2'.format(prefix))
        out.put_line('')

    def modify_c_arguments(self, arguments: [str]):
        if isinstance(self.exception_traits, ExceptionTraits.ByFirstArgument):
            arguments.insert(0, 'out {exception_info_type} {exception_info}'.format(
                exception_info_type=self.exception_info_t(),
                exception_info=self.params.exception_info_argument_name
            ))


class SharpFileCache(object):
    def __init__(self, file_cache):
        self.file_cache = file_cache
        self.base_path = file_cache.params.sharp_output_folder

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

    def get_file_for_namespace(self, path_to_namespace: [str]) -> FileGenerator:
        output_file_name = self.__get_file_name_base_for_namespace_common(path_to_namespace, OsJoin(self.base_path))
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


class SharpCmakeListGenerator(object):
    def __init__(self, capi_generator, namespaces: []):
        self.capi_generator = capi_generator
        self.params = capi_generator.params
        self.name = capi_generator.capi_generator.api_root.project_name
        self.lib_suffix = '_sharp_library'
        self.lib_name = pascal_to_stl(self.name + self.lib_suffix)
        if self.params.sharp_library_name:
            self.lib_name = self.params.sharp_library_name
        self.namespaces = [capi_generator.full_name_2_sharp_object[namespace.full_wrap_name] for namespace in
                           namespaces]
        self.out_folder = capi_generator.params.sharp_output_folder
        self.file = FileGenerator(self.out_folder + '/CMakeLists.txt')
        self.name_stack = []
        self.dependencies = []
        self.project_path = ''

    def put_dependency_lib(self, project_name: str, out: FileGenerator):
        out.put_line('if (TARGET {0})'.format(project_name))
        with Indent(out):
            out.put_line('add_dependencies({0} {1})'.format(self.lib_name, project_name))
        out.put_line('endif()')

    def put_link_lib(self, project_name: str, out: FileGenerator):
        out.put_line('target_link_libraries({0} {1})'.format(self.lib_name, project_name))

    def process_class(self, class_: SharpClass):
        path_to_class = '/'.join(self.name_stack + [class_.wrap_name])
        self.put_file(self.project_path + '/' + path_to_class + '.cs')
        pass

    def process_template(self, template: SharpTemplate):
        filename = template.template_generator.template_class_generator.wrap_short_name + '.cs'
        self.put_file('/'.join([self.project_path] + self.name_stack + [filename]))
        self.name_stack.append(template.wrap_short_name)
        for class_ in template.classes:
            self.process_class(class_)
        self.name_stack.pop()

    def process_external_namespace(self, external_namespace):
        if external_namespace.project_name and external_namespace.project_name not in self.dependencies:
            self.dependencies.append(external_namespace.project_name)
        for nested_namespace in external_namespace.nested_namespaces:
            self.process_external_namespace(nested_namespace)

    def process_namespace(self, namespace):
        if not self.name_stack:
            self.put_file(self.project_path + '/' + namespace.wrap_name + '/' + namespace.wrap_name + 'Init.cs')
        self.put_file('/'.join([self.project_path] + self.name_stack + [namespace.wrap_name + 'Functions.cs']))
        if namespace.enums:
            self.put_file('/'.join([self.project_path] + self.name_stack + [namespace.wrap_name + 'Enums.cs']))
        self.name_stack.append(namespace.wrap_name)
        for nested_namespace in namespace.nested_namespaces.values():
            self.process_namespace(nested_namespace)
        for class_ in namespace.classes.values():
            self.process_class(class_)
        for template in namespace.templates.values():
            self.process_template(template)
        for external_namespace in namespace.external_namespaces:
            self.process_external_namespace(external_namespace)
        self.name_stack.pop()

    def put_file(self, file_path: str):
        self.file.put_line('"' + file_path + '"')

    def generate(self):
        self.file.put_line('project({library_name} LANGUAGES CSharp)\n'.format(library_name=self.lib_name))
        self.file.put_line('cmake_minimum_required(VERSION 3.8.2)\n')
        self.file.put_line('add_library({library_name} SHARED'.format(library_name=self.lib_name))
        self.project_path = '${{{library_name}_SOURCE_DIR}}'.format(library_name=self.lib_name)
        with Indent(self.file):
            for namespace in self.namespaces:
                self.process_namespace(namespace)
                if not isinstance(self.capi_generator.main_exception_traits.exception_traits, NoHandling):
                    file = self.capi_generator.params.check_and_throw_exception_filename.format(project_name=self.name)
                    self.put_file(self.project_path + '/' + file.replace('.h', '.cs'))
                if self.capi_generator.generate_string_marshaler:
                    filename = self.project_path + '/' + self.params.beautiful_capi_namespace + '/StringMarshaler.cs'
                    self.put_file(filename)
        self.file.put_line(')\n')
        self.file.put_line('target_compile_options({0} PRIVATE "/unsafe")'.format(self.lib_name))
        self.file.put_line('SET_TARGET_PROPERTIES({0} PROPERTIES LINKER_LANGUAGE CSharp)'.format(self.lib_name))
        self.put_dependency_lib(pascal_to_stl(self.name), self.file)
        self.put_link_lib(pascal_to_stl(self.name), self.file)
        for dependency in self.dependencies:
            lib_name = pascal_to_stl(dependency + self.lib_suffix)
            self.put_dependency_lib(lib_name, self.file)
            self.put_link_lib(lib_name, self.file)
            self.file.put_line('')


class SharpExternalNamespace(object):
    def __init__(self, generator: ExternalNamespaceGenerator, parent, capi_generator: SharpCapiGenerator):
        self.generator = generator
        self.parent = parent
        self.nested_namespaces = []
        self.classes = []
        self.enums = []
        self.project_name = generator.namespace_object.project_name
        self.capi_generator = capi_generator

    @property
    def wrap_name(self):
        return self.generator.wrap_name

    @property
    def full_wrap_name(self):
        return self.parent.full_wrap_name + '.' + self.wrap_name if self.parent else self.wrap_name

    def generate(self):
        self.nested_namespaces = []
        for ns in self.generator.nested_namespaces:
            external_namespace = SharpExternalNamespace(ns, self, self.capi_generator)
            self.nested_namespaces.append(external_namespace)
            external_namespace.generate()
        self.classes = []
        for class_ in self.generator.classes:
            external_class = self.capi_generator.get_or_gen_external_class('.'.join(class_.full_name_array), class_)
            self.classes.append(external_class)
        self.enums = []
        for enum in self.generator.enums:
            external_enum = SharpExternalEnum(enum, self)
            self.enums.append(external_enum)


class SharpExternalClass(object):
    def __init__(self,
                 generator: ExternalClassGenerator,
                 parent: ExternalNamespaceGenerator,
                 capi_generator: SharpCapiGenerator):
        self.generator = generator
        self.parent = parent
        self.capi_generator = capi_generator
        self.enums = [SharpExternalEnum(enum, self) for enum in generator.enums]

    @property
    def wrap_name(self):
        return self.generator.wrap_name

    @property
    def full_wrap_name(self):
        return '{0}.{1}'.format(self.parent.full_wrap_name, self.wrap_name) if self.parent else self.wrap_name

    def wrap_argument_declaration(self) -> str:
        return self.full_wrap_name

    @staticmethod
    def c_argument_declaration() -> str:
        return 'IntPtr'

    def c_2_wrap_var(self, result_var: str, expression: str) -> ([str], str):
        parent_full_name = self.parent.full_wrap_name
        internal_expression = '{type_name}.{create_from_ptr_expression}, {expression}, {copy_or_add_ref}'.format(
            create_from_ptr_expression='ECreateFromRawPointer.force_creating_from_raw_pointer',
            type_name=parent_full_name + '.' + self.wrap_name,
            expression=expression,
            copy_or_add_ref=bool_to_str(False))  # self.copy_or_add_ref_when_c_2_wrap))
        if result_var:
            return ['var {result_var} = new {type_name}({internal_expression});'.format(
                type_name=parent_full_name + '.' + self.wrap_name,
                result_var=result_var,
                internal_expression=internal_expression
            )], result_var
        else:
            return [], 'new {type_name}({internal_expression})'.format(
                type_name=parent_full_name + '.' + self.wrap_name,
                internal_expression=internal_expression
            )

    def wrap_2_c_var(self, result_var: str, expression: str) -> ([str], str):
        internal_expression = '{expression}.{get_raw_pointer_method}()'.format(
            expression=expression,
            get_raw_pointer_method=self.generator.get_raw_pointer_method_name)
        if result_var:
            return ['IntPtr {result_var} = {internal_expression};'.format(
                result_var=result_var,
                internal_expression=internal_expression
            )], result_var
        else:
            return [], internal_expression


class SharpExternalEnum(SharpEnum):
    def __init__(self, enum_generator, parent: ExternalNamespaceGenerator or ExternalClassGenerator):
        super().__init__(enum_generator, parent)


def generate_requires_cast_to_base_set_object_definition(out: FileGenerator, sharp_class: SharpClass):
    new = 'new ' if sharp_class.base else ''
    out.put_line('{0}unsafe protected void SetObject(IntPtr object_pointer)'.format(new))
    with IndentScope(out):
        out.put_line('mObject = object_pointer;')
        if sharp_class.base:
            out.put_line('if (mObject != IntPtr.Zero)')
            with IndentScope(out):
                out.put_line('base.SetObject({cast_to_base}(mObject));'.format(
                    cast_to_base=sharp_class.class_generator.cast_to_base
                ))
            out.put_line('else')
            with IndentScope(out):
                out.put_line('base.SetObject(IntPtr.Zero);')


def generate_simple_case_set_object_definition(out: FileGenerator, sharp_class):
    if sharp_class.base:
        out.put_line('unsafe protected override void SetObject(IntPtr object_pointer)')
    else:
        out.put_line('unsafe protected virtual void SetObject(IntPtr object_pointer)')
    with IndentScope(out):
        if sharp_class.base:
            out.put_line('base.SetObject(object_pointer);')
        else:
            out.put_line('mObject = object_pointer;')


def generate_set_object_definition(inheritance_traits, out: FileGenerator, sharp_class):
    if isinstance(inheritance_traits, RequiresCastToBase):
        generate_requires_cast_to_base_set_object_definition(out, sharp_class)
    else:
        generate_simple_case_set_object_definition(out, sharp_class)


def generate_requires_cast_to_base_object_field_definition(out: FileGenerator, sharp_class: SharpClass):
    new = 'new ' if sharp_class.base else ''
    out.put_line('{0}protected unsafe IntPtr mObject;'.format(new))


def generate_simple_case_object_field_definition(out: FileGenerator, sharp_class):
    if not sharp_class.base:
        out.put_line('protected unsafe IntPtr mObject;')


def generate_object_field_definition(inheritance_traits, out: FileGenerator, sharp_class):
    if isinstance(inheritance_traits, RequiresCastToBase):
        generate_requires_cast_to_base_object_field_definition(out, sharp_class)
    else:
        generate_simple_case_object_field_definition(out, sharp_class)


def get_template_base_init(template: SharpTemplate):
    base = template.base
    if base:
        return ' : base({0}.{1}, obj)'.format(base.wrap_name, 'ECreateFromObject.create_from_object')
    return ''


def get_base_init(sharp_class: SharpClass):
    base = sharp_class.base
    if base:
        base_class_name = '.'.join(base.class_generator.parent_namespace.full_name_array + [base.wrap_name])
        create_from_raw_ptr_expession = 'ECreateFromRawPointer.force_creating_from_raw_pointer'
        return ' : base({base}.{expr}, IntPtr.Zero, false)'.format(base=base_class_name,
                                                                   expr=create_from_raw_ptr_expession)
    return ''


sharp_lifecycles = {}

str_to_sharp_lifecycle = {
    TLifecycle.copy_semantic: SharpCopySemantic,
    TLifecycle.raw_pointer_semantic: SharpRawPointerSemantic,
    TLifecycle.reference_counted: SharpRefCountedSemantic
}


def create_sharp_lifecycle(lifecycle: TLifecycle,
                           lifecycle_traits: LifecycleTraits,
                           capi_generator: CapiGenerator) -> SharpLifecycleTraits:
    if lifecycle not in sharp_lifecycles:
        result = str_to_sharp_lifecycle[lifecycle](lifecycle_traits, capi_generator)
        sharp_lifecycles[lifecycle] = result
    else:
        result = sharp_lifecycles[lifecycle]
    return result


def generate(cpp_file_cache: FileCache, capi_generator: CapiGenerator, namespace_generators: []):
    sharp_capi_generator = SharpCapiGenerator(SharpFileCache(cpp_file_cache), capi_generator)
    sharp_capi_generator.generate(namespace_generators)
    sharp_capi_generator.generate_exception_traits()
    if capi_generator.params.generate_sharp_library:
        project_gen = SharpCmakeListGenerator(sharp_capi_generator, namespace_generators)
        project_gen.generate()
