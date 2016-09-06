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


import copy
from LifecycleTraits import CreateLifecycleTraits

class TemplateProcessor(object):
    def __init__(self, capi_generator):
        self.capi_generator = capi_generator
        self.begin_namespace_callback = None
        self.end_namespace_callback = None
        self.template_callback = None
        self.cur_namespace_stack = []
        self.cur_namespace = None

    def __instantiate_type_impl(self, type_name, name, value):
        return type_name.replace(name, value)

    def __instantiate_return_type_impl(self, type_name, name, value):
        return type_name.replace(name, value)

    def __instantiate_impl_type_impl(self, type_name, name, value):
        return type_name.replace(name, value)

    def __instantiate_type(self, type_name, instantiation):
        for argument in instantiation.arguments:
            type_name = self.__instantiate_type_impl(type_name, argument.name, argument.value)
        return type_name

    def __instantiate_return_type(self, type_name, instantiation):
        for argument in instantiation.arguments:
            type_name = self.__instantiate_return_type_impl(type_name, argument.name, argument.value)
        return type_name

    def __instantiate_impl_type(self, type_name, instantiation):
        for argument in instantiation.arguments:
            type_name = self.__instantiate_impl_type_impl(type_name, argument.name, argument.value)
        return type_name

    def __instantiate_constructor(self, constructor, instantiation):
        for argument in constructor.arguments:
            argument.type_name = self.__instantiate_type(argument.type_name, instantiation)

    def __instantiate_method(self, method, instantiation):
        self.__instantiate_constructor(method, instantiation)
        method.return_type = self.__instantiate_return_type(method.return_type, instantiation)

    def __begin_namespace_callback(self, namespace):
        self.capi_generator.cur_namespace_path.append(namespace.name)
        self.cur_namespace_stack.append(self.cur_namespace)
        self.cur_namespace = namespace

    def __end_namespace_callback(self, namespace):
        self.capi_generator.cur_namespace_path.pop()
        self.cur_namespace = self.cur_namespace_stack[-1]
        self.cur_namespace_stack.pop()

    def __generate_template_classes(self, template):
        for instantiation in template.instantiations:
            template_class = template.classes[0]
            new_class = copy.deepcopy(template_class)
            new_class.implementation_class_name = self.__instantiate_impl_type(
                new_class.implementation_class_name, instantiation)
            new_class.base = self.__instantiate_type(new_class.base, instantiation)
            for constructor in new_class.constructors:
                self.__instantiate_constructor(constructor, instantiation)
            for method in new_class.methods:
                self.__instantiate_method(method, instantiation)
            new_class.template_line = 'template<>'
            class_suffix = ', '.join([argument.value for argument in instantiation.arguments])
            new_class.name += '<{0}>'.format(class_suffix)
            self.cur_namespace.classes.append(new_class)
        # print("template name = {0}".format(template.name))

    def process_template(self, template):
        if self.template_callback:
            self.template_callback(self, template)

    def process_namespace(self, namespace):
        if self.begin_namespace_callback:
            self.begin_namespace_callback(self, namespace)
        for nested_namespace in namespace.namespaces:
            self.process_namespace(nested_namespace)
        for cur_template in namespace.templates:
            self.process_template(cur_template)
        if self.end_namespace_callback:
            self.end_namespace_callback(self, namespace)

    def process_root_node(self, root_node):
        for cur_namespace in root_node.namespaces:
            self.process_namespace(cur_namespace)

    def process(self, root_node):
        self.begin_namespace_callback = TemplateProcessor.__begin_namespace_callback
        self.end_namespace_callback = TemplateProcessor.__end_namespace_callback
        self.template_callback = TemplateProcessor.__generate_template_classes
        self.process_root_node(root_node)
