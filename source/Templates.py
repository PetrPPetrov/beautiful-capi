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

from Parser import TInstantiation, TConstructor, TMethod, TNamespace, TTemplate, TBeautifulCapiRoot
from Helpers import BeautifulCapiException


def instantiate_type(type_name: str, instantiation: TInstantiation):
    for argument in instantiation.arguments:
        type_name = type_name.replace(argument.name, argument.value)
    return type_name


def instantiate_constructor(constructor: TConstructor or TMethod, instantiation: TInstantiation):
    for argument in constructor.arguments:
        argument.type_name = instantiate_type(argument.type_name, instantiation)


def instantiate_method(method: TMethod, instantiation: TInstantiation):
    instantiate_constructor(method, instantiation)
    method.return_type = instantiate_type(method.return_type, instantiation)


def generate_template_classes(namespace: TNamespace, template: TTemplate):
    if not template.classes:
        raise BeautifulCapiException('template have to contain a nested class')
    template_class = template.classes[0]
    for instantiation in template.instantiations:
        new_class = copy.deepcopy(template_class)
        new_class.implementation_class_name = instantiate_type(new_class.implementation_class_name, instantiation)
        if instantiation.typedef_name:
            new_class.typedef_name = instantiation.typedef_name
        new_class.base = instantiate_type(new_class.base, instantiation)
        for constructor in new_class.constructors:
            instantiate_constructor(constructor, instantiation)
        for method in new_class.methods:
            instantiate_method(method, instantiation)
        new_class.template_line = 'template<>'
        class_suffix = ', '.join([argument.value for argument in instantiation.arguments])
        new_class.name += '<{0}>'.format(class_suffix)
        namespace.classes.append(new_class)


def process_namespace(namespace: TNamespace):
    for nested_namespace in namespace.namespaces:
        process_namespace(nested_namespace)
    for cur_template in namespace.templates:
        generate_template_classes(namespace, cur_template)


def process(root_node: TBeautifulCapiRoot):
    for cur_namespace in root_node.namespaces:
        process_namespace(cur_namespace)
