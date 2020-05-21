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

import CapiGenerator
from DoxygenCpp import DoxygenCppGenerator
from Parser import TTemplate
from FileGenerator import FileGenerator, WatchdogScope, IndentScope
from ClassGenerator import ClassGenerator
from ArgumentGenerator import ClassTypeGenerator, EnumTypeGenerator
from FileCache import FileCache
from Helpers import get_template_name


class TemplateGenerator(object):
    def __init__(self, template_object: TTemplate, parent_namespace, params):
        self.template_object = template_object
        self.parent_namespace = parent_namespace
        # We have pre-condition that classes array has at least one element
        self.template_class = template_object.classes[0]
        self.template_class_generator = ClassGenerator(self.template_class, parent_namespace, params)
        self.params = params

    @property
    def full_wrap_name_array(self):
        if self.parent_namespace:
            return self.parent_namespace.full_name_array + [self.template_class_generator.wrap_name]
        return self.template_class_generator.wrap_name

    def generate_forward_declaration(self, out: FileGenerator):
        template_arguments = ', '.join(
            ['{0} {1}'.format(argument.type_name, argument.name) for argument in self.template_object.arguments])
        out.put_line('template<{0}>'.format(template_arguments))
        self.template_class_generator.generate_forward_declaration(out)
        for lifecycle_extension in self.template_object.classes[0].lifecycle_extensions:
            out.put_line('template<{0}>'.format(template_arguments))
            out.put_line('class {0};'.format(get_template_name(lifecycle_extension.wrap_name)))

    def __generate_declaration(self, file_cache: FileCache, capi_generator: CapiGenerator):
        full_name_array = self.parent_namespace.full_name_array + [self.template_class.name]
        header = file_cache.get_file_for_class_decl(full_name_array)
        header.put_begin_cpp_comments(self.params)
        with WatchdogScope(header, '::'.join(full_name_array).upper() + '_DECLARATION_INCLUDED'):
            for namespace in self.parent_namespace.full_name_array:
                header.put_line('namespace {}'.format(namespace))
                header.put_line('{')
                header.increase_indent()
            DoxygenCppGenerator().generate_for_template(header, self)
            args = ', '.join(['{0} {1}'.format(arg.type_name, arg.name) for arg in self.template_object.arguments])
            header.put_line('template<{0}>'.format(args))
            if self.template_class_generator.base_class_generator:
                header.put_line('class {name} : public {base_class}'.format(
                    name=self.template_class_generator.wrap_name,
                    base_class=self.template_class_generator.base_class_generator.full_wrap_name))
            else:
                header.put_line('class {name}'.format(name=self.template_class_generator.wrap_name))
            with IndentScope(header, ending='};'):
                header.put_line('public:')
                for method in self.template_class_generator.method_generators:
                    DoxygenCppGenerator().generate_for_template_method(header, self, method)
                    header.put_line('{};'.format(method.wrap_declaration(capi_generator)))
                    header.put_line('')
            for namespace in self.parent_namespace.full_name_array:
                header.decrease_indent()
                header.put_line('}')

    def generate(self, file_cache: FileCache, capi_generator: CapiGenerator):
        if self.template_class.documentations:
            self.__generate_declaration(file_cache, capi_generator)


class TemplateConstantArgumentGenerator(object):
    def __init__(self, value):
        self.value = value

    def wrap_return_type(self) -> str:
        return self.value

    def include_dependent_declaration_headers(self, file_generator: FileGenerator, file_cache: FileCache):
        pass

    @staticmethod
    def dependent_implementation_headers():
        return []


class TemplateSnippetGenerator(object):
    def __init__(self, name_array: [str], instance_generators: [ClassGenerator]):
        self.name_array = name_array
        self.dependency_headers = []
        self.dependencies = TemplateDependency('')
        self.ignored_instances = []
        self.instances = instance_generators

    def __generate(self):
        for instantiation in self.instances:
            for argument in instantiation.template_argument_generators:
                generator = None
                is_class = isinstance(argument, ClassTypeGenerator)
                is_enum = isinstance(argument, EnumTypeGenerator)
                add_header = add_forwards = True
                unusable = False
                if is_class:
                    generator = argument.class_argument_generator
                    add_forwards = not generator.is_template
                elif is_enum:
                    generator = argument.enum_argument_generator
                    add_header = add_forwards = generator.is_in_namespace
                    unusable = not generator.is_in_namespace

                if generator:
                    if add_header:
                        self.dependency_headers += [header for header in generator.dependent_implementation_headers()
                                                    if header not in self.dependency_headers]
                    if add_forwards:
                        tokens = generator.implementation_name.split('::')
                        ns = self.dependencies
                        while len(tokens) > 1:
                            ns = ns.emplace_namespace(tokens[0])
                            tokens = tokens[1:]
                        if is_class:
                            ns.add_class(tokens[0])
                        elif is_enum:
                            ns.add_enum(tokens[0])

                if unusable:
                    self.ignored_instances.append(instantiation)

    def generate(self, file_cache: FileCache):
        self.__generate()

        forwards_snippet_file = file_cache.get_file_for_template_forwards_snippet(self.name_array)
        for dependency in self.dependencies.namespaces:
            self.dependencies.namespaces[dependency].write_forwards(forwards_snippet_file)

        instance_snippet_file = file_cache.get_file_for_template_instance_snippet(self.name_array)
        for header in self.dependency_headers:
            instance_snippet_file.put_line('#include "{}"'.format(header))

        alias_snippet_file = file_cache.get_file_for_template_alias_snippet(self.name_array)
        extern_snippet_file = file_cache.get_file_for_template_extern_snippet(self.name_array)
        for instantiation in self.instances:
            if instantiation in self.ignored_instances:
                continue
            alias_snippet_file.put_line('typedef {} {};'.format(instantiation.snippet_implementation_declaration, instantiation.template_name))
            extern_snippet_file.put_line('extern template class {};'.format(instantiation.implementation_name))
            instance_snippet_file.put_line('template class {};'.format(instantiation.implementation_name))


class TemplateDependency(object):
    def __init__(self, name: str, namespaces: {str: {}} = None, classes: [str] = None, enums: [str] = None):
        self.name = name
        self.namespaces = namespaces if namespaces is not None else {}
        self.classes = classes if classes is not None else []
        self.enums = enums if enums is not None else []

    def write_forwards(self, file: FileGenerator):
        file.put_line('namespace {}'.format(self.name), ' ')
        with IndentScope(file):
            for name in self.classes:
                file.put_line('class {};'.format(name))
            for name in self.enums:
                file.put_line('enum {};'.format(name))
            for namespace in self.namespaces:
                self.namespaces[namespace].write_forwards(file)

    def namespace(self, name: str):
        return self.namespaces[name] if name in self.namespaces else None

    def add_class(self, name: str):
        if name not in self.classes:
            self.classes.append(name)

    def add_enum(self, name: str):
        if name not in self.enums:
            self.enums.append(name)

    def emplace_namespace(self, name: str) -> {}:
        if name not in self.namespaces.keys():
            self.namespaces.update({name: TemplateDependency(name)})
        return self.namespaces[name]
