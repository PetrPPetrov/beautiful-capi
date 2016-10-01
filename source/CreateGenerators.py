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


from Parser import TClass, TEnumeration, TNamespace, TArgument, TBeautifulCapiRoot
from ParamsParser import TBeautifulCapiParams
from NamespaceGenerator import NamespaceGenerator
from ClassGenerator import ClassGenerator
from MethodGenerator import MethodGenerator, FunctionGenerator, ConstructorGenerator
from ArgumentGenerator import ClassTypeGenerator, BuiltinTypeGenerator, EnumTypeGenerator, ArgumentGenerator
from EnumGenerator import EnumGenerator
from Helpers import BeautifulCapiException


class GeneratorCreator(object):
    def __init__(self, params: TBeautifulCapiParams):
        self.full_name_2_generator = {}
        self.cur_namespace_generator = None
        self.params = params
        self.cur_exception_code = 1

    def __register_class_or_namespace_generator(
            self, generator: ClassGenerator or NamespaceGenerator or EnumGenerator):
        self.full_name_2_generator.update({generator.full_name.replace(' ', ''): generator})

    def __create_enum_generator(self, cur_enum: TEnumeration, parent_generator) -> EnumGenerator:
        new_enum_generator = EnumGenerator(cur_enum, parent_generator)
        self.__register_class_or_namespace_generator(new_enum_generator)
        return new_enum_generator

    def __create_class_generator(self, cur_class: TClass) -> ClassGenerator:
        new_class_generator = ClassGenerator(cur_class, self.cur_namespace_generator, self.params)
        self.__register_class_or_namespace_generator(new_class_generator)
        for cur_enum in cur_class.enumerations:
            new_enum_generator = self.__create_enum_generator(cur_enum, new_class_generator)
            new_class_generator.enum_generators.append(new_enum_generator)
        for constructor in cur_class.constructors:
            new_constructor_generator = ConstructorGenerator(constructor, new_class_generator, self.params)
            new_class_generator.constructor_generators.append(new_constructor_generator)
        for method in cur_class.methods:
            new_method_generator = MethodGenerator(method, new_class_generator, self.params)
            new_class_generator.method_generators.append(new_method_generator)
        return new_class_generator

    def create_namespace_generator(self, namespace: TNamespace) -> NamespaceGenerator:
        previous_namespace_generator = self.cur_namespace_generator
        new_namespace_generator = NamespaceGenerator(
            namespace, previous_namespace_generator, self.params)
        self.cur_namespace_generator = new_namespace_generator
        self.__register_class_or_namespace_generator(new_namespace_generator)
        for nested_namespace in namespace.namespaces:
            new_namespace_generator.nested_namespaces.append(
                self.create_namespace_generator(nested_namespace))
        for cur_enum in namespace.enumerations:
            new_enum_generator = self.__create_enum_generator(cur_enum, new_namespace_generator)
            new_namespace_generator.enum_generators.append(new_enum_generator)
        for cur_class in namespace.classes:
            new_namespace_generator.classes.append(self.__create_class_generator(cur_class))
        for cur_function in namespace.functions:
            new_namespace_generator.functions.append(
                FunctionGenerator(cur_function, new_namespace_generator, self.params))
        self.cur_namespace_generator = previous_namespace_generator
        return new_namespace_generator

    def __create_type_generator(
            self, type_name: str) -> ClassTypeGenerator or EnumTypeGenerator or BuiltinTypeGenerator:
        if type_name.replace(' ', '') in self.full_name_2_generator:
            type_generator = self.full_name_2_generator[type_name.replace(' ', '')]
            if type(type_generator) is ClassGenerator:
                return ClassTypeGenerator(type_generator)
            elif type(type_generator) is EnumGenerator:
                return EnumTypeGenerator(type_generator)
            else:
                raise BeautifulCapiException('namespace is used as type name')
        else:
            return BuiltinTypeGenerator(type_name)

    def __create_argument_generator(self, argument: TArgument) -> ArgumentGenerator:
        return ArgumentGenerator(self.__create_type_generator(argument.type_name), argument.name)

    def __bind_constructor(self, constructor_generator: ConstructorGenerator):
        for argument in constructor_generator.constructor_object.arguments:
            constructor_generator.argument_generators.append(self.__create_argument_generator(argument))

    def __bind_method(self, method_generator: MethodGenerator):
        for argument in method_generator.method_object.arguments:
            method_generator.argument_generators.append(self.__create_argument_generator(argument))
        method_generator.return_type_generator = self.__create_type_generator(
            method_generator.method_object.return_type)

    def __bind_function(self, function_generator: FunctionGenerator):
        for argument in function_generator.function_object.arguments:
            function_generator.argument_generators.append(self.__create_argument_generator(argument))
        function_generator.return_type_generator = self.__create_type_generator(
            function_generator.function_object.return_type)

    def __bind_class(self, class_generator: ClassGenerator):
        if class_generator.class_object.base:
            base_class_str = class_generator.class_object.base.replace(' ', '')
            if base_class_str not in self.full_name_2_generator:
                raise BeautifulCapiException(
                    'base class {0} is not found'.format(class_generator.class_object.base))
            class_generator.base_class_generator = self.full_name_2_generator[base_class_str]
            class_generator.base_class_generator.derived_class_generators.append(class_generator)
        if class_generator.class_object.exception:
            class_generator.exception_code = self.cur_exception_code
            self.cur_exception_code += 1
        for constructor_generator in class_generator.constructor_generators:
            self.__bind_constructor(constructor_generator)
        for method_generator in class_generator.method_generators:
            self.__bind_method(method_generator)

    def __bind_namespace(self, namespace_generator: NamespaceGenerator):
        for nested_namespace_generator in namespace_generator.nested_namespaces:
            self.__bind_namespace(nested_namespace_generator)
        for class_generator in namespace_generator.classes:
            self.__bind_class(class_generator)
        for function_generator in namespace_generator.functions:
            self.__bind_function(function_generator)

    def bind_namespaces(self, namespace_generators: [NamespaceGenerator]):
        for namespace_generator in namespace_generators:
            self.__bind_namespace(namespace_generator)


def create_namespace_generators(root_node: TBeautifulCapiRoot,
                                params: TBeautifulCapiParams) -> [NamespaceGenerator]:
    generator_creator = GeneratorCreator(params)
    created_namespace_generators = []
    for cur_namespace in root_node.namespaces:
        created_namespace_generators.append(
            generator_creator.create_namespace_generator(cur_namespace))
    generator_creator.bind_namespaces(created_namespace_generators)
    return created_namespace_generators
