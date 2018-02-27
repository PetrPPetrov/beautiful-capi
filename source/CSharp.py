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

from NamespaceGenerator import NamespaceGenerator
import CapiGenerator
from ClassGenerator import ClassGenerator
from LifecycleTraits import LifecycleTraits, RawPointerSemantic, CopySemantic
from ArgumentGenerator import ArgumentGenerator, MappedTypeGenerator, ClassTypeGenerator
from BuiltinTypeGenerator import BuiltinTypeGenerator
from MethodGenerator import MethodGenerator, ConstructorGenerator, FunctionGenerator
from FileGenerator import FileGenerator, IndentScope, Indent
from Helpers import if_required_then_add_empty_line, bool_to_str, replace_template_to_filename, BeautifulCapiException, \
    pascal_to_stl
from Helpers import get_template_name
from Parser import TLifecycle
from InheritanceTraits import RequiresCastToBase
from ExceptionTraits import NoHandling
from FileCache import FileCache, OsJoin, PosixJoin
from TemplateGenerator import TemplateGenerator, TemplateConstantArgumentGenerator

full_name_2_sharp_object = {}


class SharpNamespace(object):
    def __init__(self, namespace_generator: NamespaceGenerator, parent_namespace=None):
        self.namespace_generator = namespace_generator
        self.parent_namespace = parent_namespace
        self.nested_namespaces = {}
        self.classes = {}
        self.enums = [SharpEnum(enum, self) for enum in namespace_generator.enum_generators]
        self.functions = [SharpFunction(func, self) for func in namespace_generator.functions]
        self.capi_generator = None
        self.file_cache = None
        self.wrap_name = namespace_generator.wrap_name
        self.full_wrap_name = '.'.join(namespace_generator.full_name_array)
        self.mapped_types = {}
        self.templates = {}

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
        file = self.file_cache.get_file_for_class(self.full_name_array + [self.wrap_name + 'Init'])
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
        file = self.file_cache.get_file_for_class(self.full_name_array[:-1] + [self.wrap_name + 'Functions'])
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

    def generate(self, file_cache, capi_generator: CapiGenerator):
        self.capi_generator = capi_generator
        self.file_cache = file_cache
        if self.enums:
            enums_header = self.enums[0].generate_enums_header(file_cache)
            self.increase_indent_recursively(enums_header)
            for enum in self.enums:
                enum.generate_enum_definition(enums_header)

            self.decrease_indent_recursively(enums_header)

        self.nested_namespaces = {ns.name: SharpGenerator.get_or_gen_namespace(ns.full_wrap_name, ns)
                                  for ns in self.namespace_generator.nested_namespaces}
        for nested_namespace in self.nested_namespaces.values():
            nested_namespace.generate(file_cache, capi_generator)
        if not self.parent_namespace:
            self.__generate_initialisation_class()
        if self.functions:
            self.__generate_functions_class()
        for template_generator in self.namespace_generator.templates:
            generator = template_generator.template_class_generator
            template = SharpGenerator.get_or_gen_template('.'.join(generator.full_name_array), template_generator)
            self.templates[generator.name] = template
        for class_ in self.namespace_generator.classes:
            full_class_name = '.'.join(class_.full_template_name_array).replace('::', '.')
            sharp_class = SharpGenerator.get_or_gen_class(full_class_name, class_)
            if class_.is_template:
                template_name = get_template_name(class_.name)
                template = self.get_template(template_name)
                if template:
                    template.classes.append(sharp_class)
                    self.templates[template_name] = template
            else:
                self.classes['.'.join(class_.full_template_name_array)] = sharp_class
        for class_generator in self.classes.values():
            class_generator.generate()
        if self.namespace_generator.namespace_object.implementation_header_filled:
            capi_generator.additional_includes.include_user_header(
                self.namespace_generator.namespace_object.implementation_header)
        for template in self.templates.values():
            template.generate(file_cache)

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
        self.file_cache = None
        self.lifecycle_traits = create_sharp_lifecycle(class_generator.class_object.lifecycle,
                                                       class_generator.lifecycle_traits)
        self.enums = [SharpEnum(enum, self) for enum in class_generator.enum_generators]
        self.base = None
        self.template_arguments = []

    @property
    def is_template(self):
        return self.class_generator.is_template

    @staticmethod
    def template_2_wrap(name: str) -> str:
        result = name
        result = result.replace('<', '_')
        result = result.replace('>', '')
        result = result.replace('::', '.')
        result = result.replace(' ', '')
        result = result.replace(',', '_')
        return result

    @property
    def wrap_name(self):
        return self.template_2_wrap(self.template_name) if self.is_template else self.class_generator.wrap_name

    @property
    def wrap_short_name(self):
        return self.class_generator.wrap_short_name if self.is_template else self.class_generator.wrap_name

    @property
    def full_name_array(self):
        return self.namespace.full_name_array + [self.wrap_name]

    @property
    def full_wrap_name(self):
        return self.namespace.full_wrap_name + '.' + self.wrap_name

    @property
    def template_name(self):
        result = self.class_generator.class_object.typedef_name
        if not result:
            arguments = ', '.join(arg.wrap_argument_declaration(self.namespace.full_name_array)for arg in self.template_arguments)
            result = '{name}<{arguments}>'.format(name=self.class_generator.wrap_short_name, arguments=arguments)
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
            self.base = SharpGenerator.get_or_gen_class(base_class_name, base)

    def __generate_definition(self):
        name_array = self.namespace.full_name_array + [self.wrap_short_name, self.wrap_name]
        definition_header = self.file_cache.get_file_for_class(name_array if self.is_template else self.full_name_array)
        definition_header.put_begin_cpp_comments(self.class_generator.params)
        definition_header.put_line('using System.Runtime.InteropServices;\n')
        self.namespace.increase_indent_recursively(definition_header)
        definition_header.put_line('public class {class_name}{base} '.format(
            class_name=self.wrap_name,
            base=': {0}'.format(self.base.wrap_name) if self.base else ''
        ))
        with IndentScope(definition_header):
            self.__generate_export_functions()
            definition_header.put_line('')
            new = 'new ' if self.base else ''
            definition_header.put_line('%spublic enum ECreateFromRawPointer{force_creating_from_raw_pointer};' % new)
            definition_header.put_line('')
            definition_header.put_line('{0}protected unsafe void* mObject;'.format(new))
            definition_header.put_line('')
            if self.enums:
                for enum in self.enums:
                    enum.generate_enum_definition(definition_header)
                definition_header.put_line('')
            first_method = True
            first_method = self.__generate_constructor_definitions(definition_header, first_method)
            self.__generate_method_definitions(definition_header, first_method)
            definition_header.put_line('')
            self.lifecycle_traits.generate_std_methods_definitions(definition_header, self)
            definition_header.put_line('')
            if hasattr(self, 'extension_base_class_generator'):
                self.class_generator.generate_cast_name_definition(definition_header)
                definition_header.put_line('')
            generate_set_object_definition(
                self.class_generator.inheritance_traits,
                definition_header,
                self
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
        name_array = self.namespace.full_name_array + [self.wrap_short_name, self.wrap_name]
        header = self.file_cache.get_file_for_class(name_array if self.is_template else self.full_name_array)
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
        if self.base:
            header.put_line(import_string)
            header.put_line('unsafe static extern void* {func_name}(void* object_pointer);'.format(
                func_name=self.class_generator.cast_to_base))

    def generate(self):
        self.file_cache = self.namespace.file_cache
        self.gen_base_class()
        if self.is_template:
            template_arguments = self.class_generator.template_argument_generators
            self.template_arguments = [SharpArgument(ArgumentGenerator(arg, "")) for arg in template_arguments]
        self.__generate_definition()


class SharpTemplate(object):
    def __init__(self, template_generator: TemplateGenerator):
        self.template_generator = template_generator
        self.namespace = SharpGenerator.get_or_gen_namespace(
            '.'.join(template_generator.parent_namespace.full_name_array),
            template_generator.parent_namespace
        )
        self.constructors = []
        self.methods = []
        self.classes = []
        self.base = None
        self.explicit_arguments = []
        self.arguments = []
        self.non_types = ('template', 'typename', 'class')

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
                base_init=' :this(ECreateFromObject.create_from_object, {obj})'.format(obj=certain)
            ))
            out.put_line('{}')
            out.put_line('')

    def __generate_methods_definitions(self, out: FileGenerator):
        for method in self.methods:
            new = 'new ' if method.is_overload() else ''
            return_type = method.return_type.wrap_argument_declaration(self.namespace.full_name_array)
            arguments = [arg.wrap_argument_declaration(self.namespace.full_name_array) for arg in method.arguments]
            out.put_line('{new}public {return_type} {method_name}({arguments})'.format(
                method_name=method.method_generator.wrap_name, new=new,
                arguments=', '.join(arguments), return_type=return_type
            ))
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
                    name=method.method_generator.wrap_name,
                    bracket=')' if return_expression else '',
                    arguments=', '.join(argument.argument_generator.name for argument in method.arguments)
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
                        argument = full_name_2_sharp_object[argument].wrap_name
                        class_name_array.append(argument)
                    else:
                        class_name_array.append(arg.value)
                    if template_arguments[arg.name] not in self.non_types:
                        inst_arguments.append(argument)
                    else:
                        inst_arguments.append('typeof({0}).Name'.format(argument))
                certain_class = instantiation.typedef_name if instantiation.typedef_name else '_'.join(class_name_array)
                type_map.append((' + "_" + '.join(inst_arguments), certain_class))

            out.put_lines(['{{ {0}, typeof({1}) }}'.format(value[0], value[1]) for value in type_map[:-1]], ',\n')
            out.put_line('{{ {0}, typeof({1}) }}'.format(type_map[-1][0], type_map[-1][1]))

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

    def __generate__get_certain_class(self, out: FileGenerator):
        out.put_line('{new}public object GetCertainClass()'.format(new='new ' if self.base else ''))
        with IndentScope(out):
            out.put_line('return mObject;')

    def __generate__certain_2_template(self, out: FileGenerator):
        new = 'new ' if self.base else ''
        out.put_line('private static TemplateArgument Certain2Template<TemplateArgument>(object obj)'.format(new))
        with IndentScope(out):
            out.put_line('Type type = typeof(TemplateArgument);')
            out.put_line('if (type.GetMethod("GetCertainType") != null)')
            with IndentScope(out):
                out.put_line('var enumeration = Enum.Parse(type.GetNestedType("ECreateFromObject"), '
                             '"create_from_object");')
                out.put_line('return (TemplateArgument)type.GetConstructors()[0].Invoke(new object[] '
                             '{ enumeration, obj });')
            out.put_line('return (TemplateArgument)obj;')

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

    def __generate_std_method_definition(self, out: FileGenerator, name: str, return_type: str='void',
                                         arguments=(), keywords=('unsafe', 'public', )):
        if self.base:
            keywords = (('new', ) + keywords)
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

    def generate_definition(self, out: FileGenerator):
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
            out.put_line('')
            out.put_line('{new}public enum ECreateFromObject {{create_from_object}};'.format(new=new))
            out.put_line('')
            self.__generate_constructor_definitions(out)
            self.__generate_std_methods_definitions(out)
            self.__generate_methods_definitions(out)
            self.__generate__type_2_name(out)
            out.put_line('')
            self.__generate__get_certain_type_(out)
            out.put_line('')
            self.__generate__execute_method_(out)
            out.put_line('')
            self.__generate__get_certain_class(out)
            out.put_line('')
            self.__generate__certain_2_template(out)
            out.put_line('')
            out.put_line('{new}private object mObject;'.format(new=new))
        self.namespace.decrease_indent_recursively(out)

    def generate(self, file_cache):
        header = file_cache.get_file_for_class(self.namespace.full_name_array + [self.wrap_short_name])
        base_name = self.template_generator.template_class.base
        if base_name:
            base_name = get_template_name(base_name)
            base_name_array = SharpClass.get_relative_name_array(self.namespace.full_name_array, base_name.split('::'))
            self.base = self.namespace.find_object(base_name_array)
        for argument in self.template_generator.template_object.arguments:
            if argument.type_name not in ['template', 'class', 'typename']:
                self.explicit_arguments.append((argument.type_name, argument.name))
            type_name = full_name_2_sharp_object.get(argument.type_name.replace('::', '.'), None)
            self.arguments.append((argument.name, type_name if type_name else argument.type_name, ))
        for constructor in self.template_generator.template_class_generator.constructor_generators:
            self.constructors.append(SharpConstructor(constructor, self))
        for method in self.template_generator.template_class_generator.method_generators:
            self.methods.append(SharpMethod(method, self))
        for class_ in self.classes:
            class_.generate()
        if not self.classes:
            raise BeautifulCapiException('Template {name} has no classes'.format(name=self.wrap_short_name))
        self.generate_definition(header)


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

    def wrap_decl(self, base=None) -> str:
        return self.wrap_argument_declaration(base)

    def wrap_argument_declaration(self, base=None) -> str:
        generator = self.argument_generator.type_generator
        if isinstance(generator, ClassTypeGenerator):
            sharp_class = SharpGenerator.get_or_gen_class(
                '.'.join(generator.class_argument_generator.full_template_name_array).replace('::', '.'),
                generator.class_argument_generator
            )
            argument_type = sharp_class.full_wrap_name
        elif isinstance(generator, MappedTypeGenerator):
            if generator.mapped_type_object.sharp_wrap_type:
                argument_type = generator.mapped_type_object.sharp_wrap_type
            else:
                argument_type = generator.wrap_argument_declaration()
        elif isinstance(generator, TemplateConstantArgumentGenerator):
            argument_type = generator.value
        else:
            argument_type = generator.wrap_argument_declaration()
        argument_type = argument_type.replace('::', '.')
        if base:
            argument_type = SharpClass.get_relative_name(base, argument_type.split('.'))
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
        generator = self.argument_generator.type_generator
        if isinstance(generator, MappedTypeGenerator):
            return generator.format(
                generator.mapped_type_object.c_2_wrap,
                expression,
                result_var,
                generator.mapped_type_object.wrap_type
            )
        elif isinstance(generator, ClassTypeGenerator):
            parent_full_name = '.'.join(generator.class_argument_generator.parent_namespace.full_name_array)
            sharp_class = SharpGenerator.get_or_gen_class(
                parent_full_name + '.' + generator.class_argument_generator.template_name.replace('::', '.'),
                generator.class_argument_generator)
            internal_expression = '{type_name}.{create_from_ptr_expression}, {expression}, {copy_or_add_ref}'.format(
                create_from_ptr_expression='ECreateFromRawPointer.force_creating_from_raw_pointer',
                type_name=parent_full_name + '.' + sharp_class.wrap_name,
                expression=expression,
                copy_or_add_ref=bool_to_str(generator.copy_or_add_ref_when_c_2_wrap)
            )
            if result_var:
                return ['new {type_name} {result_var}({internal_expression});'.format(
                    type_name=parent_full_name + '.' + sharp_class.wrap_name,
                    result_var=result_var,
                    internal_expression=internal_expression
                )], result_var
            else:
                return [], 'new {type_name}({internal_expression})'.format(
                    type_name=parent_full_name + '.' + sharp_class.wrap_name,
                    internal_expression=internal_expression
                )
        else:
            return generator.c_2_wrap_var(result_var, expression)


