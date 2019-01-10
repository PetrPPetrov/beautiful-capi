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
