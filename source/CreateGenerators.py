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


from Parser import TClass, TEnumeration, TNamespace, TArgument, TBeautifulCapiRoot, TMappedType, TLifecycle
from Parser import TGenericDocumentation, TDocumentation, TReference, TExternalClass, TExternalNamespace
from ParamsParser import TBeautifulCapiParams
from TemplateGenerator import TemplateGenerator
from ClassGenerator import ClassGenerator
from MethodGenerator import MethodGenerator, FunctionGenerator, ConstructorGenerator
from ArgumentGenerator import *
from EnumGenerator import EnumGenerator
from DocumentationGenerator import ReferenceGenerator
from ExternalClassGenerator import ExternalClassGenerator
from ExternalNamespaceGenerator import ExternalNamespaceGenerator
from TemplateGenerator import TemplateConstantArgumentGenerator
from Helpers import BeautifulCapiException
from Helpers import get_template_arguments_count, get_template_argument, replace_template_argument


class GeneratorCreator(object):
    def __init__(self, params: TBeautifulCapiParams):
        self.full_name_2_type_generator = {}
        self.full_name_2_routine_generator = {}
        self.scope_2_mapped_types = {}  # NamespaceGenerator or ClassGenerator -> {str -> MappedTypeGenerator}
        self.scope_stack = []  # NamespaceGenerator or ClassGenerator
        self.cur_namespace_generator = None
        self.params = params
        self.cur_exception_code = 100000

    def __register_class_or_namespace_generator(self, generator):
        """
        :param generator: Class, Namespace, Enum, MappedType, ExternalClass or ExternalNamespace generators
        """
        self.full_name_2_type_generator.update({generator.full_name.replace(' ', ''): generator})
        if type(generator) is ClassGenerator and generator.class_object.typedef_name:
            # If the current generator class has typedef name and this class is not a lifecycle extension
            if not hasattr(generator.class_object, 'extension_base_class_name'):
                full_name = generator.parent_namespace.full_name + '::' + generator.class_object.typedef_name
                self.full_name_2_type_generator.update({full_name.replace(' ', ''): generator})

    def __create_enum_generator(self, cur_enum: TEnumeration, parent_generator) -> EnumGenerator:
        new_enum_generator = EnumGenerator(cur_enum, parent_generator)
        self.__register_class_or_namespace_generator(new_enum_generator)
        return new_enum_generator

    def __create_class_generator(self, cur_class: TClass) -> ClassGenerator:
        new_class_generator = ClassGenerator(cur_class, self.cur_namespace_generator, self.params)
        self.__register_class_or_namespace_generator(new_class_generator)
        for cur_mapped_type in cur_class.mapped_types:
            self.__create_mapped_type_generator(cur_mapped_type, new_class_generator)
        for cur_enum in cur_class.enumerations:
            new_enum_generator = self.__create_enum_generator(cur_enum, new_class_generator)
            new_class_generator.enum_generators.append(new_enum_generator)
        for constructor in cur_class.constructors:
            new_constructor_generator = ConstructorGenerator(constructor, new_class_generator, self.params)
            new_class_generator.constructor_generators.append(new_constructor_generator)
            self.full_name_2_routine_generator.update({new_constructor_generator.full_name: new_constructor_generator})
        for method in cur_class.methods:
            new_method_generator = MethodGenerator(method, new_class_generator, self.params)
            new_class_generator.method_generators.append(new_method_generator)
            self.full_name_2_routine_generator.update({new_method_generator.full_name: new_method_generator})
        return new_class_generator

    def __create_mapped_type_generator(self, cur_mapped_type: TMappedType, parent_generator):
        if parent_generator not in self.scope_2_mapped_types:
            self.scope_2_mapped_types[parent_generator] = {}
        new_mapped_type_generator = MappedTypeGenerator(cur_mapped_type, parent_generator)
        self.scope_2_mapped_types[parent_generator].update({cur_mapped_type.name: new_mapped_type_generator})

    def __create_external_class_generator(self, cur_class: TExternalClass, parent):
        new_class_generator = ExternalClassGenerator(cur_class, parent)
        self.__register_class_or_namespace_generator(new_class_generator)
        return new_class_generator

    def __create_external_namespace_generator(self, namespace: TExternalNamespace, parent):
        namespace_generator = ExternalNamespaceGenerator(namespace, parent)
        for cur_class in namespace.classes:
            namespace_generator.classes.append(self.__create_external_class_generator(cur_class, namespace_generator))
        for cur_namespace in namespace.namespaces:
            namespace_generator.nested_namespaces.append(
                self.__create_external_namespace_generator(cur_namespace, namespace_generator)
            )
        self.__register_class_or_namespace_generator(namespace_generator)
        return namespace_generator

    def create_namespace_generator(self, namespace: TNamespace) -> NamespaceGenerator:
        previous_namespace_generator = self.cur_namespace_generator
        new_namespace_generator = NamespaceGenerator(
            namespace, previous_namespace_generator, self.params)
        self.cur_namespace_generator = new_namespace_generator
        self.__register_class_or_namespace_generator(new_namespace_generator)
        for external_namespace in namespace.external_namespaces:
            new_namespace_generator.external_namespaces.append(
                self.__create_external_namespace_generator(external_namespace, None)
            )
        for nested_namespace in namespace.namespaces:
            new_namespace_generator.nested_namespaces.append(
                self.create_namespace_generator(nested_namespace))
        for cur_mapped_type in namespace.mapped_types:
            self.__create_mapped_type_generator(cur_mapped_type, new_namespace_generator)
        for cur_template in namespace.templates:
            new_namespace_generator.templates.append(
                TemplateGenerator(cur_template, new_namespace_generator, self.params))
        for cur_enum in namespace.enumerations:
            new_enum_generator = self.__create_enum_generator(cur_enum, new_namespace_generator)
            new_namespace_generator.enum_generators.append(new_enum_generator)
        for cur_class in namespace.classes:
            new_namespace_generator.classes.append(self.__create_class_generator(cur_class))
        for cur_function in namespace.functions:
            new_function_generator = FunctionGenerator(cur_function, new_namespace_generator, self.params)
            new_namespace_generator.functions.append(new_function_generator)
            self.full_name_2_routine_generator.update({new_function_generator.full_name: new_function_generator})
        self.cur_namespace_generator = previous_namespace_generator
        return new_namespace_generator

    def __apply_semantic_operator(self, type_name: str, operator_name: str, semantic_type: TLifecycle) -> str:
        begin_operator_str = operator_name + '('
        found_start_index = type_name.rfind(begin_operator_str)
        while found_start_index != -1:
            found_end_index = type_name.find(')', found_start_index)
            argument_type = type_name[found_start_index + len(begin_operator_str):found_end_index]
            result_type = ''
            if argument_type in self.full_name_2_type_generator:
                class_generator = self.full_name_2_type_generator[argument_type]
                if type(class_generator) is ClassGenerator:
                    for lifecycle_extension in class_generator.class_object.lifecycle_extensions:
                        if lifecycle_extension.lifecycle == semantic_type:
                            result_type = class_generator.parent_namespace.full_name + '::' + lifecycle_extension.name
                            result_type = result_type.replace(' ', '')
                            break
            if not result_type:
                is_pointer = argument_type[-1] == '*'
                if semantic_type == TLifecycle.copy_semantic:
                    if is_pointer:
                        result_type = argument_type[:-1]
                    else:
                        result_type = argument_type
                else:
                    if not is_pointer:
                        result_type = argument_type + '*'
                    else:
                        result_type = argument_type
            begin_str = type_name[:found_start_index]
            end_str = type_name[found_end_index + 1:]
            type_name = begin_str + result_type + end_str
            found_start_index = type_name.rfind(begin_operator_str)
        return type_name

    def __apply_semantic_operators(self, type_name: str) -> str:
        type_name = self.__apply_semantic_operator(
            type_name, 'raw_pointer_semantic_extension', TLifecycle.raw_pointer_semantic)
        type_name = self.__apply_semantic_operator(
            type_name, 'reference_counted_semantic_extension', TLifecycle.reference_counted)
        type_name = self.__apply_semantic_operator(
            type_name, 'copy_semantic_extension', TLifecycle.copy_semantic)
        return type_name

    def __create_type_generator(self, type_name: str, is_builtin: bool) -> BaseTypeGenerator:
        name = type_name.replace(' ', '')
        name = self.__apply_semantic_operators(name)
        type_name = self.__apply_semantic_operators(type_name)
        if name in self.full_name_2_type_generator:
            type_generator = self.full_name_2_type_generator[name]
            if type(type_generator) is ClassGenerator:
                return ClassTypeGenerator(type_generator)
            elif type(type_generator) is EnumGenerator:
                return EnumTypeGenerator(type_generator)
            elif type(type_generator) is ExternalClassGenerator:
                return ExternalClassTypeGenerator(type_generator)
            else:
                raise BeautifulCapiException('namespace is used as type name')
        else:
            for cur_scope in reversed(self.scope_stack):
                if cur_scope in self.scope_2_mapped_types:
                    if type_name in self.scope_2_mapped_types[cur_scope]:
                        return self.scope_2_mapped_types[cur_scope][type_name]
            if self.params.warn_when_builtin_type_used and type_name and not is_builtin:
                print('Warning: Builtin type "{name}" used, use type maps for overriding them.'.format(name=type_name))
            return BuiltinTypeGenerator(type_name)

    def __get_generator(self, type_name: str) -> object:
        type_name_without_spaces = type_name.replace(' ', '')
        if type_name_without_spaces in self.full_name_2_routine_generator:
            return self.full_name_2_routine_generator[type_name_without_spaces]
        elif type_name_without_spaces in self.full_name_2_type_generator:
            return self.full_name_2_type_generator[type_name_without_spaces]
        raise BeautifulCapiException('reference could not be bound')

    def __bind_documentation_references_impl(self, documentation: TGenericDocumentation):
        for i, doc_item in enumerate(documentation.all_items):
            if type(doc_item) is TReference:
                reference_as_text = ''.join(doc_item.all_items)
                new_reference_to_replace = ReferenceGenerator()
                new_reference_to_replace.referenced_generator = self.__get_generator(reference_as_text)
                documentation.all_items[i] = new_reference_to_replace
            elif type(doc_item) is TGenericDocumentation:
                self.__bind_documentation_references(doc_item)

    def __bind_documentation_references(self, documentation):
        if issubclass(type(documentation), TDocumentation):
            for brief in documentation.briefs:
                self.__bind_documentation_references_impl(brief)
            for doc_return in documentation.returns:
                self.__bind_documentation_references_impl(doc_return)
        self.__bind_documentation_references_impl(documentation)

    def __bind_documentation(self, some_object):
        for documentation in some_object.documentations:
            self.__bind_documentation_references(documentation)

    def __create_argument_generator(self, argument: TArgument) -> ArgumentGenerator:
        new_argument_generator = ArgumentGenerator(
            self.__create_type_generator(argument.type_name, argument.is_builtin), argument.name)
        new_argument_generator.argument_object = argument
        self.__bind_documentation(new_argument_generator.argument_object)
        return new_argument_generator

    def __bind_constructor(self, constructor_generator: ConstructorGenerator):
        for argument in constructor_generator.constructor_object.arguments:
            constructor_generator.argument_generators.append(self.__create_argument_generator(argument))
        self.__bind_documentation(constructor_generator.constructor_object)

    def __bind_method(self, method_generator: MethodGenerator):
        for argument in method_generator.method_object.arguments:
            method_generator.argument_generators.append(self.__create_argument_generator(argument))
        method_generator.return_type_generator = self.__create_type_generator(
            method_generator.method_object.return_type,
            method_generator.method_object.return_is_builtin)
        method_generator.return_type_generator.impl_2_c = method_generator.method_object.impl_2_c
        method_generator.return_type_generator.impl_2_c_filled = method_generator.method_object.impl_2_c_filled
        self.__bind_documentation(method_generator.method_object)

    def __bind_function(self, function_generator: FunctionGenerator):
        for argument in function_generator.function_object.arguments:
            function_generator.argument_generators.append(self.__create_argument_generator(argument))
        function_generator.return_type_generator = self.__create_type_generator(
            function_generator.function_object.return_type,
            function_generator.function_object.return_is_builtin)
        function_generator.return_type_generator.impl_2_c = function_generator.function_object.impl_2_c
        function_generator.return_type_generator.impl_2_c_filled = function_generator.function_object.impl_2_c_filled
        self.__bind_documentation(function_generator.function_object)

    def __replace_template_implementation_class_plain(self, implementation_class_name: str):
        template_arguments_count = get_template_arguments_count(implementation_class_name)
        for index in range(template_arguments_count):
            original_template_argument = get_template_argument(implementation_class_name, index)
            original_template_argument_for_search = original_template_argument.replace(' ', '')
            if original_template_argument_for_search in self.full_name_2_type_generator:
                argument_generator = self.full_name_2_type_generator[original_template_argument_for_search]
                if type(argument_generator) is ClassGenerator:
                    self.__replace_template_implementation_class(argument_generator)
                implementation_class_name = replace_template_argument(
                    implementation_class_name,
                    index,
                    argument_generator.implementation_name
                )
            else:
                new_template_argument = self.__replace_template_implementation_class_plain(original_template_argument)
                implementation_class_name = replace_template_argument(
                    implementation_class_name,
                    index,
                    new_template_argument
                )
        return implementation_class_name

    def __replace_template_implementation_class(self, class_generator):
        class_generator.class_object.implementation_class_name = self.__replace_template_implementation_class_plain(
            class_generator.class_object.implementation_class_name
        )

    def __bind_class(self, class_generator: ClassGenerator):
        def name_to_class_generator(class_name: str, exception_class_type: str):
            class_name = class_name.replace(' ', '')
            class_name = self.__apply_semantic_operators(class_name)
            if class_name not in self.full_name_2_type_generator:
                raise BeautifulCapiException('{0} class {1} is not found'.format(exception_class_type, class_name))
            return self.full_name_2_type_generator[class_name]

        self.scope_stack.append(class_generator)
        if class_generator.class_object.base:
            class_generator.base_class_generator = name_to_class_generator(class_generator.class_object.base, 'base')
            class_generator.base_class_generator.derived_class_generators.append(class_generator)
        if class_generator.class_object.exception:
            if class_generator.class_object.exception_code_filled:
                class_generator.exception_code = class_generator.class_object.exception_code
            else:
                class_generator.exception_code = self.cur_exception_code
                self.cur_exception_code += 1
        template_arguments_count = get_template_arguments_count(class_generator.name)
        for index in range(template_arguments_count):
            template_argument = get_template_argument(class_generator.name, index)
            template_argument_type = class_generator.class_object.template_arguments[index].template_argument_type
            if template_argument_type not in ['class', 'typename']:
                template_argument_generator = TemplateConstantArgumentGenerator(template_argument)
            else:
                template_argument_generator = self.__create_type_generator(template_argument, False)
            class_generator.template_argument_generators.append(template_argument_generator)
        for constructor_generator in class_generator.constructor_generators:
            self.__bind_constructor(constructor_generator)
        for method_generator in class_generator.method_generators:
            self.__bind_method(method_generator)
        self.__bind_documentation(class_generator.class_object)
        for enum_generator in class_generator.enum_generators:
            self.__bind_documentation(enum_generator.enum_object)
            for item in enum_generator.enum_object.items:
                self.__bind_documentation(item)
        if hasattr(class_generator.class_object, 'extension_base_class_name'):
            class_generator.extension_base_class_generator = \
                name_to_class_generator(class_generator.class_object.extension_base_class_name, 'extension')
        if hasattr(class_generator.class_object, 'lifecycle_extension'):
            for index, cast_to in enumerate(class_generator.class_object.lifecycle_extension.cast_tos):
                result_cast_to = class_generator.class_object.lifecycle_extension.cast_tos[index]
                result_cast_to.target_generator = name_to_class_generator(cast_to.target_type, 'target')
            for index, cast_from in enumerate(class_generator.class_object.lifecycle_extension.cast_froms):
                result_cast_from = class_generator.class_object.lifecycle_extension.cast_froms[index]
                result_cast_from.source_generator = name_to_class_generator(cast_from.source_type, 'source')
            if class_generator.base_class_generator:
                base = class_generator.base_class_generator.class_object
                class_lifecycle = class_generator.class_object.lifecycle
                lifecycle_extensions = [ext for ext in base.lifecycle_extensions if class_lifecycle == ext.lifecycle]
                if base and lifecycle_extensions:
                    extension_name = "{namespace}::{base_class}".format(
                        namespace=class_generator.base_class_generator.parent_namespace.full_name,
                        base_class=lifecycle_extensions[0].name
                    )
                    class_generator.class_object.base = extension_name
        self.__replace_template_implementation_class(class_generator)
        self.scope_stack.pop()

    def __bind_namespace(self, namespace_generator: NamespaceGenerator):
        self.scope_stack.append(namespace_generator)
        for nested_namespace_generator in namespace_generator.nested_namespaces:
            self.__bind_namespace(nested_namespace_generator)
        for class_generator in namespace_generator.classes:
            self.__bind_class(class_generator)
        for function_generator in namespace_generator.functions:
            self.__bind_function(function_generator)
        for enum_generator in namespace_generator.enum_generators:
            self.__bind_documentation(enum_generator.enum_object)
            for item in enum_generator.enum_object.items:
                self.__bind_documentation(item)
        self.__bind_documentation(namespace_generator.namespace_object)
        self.scope_stack.pop()

    def bind_namespaces(self, namespace_generators: [NamespaceGenerator]):
        for namespace_generator in namespace_generators:
            self.__bind_namespace(namespace_generator)


def create_namespace_generators(root_node: TBeautifulCapiRoot,
                                params: TBeautifulCapiParams) -> [NamespaceGenerator]:
    generator_creator = GeneratorCreator(params)
    created_namespace_generators = []
    for cur_namespace in root_node.namespaces:
        created_namespace_generators.append(generator_creator.create_namespace_generator(cur_namespace))
    generator_creator.bind_namespaces(created_namespace_generators)
    return created_namespace_generators
