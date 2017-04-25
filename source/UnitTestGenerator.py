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


import random
import os
import string
from collections import OrderedDict

import ParamsParser
import NamespaceGenerator
import Parser
from ArgumentGenerator import MappedTypeGenerator, EnumTypeGenerator
from BuiltinTypeGenerator import BuiltinTypeGenerator
from ClassGenerator import ClassTypeGenerator as CClassTypeGenerator, ClassGenerator
from FileGenerator import FileGenerator, IndentScope, WatchdogScope
from Helpers import format_type
from MethodGenerator import MethodGenerator
from Helpers import pascal_to_stl


class ClassToProperties(object):
    class Properties(object):
        def __init__(self, c_property, set_method, get_method):
            self.property = c_property
            self.set_method = set_method
            self.get_method = get_method
            self.set_method_generator = None
            self.get_method_generator = None

    class CGeneratorToProperties(object):
        def __init__(self):
            self.class_generator = None
            self.properties = []

        def add_property(self, c_property, set_method: Parser.TMethod, get_method: Parser.TMethod):
            self.properties.append(ClassToProperties.Properties(c_property, set_method, get_method))

    def __init__(self):
        self.map = {}

    def __add_object(self, cur_class: Parser.TClass):
        if cur_class not in self.map:
            self.map[cur_class] = self.CGeneratorToProperties()
        return self.map[cur_class]

    def add_property(self, cur_class: Parser.TClass, c_property: Properties,
                     set_method: Parser.TMethod, get_method: Parser.TMethod):
        cur_dict_object = self.__add_object(cur_class)
        cur_dict_object.add_property(c_property, set_method, get_method)


class RandomValue(object):
    def __init__(self):
        pass

    @staticmethod
    def __random_simple_types(type_name: str) -> str or float or int:
        type_name = type_name.strip().lower()
        if type_name == 'const char*':
            len_for_string = random.randint(1, 255)
            ss = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(len_for_string))
            return '"{0}"'.format(ss)
        elif type_name in ['char', 'signed char']:
            return random.randint(-128, 127)
        elif type_name == 'unsigned char':
            return random.randint(0, 255)
        elif type_name in ['short int', 'signed short int']:
            return random.randint(-32768, 32767)
        elif type_name in ['unsigned short int', 'unsigned short']:
            return random.randint(0, 65535)
        elif type_name in ['int', 'long int', 'signed int', 'signed long int']:
            return random.randint(-2147483647, 2147483647)
        elif type_name in ['size_t', 'unsigned int', 'unsigned long int', 'unsigned']:
            return random.randint(0, 2147483647)
        elif type_name in ['float']:
            return round(random.uniform(0, 1), 7)
        elif type_name in ['double', 'long double']:
            return round(random.uniform(0, 1), 15)
        elif type_name == 'bool':
            return random.choice(['true', 'false'])
        else:
            raise Exception('Unknown type {type_name}'.format(type_name=type_name))

    def generate(self, type_name: str) -> str:
        return str(self.__random_simple_types(type_name))