class SharpMethod(object):
    def __init__(self, method_generator: MethodGenerator, generator: SharpClass or SharpTemplate):
        self.method_generator = method_generator
        self.generator = generator
        self.arguments = [SharpArgument(arg) for arg in method_generator.argument_generators]
        self.return_type = SharpArgument(ArgumentGenerator(method_generator.return_type_generator, ''))
        self.exception_traits = SharpExceptionTraits(method_generator.exception_traits)

    def is_overload(self):
        if self.generator.base:
            for method in self.generator.base.methods:
                if self.method_generator.name != method.method_generator.name:
                    continue
                return_type = self.method_generator.return_type_generator.type_name
                if return_type != method.method_generator.return_type_generator.type_name:
                    continue
                result = True
                for arg in self.method_generator.argument_generators:
                    if arg.type_generator != method.method_generator.argument_generators.type_generator:
                        result = False
                        break
                if result:
                    return True
        return False

    def generate_wrap_definition(self, out: FileGenerator):
        new = ''
        if self.is_overload:
            new = 'new '
        arguments = ', '.join(argument.wrap_argument_declaration() for argument in self.arguments)
        arguments_call = [argument.wrap_2_c() for argument in self.method_generator.c_arguments_list]
        out.put_line('{new}unsafe public {return_type} {name}({arguments})'.format(
            return_type=self.return_type.wrap_argument_declaration(), new=new,
            name=self.method_generator.wrap_name, arguments=arguments
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
    def __init__(self, constructor_generator: ConstructorGenerator, generator: SharpClass or SharpTemplate):
        self.constructor_generator = constructor_generator
        self.generator = generator
        self.arguments = [SharpArgument(arg) for arg in constructor_generator.argument_generators]

    def generate_wrap_definition(self, out: FileGenerator, capi_generator: CapiGenerator):
        self.constructor_generator.exception_traits = capi_generator.get_exception_traits(
            self.constructor_generator.constructor_object.noexcept)
        arguments = ', '.join(argument.wrap_argument_declaration() for argument in self.arguments)
        arguments_call = [argument.wrap_2_c() for argument in self.constructor_generator.argument_generators]
        out.put_line('unsafe public {class_name}({arguments}){base_init}'.format(
            class_name=self.generator.wrap_name,
            arguments=arguments,
            base_init=get_base_init(self.generator) if self.generator.base else ''
        ))
        with IndentScope(out):
            result_expression = SharpExceptionTraits.generate_c_call(
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

    def generate_std_methods_definitions(self, out: FileGenerator, sharp_class: SharpClass):
        new = 'new ' if sharp_class.base else ''
        out.put_line('{new}unsafe public static {class_name} {null_method}()'.format(
            class_name=sharp_class.wrap_name,
            null_method=self.params.null_method_name,
            new=new))
        with IndentScope(out):
            out.put_line('return new {class_name}({class_name}.{force_create}, null, false);'.format(
                force_create='ECreateFromRawPointer.force_creating_from_raw_pointer',
                class_name=sharp_class.wrap_name))
        out.put_line('')
        out.put_line('{new}unsafe public bool {is_null_method}()'.format(
            is_null_method=self.params.is_null_method_name, new=new))
        with IndentScope(out):
            out.put_line('return {get_raw}() != null;'.format(get_raw=self.params.get_raw_pointer_method_name))
        out.put_line('')
        out.put_line('{new}unsafe public bool {is_not_null_method}()'.format(
            is_not_null_method=self.params.is_not_null_method_name, new=new))
        with IndentScope(out):
            out.put_line('return {get_raw}() != null;'.format(get_raw=self.params.get_raw_pointer_method_name))
        out.put_line('')
        out.put_line('unsafe public static bool operator!({class_name} obj)'.format(
            class_name=sharp_class.wrap_name))
        with IndentScope(out):
            out.put_line('return obj.{get_raw}() != null;'.format(get_raw=self.params.get_raw_pointer_method_name))
        out.put_line('')
        out.put_line('{new}unsafe public void* {detach_method}()'.format(
            detach_method=self.params.detach_method_name, new=new))
        with IndentScope(out):
            out.put_line('void* result = {get_raw}();'.format(get_raw=self.params.get_raw_pointer_method_name))
            out.put_line('SetObject(null);')
            out.put_line('return result;')
        out.put_line('')
        out.put_line('{new}unsafe public void* {get_raw_pointer_method}()'.format(
            get_raw_pointer_method=self.params.get_raw_pointer_method_name, new=new))
        with IndentScope(out):
            out.put_line('return mObject != null ? mObject: null;')


class SharpCopySemantic(SharpLifecycleTraits):
    def __init__(self, lifecycle_traits: CopySemantic):
        super().__init__(lifecycle_traits)

    def __generate_copy_constructor_definition(self, out: FileGenerator, sharp_class):
        out.put_line('unsafe public {class_name}({class_name} other){base_init}'.format(
            class_name=sharp_class.wrap_name,
            base_init=get_base_init(sharp_class))
        )
        with IndentScope(out):
            out.put_line('new {class_name}(ECreateFromRawPointer.force_creating_from_raw_pointer, null, false);'.format(
                class_name=sharp_class.wrap_name, ))
            out.put_line('if (other.{get_raw}() != null)'.format(get_raw=self.params.get_raw_pointer_method_name))
            with IndentScope(out):
                copy_result = self.lifecycle_traits.init_method_exception_traits.generate_c_call(
                    out, BuiltinTypeGenerator('void*'), sharp_class.class_generator.copy_method,
                    ['other.{get_raw}()'.format(get_raw=self.params.get_raw_pointer_method_name)])
                out.put_line('SetObject({copy_result});'.format(copy_result=copy_result))
            out.put_line('else')
            with IndentScope(out):
                out.put_line('SetObject(null);')

    def generate_raw_copy_constructor_body_definition(self, out: FileGenerator, sharp_class, copy_object):
        out.put_line('if (object_pointer != null && {copy_object})'.format(copy_object=copy_object))
        with IndentScope(out):
            copy_result = self.lifecycle_traits.init_method_exception_traits.generate_c_call(
                out, BuiltinTypeGenerator('void*'), sharp_class.class_generator.copy_method, ['object_pointer'])
            out.put_line('SetObject({copy_result});'.format(copy_result=copy_result))
        out.put_line('else')
        with IndentScope(out):
            out.put_line('SetObject(object_pointer);')

    def __generate_raw_copy_constructor_definition(self, out: FileGenerator, sharp_class):
        constructor_arguments = 'ECreateFromRawPointer e, void *object_pointer, bool copy_object'.format(
            class_name=sharp_class.wrap_name
        )
        out.put_line('unsafe public {class_name}({arguments}){base_init}'.format(
            class_name=sharp_class.wrap_name,
            arguments=constructor_arguments,
            base_init=get_base_init(sharp_class))
        )
        with IndentScope(out):
            self.generate_raw_copy_constructor_body_definition(out, sharp_class, 'copy_object')

    def __generate_deallocate(self, out: FileGenerator, sharp_class):
        out.put_line('if ({get_raw}() != null)'.format(
            get_raw=self.params.get_raw_pointer_method_name))
        with IndentScope(out):
            self.lifecycle_traits.finish_method_exception_traits.generate_c_call(
                out, BuiltinTypeGenerator('void'), sharp_class.class_generator.delete_method,
                ['{get_raw}()'.format(get_raw=self.params.get_raw_pointer_method_name)])
            out.put_line('SetObject(null);')

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
    def __init__(self, lifecycle_traits: LifecycleTraits):
        super().__init__(lifecycle_traits)

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
            arguments='ECreateFromRawPointer e, void *object_pointer, bool copy',
            base_init=get_base_init(sharp_class))
        )
        with IndentScope(out):
            RawPointerSemantic.generate_raw_copy_constructor_body_definition(out, sharp_class, '')

    def __generate_delete_method(self, out: FileGenerator, sharp_class):
        out.put_line('unsafe public void {delete_method}()'.format(
            delete_method=self.params.delete_method_name
        ))
        with IndentScope(out):
            out.put_line('if ({get_raw}() != null)'.format(
                get_raw=self.params.get_raw_pointer_method_name))
            with IndentScope(out):
                self.lifecycle_traits.finish_method_exception_traits.generate_c_call(
                    out, BuiltinTypeGenerator('void'), sharp_class.class_generator.delete_method,
                    ['{get_raw}()'.format(get_raw=self.params.get_raw_pointer_method_name)])
                out.put_line('SetObject(null);')

    def generate_std_methods_definitions(self, out: FileGenerator, sharp_class):
        self.__generate_copy_constructor_definition(out, sharp_class)
        out.put_line('')
        self.__generate_raw_copy_constructor_definition(out, sharp_class)
        out.put_line('')
        self.__generate_delete_method(out, sharp_class)
        out.put_line('')
        super().generate_std_methods_definitions(out, sharp_class)


class SharpRefCountedSemantic(SharpLifecycleTraits):
    def __init__(self, lifecycle_traits: LifecycleTraits):
        super().__init__(lifecycle_traits)

    def __generate_copy_constructor_definition(self, out: FileGenerator, sharp_class):
        out.put_line('unsafe public {class_short_name}({class_name} other){base_init}'.format(
            class_short_name=sharp_class.wrap_name,
            class_name=sharp_class.wrap_name,
            base_init=get_base_init(sharp_class))
        )
        with IndentScope(out):
            out.put_line('SetObject(other.{get_raw}());'.format(get_raw=self.params.get_raw_pointer_method_name))
            out.put_line('if (other.{get_raw}() != null)'.format(get_raw=self.params.get_raw_pointer_method_name))
            with IndentScope(out):
                self.lifecycle_traits.init_method_exception_traits.generate_c_call(
                    out, BuiltinTypeGenerator('void'), sharp_class.class_generator.add_ref_method,
                    ['other.{get_raw}()'.format(get_raw=self.params.get_raw_pointer_method_name)])

    def generate_raw_copy_constructor_body_definition(self, out: FileGenerator, sharp_class, add_ref_object):
        out.put_line('SetObject(object_pointer);')
        out.put_line('if ({add_ref_object} && object_pointer != null)'.format(add_ref_object=add_ref_object))
        with IndentScope(out):
            self.lifecycle_traits.init_method_exception_traits.generate_c_call(
                out, BuiltinTypeGenerator('void'), sharp_class.class_generator.add_ref_method, ['object_pointer'])

    def __generate_raw_copy_constructor_definition(self, out: FileGenerator, sharp_class):
        constructor_arguments = 'ECreateFromRawPointer e, void *object_pointer, bool add_ref_object'
        out.put_line('unsafe public {class_name}({arguments}){base_init}'.format(
            class_name=sharp_class.wrap_name,
            arguments=constructor_arguments,
            base_init=get_base_init(sharp_class))
        )
        with IndentScope(out):
            self.generate_raw_copy_constructor_body_definition(out, sharp_class, 'add_ref_object')

    def __generate_deallocate(self, out: FileGenerator, sharp_class):
        out.put_line('if ({get_raw}() != null)'.format(
            get_raw=self.params.get_raw_pointer_method_name))
        with IndentScope(out):
            self.lifecycle_traits.finish_method_exception_traits.generate_c_call(
                out, BuiltinTypeGenerator('void'), sharp_class.class_generator.release_method,
                ['{get_raw}()'.format(get_raw=self.params.get_raw_pointer_method_name)])
            out.put_line('SetObject(null);')

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


class SharpGenerator(object):
    @staticmethod
    def get_or_gen_namespace(fullname: str, generator: NamespaceGenerator):
        if fullname in full_name_2_sharp_object:
            return full_name_2_sharp_object[fullname]
        else:
            if generator.parent_namespace:
                parent = SharpGenerator.get_or_gen_namespace(generator.parent_namespace.full_wrap_name,
                                                             generator.parent_namespace)
                result = SharpNamespace(generator, parent)
            else:
                result = SharpNamespace(generator, None)
            full_name_2_sharp_object[fullname] = result
            return result

    @staticmethod
    def get_or_gen_class(fullname: str, generator: ClassGenerator):
        if fullname in full_name_2_sharp_object:
            return full_name_2_sharp_object[fullname]
        else:
            namespace = SharpGenerator.get_or_gen_namespace('.'.join(generator.parent_namespace.full_name_array),
                                                            generator.parent_namespace)
            result = SharpClass(generator, namespace)
            full_name_2_sharp_object[fullname] = result
            return result

    @staticmethod
    def get_or_gen_template(fullname: str, template_generator: TemplateGenerator):
        result = full_name_2_sharp_object.get(fullname, None)
        if not result:
            result = SharpTemplate(template_generator)
            full_name_2_sharp_object[fullname] = result
        return result


class SharpCmakeListGenerator(object):
    def __init__(self, capi_generator, namespaces: []):
        self.name = capi_generator.api_root.project_name
        self.params = capi_generator.params
        self.namespaces = [full_name_2_sharp_object[namespace.full_wrap_name] for namespace in namespaces]
        self.out_folder = capi_generator.params.sharp_output_folder
        self.file = FileGenerator(self.out_folder + '/CMakeLists.txt')
        self.name_stack = []
        self.project_path = ''

    def generate_class(self, class_: SharpClass):
        path_to_class = '/'.join(self.name_stack + [class_.wrap_name])
        self.file.put_line(self.project_path + '/' + path_to_class + '.cs')
        pass

    def generate_template(self, template: SharpTemplate):
        filename = template.template_generator.template_class_generator.wrap_name + '.cs'
        self.file.put_line('/'.join([self.project_path] + self.name_stack + [filename]))
        self.name_stack.append(template.wrap_short_name)
        for class_ in template.classes:
            self.generate_class(class_)
        self.name_stack.pop()

    def generate_namespace(self, namespace):
        if not self.name_stack:
            self.file.put_line(self.project_path + '/' + namespace.wrap_name + '/' + namespace.wrap_name + 'Init.cs')
        self.file.put_line('/'.join([self.project_path] + self.name_stack + [namespace.wrap_name + 'Functions.cs']))
        self.name_stack.append(namespace.wrap_name)
        for nested_namespace in namespace.nested_namespaces.values():
            self.generate_namespace(nested_namespace)
        for class_ in namespace.classes.values():
            self.generate_class(class_)
        for template in namespace.templates.values():
            self.generate_template(template)
        self.name_stack.pop()

    def generate(self):
        library_name = pascal_to_stl(self.name) + '_sharp_library'
        self.file.put_line('project({library_name} LANGUAGES CSharp)\n'.format(library_name=library_name))
        self.file.put_line('cmake_minimum_required(VERSION 3.8.2)\n')
        self.file.put_line('add_library({library_name} SHARED'.format(library_name=library_name))
        self.project_path = '${{{library_name}_SOURCE_DIR}}'.format(library_name=library_name)
        with Indent(self.file):
            for namespace in self.namespaces:
                self.generate_namespace(namespace)
        self.file.put_line(')\n')
        file_content = 'target_compile_options({library_name} PRIVATE "/unsafe")\n' \
                       'SET_TARGET_PROPERTIES({library_name} PROPERTIES LINKER_LANGUAGE CSharp)\n' \
                       'if(TARGET {project})\n' \
                       '    add_dependencies({library_name} {project})\n' \
                       '    target_link_libraries({library_name} {project})\n' \
                       'endif()\n'.format(library_name=library_name, project=pascal_to_stl(self.name))
        self.file.put_line(file_content)


def generate_requires_cast_to_base_set_object_definition(out: FileGenerator, sharp_class: SharpClass):
    new = 'new ' if sharp_class.base else ''
    out.put_line('{0}unsafe protected void SetObject(void* object_pointer)'.format(new))
    with IndentScope(out):
        out.put_line('mObject = object_pointer;')
        if sharp_class.base:
            out.put_line('if (mObject != null)')
            with IndentScope(out):
                out.put_line('base.SetObject({cast_to_base}(mObject));'.format(
                    cast_to_base=sharp_class.class_generator.cast_to_base
                ))
            out.put_line('else')
            with IndentScope(out):
                out.put_line('base.SetObject(null);')


def generate_simple_case_set_object_definition(out: FileGenerator, sharp_class):
    out.put_line('unsafe protected void {class_name}.SetObject(void* object_pointer)'.format(
        class_name=sharp_class.class_generator.full_wrap_name))
    with IndentScope(out):
        if sharp_class.base_class:
            out.put_line('{base_class}.SetObject(object_pointer);'.format(
                base_class=sharp_class.base_class.wrap_name))
        else:
            out.put_line('mObject = object_pointer;')


def generate_set_object_definition(inheritance_traits, out: FileGenerator, sharp_class):
    if isinstance(inheritance_traits, RequiresCastToBase):
        generate_requires_cast_to_base_set_object_definition(out, sharp_class)
    else:
        generate_simple_case_set_object_definition(out, sharp_class)


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
        return ' : base({base}.{expr}, null, false)'.format(base=base_class_name, expr=create_from_raw_ptr_expession)
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


def generate(cpp_file_cache: FileCache, capi_generator: CapiGenerator, namespace_generators: []):
    file_cache = SharpFileCache(cpp_file_cache)
    for namespace_generator in namespace_generators:
        namespace = SharpGenerator.get_or_gen_namespace(namespace_generator.full_wrap_name, namespace_generator)
        namespace.generate(file_cache, capi_generator)
    if capi_generator.params.generate_sharp_library:
        project_gen = SharpCmakeListGenerator(capi_generator, namespace_generators)
        project_gen.generate()
    full_name_2_sharp_object.clear()