class TestGenerator(object):
    class OutputGenerators(object):
        def __init__(self, output_file_name: str=None):
            self.main_generator = FileGenerator(output_file_name)
            self.declaration_section = FileGenerator(None)

    def __init__(self, params: ParamsParser.TBeautifulCapiParams, output_file_name: str):
        self.class_to_properties = ClassToProperties()
        self.types_for_random = set()
        self.params = params
        self.test_generator = TestGenerator.OutputGenerators(output_file_name)
        self.equal_generator = TestGenerator.OutputGenerators(None)

    def add_property(self, cur_class: Parser.TClass, c_property: ClassToProperties.Properties,
                     set_method: Parser.TMethod, get_method: Parser.TMethod):
        self.class_to_properties.add_property(cur_class, c_property, set_method, get_method)

    def __prepare_for_class(self, class_generator: ClassGenerator):
        if class_generator.class_object not in self.class_to_properties.map:
            return

        c_generator_to_properties = self.class_to_properties.map.get(class_generator.class_object, None)
        c_generator_to_properties.class_generator = class_generator
        for c_property in c_generator_to_properties.properties:
            c_property.set_method_generator = None
            c_property.get_method_generator = None

            for method in class_generator.method_generators:
                if method.method_object == c_property.set_method:
                    c_property.set_method_generator = method
                if method.method_object == c_property.get_method:
                    c_property.get_method_generator = method

            for argument in c_property.set_method_generator.argument_generators:
                self.types_for_random.add(argument.argument_object.type_name)

    def __processing_namespace(self, namespace_generators: [NamespaceGenerator.NamespaceGenerator]):
        for namespace_generator in namespace_generators:
            for class_generator in namespace_generator.classes:
                self.__prepare_for_class(class_generator)
            self.__processing_namespace(namespace_generator.nested_namespaces)

    def __gen_test_for_simple_value(self, c_property: ClassToProperties.Properties, value: str):
        self.test_generator.main_generator.put_line('test_class{sep}{method_name}({value});'.format(
            method_name=c_property.set_method.name, value=value, sep=c_property.set_method_generator.access_operator))
        check_str = 'BOOST_CHECK_EQUAL(test_class{sep}{method_name}(), {value});'.format(
            method_name=c_property.get_method.name, value=value, sep=c_property.get_method_generator.access_operator)
        self.test_generator.main_generator.put_line(check_str)

    @staticmethod
    def __gen_init_enum_type(enum_type_generator: EnumTypeGenerator) -> str:
        enum_generator = enum_type_generator.enum_argument_generator
        enum_items = enum_generator.enum_object.items
        rand_enum_value = enum_items[random.randint(0, len(enum_items) - 1)]
        value = '{name}::{value}'.format(
            name=enum_generator.parent_generator.full_wrap_name, value=rand_enum_value.name)
        return value

    @staticmethod
    def __get__enum_items(enum_type_generator: EnumTypeGenerator) -> [str]:
        result = list()
        enum_generator = enum_type_generator.enum_argument_generator
        enum_items = enum_generator.enum_object.items
        for enum_value in enum_items:
            value = '{name}::{value}'.format(
                name=enum_generator.parent_generator.full_wrap_name, value=enum_value.name)
            result.append(value)
        return result

    def __gen_code_for_test_enum(self, c_property: ClassToProperties.Properties):
        enum_type_generator = c_property.get_method_generator.return_type_generator
        all_items = self.__get__enum_items(enum_type_generator)
        for item in all_items:
            self.__gen_test_for_simple_value(c_property, item)

    def __gen_code_for_test_builtin_type(self, c_property: ClassToProperties.Properties):
        random_value = RandomValue().generate(c_property.get_method.return_type)
        self.__gen_test_for_simple_value(c_property, random_value)

    def __gen_for_object(self, argument_generator: ClassGenerator, c_property: ClassToProperties.Properties):
        field_name = pascal_to_stl(c_property.property.name)
        self.__gen_code_for_missing_arguments(argument_generator.class_object, argument_generator, field_name)

    def __gen_test_for_copy_semantic(self, argument_generator: ClassGenerator,
                                     c_property: ClassToProperties.Properties):
        # For Example:
        # test_class.SetMethodName(field_name);
        # BOOST_CHECK(equal(test_class.GetMethodName(), field_name));
        field_name = pascal_to_stl(c_property.property.name)
        self.__gen_for_object(argument_generator, c_property)

        self.test_generator.main_generator.put_line('test_class{sep}{method_name}({field_name});'.format(
            method_name=c_property.set_method.name, sep=c_property.set_method_generator.access_operator,
            field_name=field_name))
        check_str = 'BOOST_CHECK(equal(test_class{sep}{method_name}(), {field_name}));'.format(
            method_name=c_property.get_method.name, sep=c_property.get_method_generator.access_operator,
            field_name=field_name)
        self.test_generator.main_generator.put_line(check_str)

    def __gen_test_for_refcounted_semantic(self, argument_generator: ClassGenerator,
                                           c_property: ClassToProperties.Properties):
        # For Example:
        # test_class->SetMethodName(field_name);
        # BOOST_CHECK_EQUAL(test_class->getMethodName().GetRawPointer(), field_name.GetRawPointer());
        field_name = pascal_to_stl(c_property.property.name)

        self.__gen_for_object(argument_generator, c_property)
        self.test_generator.main_generator.put_line('test_class{sep}{method_name}({field_name});'.format(
            method_name=c_property.set_method.name, sep=c_property.set_method_generator.access_operator,
            field_name=field_name))
        check_str = 'BOOST_CHECK_EQUAL(test_class{sep}{method_name}().{raw_name}(), {field_name}.{raw_name}());'.format(
            method_name=c_property.get_method.name, sep=c_property.get_method_generator.access_operator,
            field_name=field_name, raw_name=argument_generator.params.get_raw_pointer_method_name)
        self.test_generator.main_generator.put_line(check_str)

    def __gen_test_for_rawpointer_semantic(self, argument_generator: ClassGenerator,
                                           c_property: ClassToProperties.Properties):
        field_name = pascal_to_stl(c_property.property.name)

        self.__gen_test_for_refcounted_semantic(argument_generator, c_property)
        self.test_generator.main_generator.put_line('{name}.{del_method_name}();'.format(
            name=field_name,  del_method_name=self.params.delete_method_name))

    def __gen_code_for_test_class(self, c_property: ClassToProperties.Properties):
        return_type_generator = c_property.get_method_generator.return_type_generator
        argument_generator = return_type_generator.class_argument_generator

        lifecycle_traits = argument_generator.class_object.lifecycle
        if lifecycle_traits == Parser.TLifecycle.reference_counted:
            self.__gen_test_for_refcounted_semantic(argument_generator, c_property)
        elif lifecycle_traits == Parser.TLifecycle.raw_pointer_semantic:
            self.__gen_test_for_rawpointer_semantic(argument_generator, c_property)
        elif lifecycle_traits == Parser.TLifecycle.copy_semantic:
            self.__gen_test_for_copy_semantic(argument_generator, c_property)
        else:
            raise Exception('Unknown LifeCycleTraits')

    @staticmethod
    def __get_arguments_as_param(method_generator: MethodGenerator) -> str:
        result = []
        for argument in method_generator.argument_generators:
            result.append(argument.name)
        return ', '.join(result)

    def __get_first_instanceable_class(self, class_argument_generator: ClassGenerator):
        value = class_argument_generator.derived_class_generators[0]
        return self.__get_first_instanceable_class(value) if value.class_object.abstract else value

    def __get_arguments(self, class_generator: ClassGenerator) -> list:
        result = list()
        if not class_generator.constructor_generators:
            return result

        generator = class_generator.constructor_generators[0]
        for argument in generator.argument_generators:
            type_generator = argument.type_generator

            if type(type_generator) in [BuiltinTypeGenerator, EnumTypeGenerator]:
                if type(type_generator) is EnumTypeGenerator:
                    value = self.__gen_init_enum_type(type_generator)
                else:
                    value = RandomValue().generate(type_generator.type_name)

                result.append('{full_type} {name} = {value};'.format(
                    full_type=format_type(type_generator.type_name), name=argument.name, value=value))
            elif type(type_generator) is CClassTypeGenerator:
                base_class = argument.type_generator.class_argument_generator
                base_full_type = base_class.full_wrap_name

                first_instanceable_class = base_class
                instanceable_full_type = base_full_type

                if type_generator.class_argument_generator.class_object.abstract:
                    first_instanceable_class = self.__get_first_instanceable_class(type_generator.class_argument_generator)
                    instanceable_full_type = format_type(first_instanceable_class.full_wrap_name)

                args = ''
                if not self.has_default_constructor(first_instanceable_class):
                    result += self.__get_arguments(first_instanceable_class)
                    args = self.__get_arguments_as_param(first_instanceable_class.constructor_generators[0])

                result.append('{full_type} {name} = {derived_type}({args});'.format(
                    full_type=format_type(base_full_type),
                    name=argument.name,
                    derived_type=instanceable_full_type,
                    args=args))
        return result

    def __gen_code_for_missing_arguments(self, class_object: Parser.TClass, class_generator: ClassGenerator,
                                         argument_name: str):

        def processing_constructor(c_generator: ClassGenerator, instanceable_class_generator: ClassGenerator):
            # int b = 10;
            # float c = 5.0;
            # BaseType a = InstanceableType(b, c);

            base_type = format_type(c_generator.full_wrap_name)
            derived_type = format_type(instanceable_class_generator.full_wrap_name)

            arguments = ''
            line = '{base} {name} = {derived}({args});'

            if not self.has_default_constructor(instanceable_class_generator):
                out_lines = self.__get_arguments(instanceable_class_generator)
                arguments = self.__get_arguments_as_param(c_generator.constructor_generators[0])
                out_lines.append(line.format(
                    base=derived_type, derived=derived_type, name=argument_name, args=arguments))
                self.test_generator.main_generator.put_lines(out_lines)
            else:
                self.test_generator.main_generator.put_line(line.format(
                    base=base_type, derived=derived_type, name=argument_name, args=arguments))

        first_instanceable_class = class_generator
        if class_object.abstract:
            self.test_generator.main_generator.put_line('// Use instanceable class')
            first_instanceable_class = self.__get_first_instanceable_class(class_generator)
        processing_constructor(class_generator, first_instanceable_class)

    @staticmethod
    def has_default_constructor(class_generator: ClassGenerator):
        if not class_generator.constructor_generators:
            return True
        has_constructor = any(filter(lambda ctor: not ctor.argument_generators, class_generator.constructor_generators))
        return has_constructor

    def generate_test(self, cur_class: Parser.TClass,
                      c_generator_to_properties: ClassToProperties.CGeneratorToProperties):
        full_type = format_type(c_generator_to_properties.class_generator.full_wrap_name)
        full_c_type = format_type(c_generator_to_properties.class_generator.full_c_name)
        test_declaration = 'BOOST_AUTO_TEST_CASE({0}_test)'.format(full_c_type.replace('::', '_').lower())

        is_copy_semantic = cur_class.lifecycle == Parser.TLifecycle.copy_semantic
        is_raw_pointer = cur_class.lifecycle == Parser.TLifecycle.raw_pointer_semantic
        if is_copy_semantic:
            self.__gen_code_equal_method(c_generator_to_properties, full_type)

        self.test_generator.main_generator.put_line(test_declaration)
        with IndentScope(self.test_generator.main_generator, ending='}\n'):
            self.__gen_code_for_missing_arguments(cur_class, c_generator_to_properties.class_generator, 'test_class')
            for c_property in c_generator_to_properties.properties:
                with IndentScope(self.test_generator.main_generator):
                    return_type_generator = c_property.get_method_generator.return_type_generator
                    if type(return_type_generator) is BuiltinTypeGenerator:
                        self.__gen_code_for_test_builtin_type(c_property)
                    elif type(return_type_generator) is EnumTypeGenerator:
                        self.__gen_code_for_test_enum(c_property)
                    elif type(return_type_generator) is CClassTypeGenerator:
                        self.__gen_code_for_test_class(c_property)
            if is_raw_pointer:
                self.test_generator.main_generator.put_line('test_class.{del_method_name}();'.format(
                    del_method_name=self.params.delete_method_name))

    def __gen_code_equal_method(self, c_generator_to_properties: ClassToProperties.CGeneratorToProperties,
                                full_type: str):
        method_declaration = 'inline bool equal(const {type_name}& first, const {type_name}& second){is_declaration}'
        self.equal_generator.declaration_section.put_line(method_declaration.format(
            type_name=full_type, is_declaration=';'))
        self.equal_generator.main_generator.put_line(method_declaration.format(
            type_name=full_type, is_declaration=''))

        with IndentScope(self.equal_generator.main_generator, ending='}\n'):
            generator = self.equal_generator.main_generator
            for c_property in c_generator_to_properties.properties:
                equal_code = 'if ({equal_method}first.{method_name}(){raw_method}{action}' \
                             'second.{method_name}(){raw_method}{close_br})'
                property_type = c_property.get_method_generator.return_type_generator
                typeof_property_type = type(property_type)

                need_raw_pointer = False
                need_equal_method = (False, '')
                if typeof_property_type in [MappedTypeGenerator, BuiltinTypeGenerator, EnumTypeGenerator]:
                    need_equal_method = (True, 'builtin_equal')
                elif typeof_property_type is CClassTypeGenerator:
                    lifecycle_property_type = property_type.class_argument_generator.class_object.lifecycle
                    if lifecycle_property_type in [Parser.TLifecycle.reference_counted,
                                                   Parser.TLifecycle.raw_pointer_semantic]:
                        need_raw_pointer = True
                    elif lifecycle_property_type == Parser.TLifecycle.copy_semantic:
                        need_equal_method = (True, 'equal')
                    else:
                        raise Exception('Unknown LifeCycle type')
                else:
                    raise Exception('Unknown TypeGenerator')
                raw_method_name = c_generator_to_properties.class_generator.params.get_raw_pointer_method_name
                equal_code = equal_code.format(
                    method_name=c_property.get_method.name,
                    raw_method='.{0}()'.format(raw_method_name) if need_raw_pointer else '',
                    equal_method='!{0}('.format(need_equal_method[1]) if need_equal_method[0] else '',
                    close_br=')' if need_equal_method[0] else '',
                    action=', ' if need_equal_method[0] else ' != ')
                generator.put_line(equal_code)
                with IndentScope(generator):
                    generator.put_line('return false;')
            generator.put_line('return true;')

    def __generate_test(self, namespace_generators: [NamespaceGenerator.NamespaceGenerator]):
        added_namespace = list()
        for namespace_generator in namespace_generators:
            self.test_generator.main_generator.put_file(self.test_generator.declaration_section)
            for class_generator in namespace_generator.classes:
                if class_generator.class_object in self.class_to_properties.map:
                    if namespace_generator not in added_namespace:
                        added_namespace.append(namespace_generator)
                        self.test_generator.main_generator.put_line('BOOST_AUTO_TEST_SUITE({0})\n'.format(
                            pascal_to_stl(namespace_generator.namespace_object.name)))
                    class_object = class_generator.class_object
                    c_generator_to_properties = self.class_to_properties.map[class_object]
                    self.generate_test(class_object, c_generator_to_properties)
            self.__generate_test(namespace_generator.nested_namespaces)
            if namespace_generator in added_namespace:
                self.test_generator.main_generator.put_line('BOOST_AUTO_TEST_SUITE_END()\n')

    def generate_tests(self, namespace_generators: [NamespaceGenerator.NamespaceGenerator]):
        if os.path.splitext(self.test_generator.main_generator.filename)[1].lower() != '.h':
            self.test_generator.main_generator.put_line('# define BOOST_TEST_MAIN')
        self.test_generator.main_generator.include_header('boost/test/unit_test.hpp', False)
        self.test_generator.main_generator.include_header('StaticEqual.h', False)

        root_namespaces = [namespace_generator.full_wrap_name for namespace_generator in namespace_generators]
        for namespace in root_namespaces:
            self.test_generator.main_generator.include_header('{0}.h'.format(namespace), False)

        self.test_generator.main_generator.put_begin_cpp_comments(self.params)
        self.test_generator.main_generator.put_include_files()
        self.test_generator.main_generator.put_file(self.equal_generator.declaration_section)
        self.test_generator.main_generator.put_line('')
        self.test_generator.main_generator.put_file(self.equal_generator.main_generator)
        self.test_generator.main_generator.put_line('')

        self.__generate_test(namespace_generators)

    def generate(self, namespace_generators: [NamespaceGenerator.NamespaceGenerator]):
        self.__processing_namespace(namespace_generators)

        d_sorted_by_value = OrderedDict(sorted(self.class_to_properties.map.items(), key=lambda x: x[0].name))
        self.class_to_properties.map = d_sorted_by_value

        if os.path.splitext(self.test_generator.main_generator.filename)[1].lower() == '.h':
            root_namespaces = [generator.full_wrap_name.upper() for generator in namespace_generators]
            with WatchdogScope(self.test_generator.main_generator, '{0}_TEST_H'.format('_'.join(root_namespaces))):
                self.generate_tests(namespace_generators)
        else:
            self.generate_tests(namespace_generators)
