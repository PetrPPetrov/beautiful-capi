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


class TemplateArgument(object):
    def __init__(self, name, value, template_argument_type):
        self.name = name
        self.value = value
        self.template_argument_type = template_argument_type


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


def instantiate_property(cur_property, instantiation: TInstantiation):
    cur_property.type_name = instantiate_type(cur_property.type_name, instantiation)
    cur_property.return_type = instantiate_type(cur_property.return_type, instantiation)
    cur_property.set_argument_type = instantiate_type(cur_property.set_argument_type, instantiation)


def generate_template_classes(namespace: TNamespace, template: TTemplate):
    if not template.classes:
        raise BeautifulCapiException('template have to contain a nested class')
    template_class = template.classes[0]
    name2type = {}
    for template_argument in template.arguments:
        name2type.update({template_argument.name: template_argument.type_name})
    for instantiation in template.instantiations:
        new_class = copy.deepcopy(template_class)
        if instantiation.implementation_class_name_filled:
            new_class.implementation_class_name = instantiation.implementation_class_name
        else:
            new_class.implementation_class_name = instantiate_type(new_class.implementation_class_name, instantiation)
        if instantiation.typedef_name:
            new_class.typedef_name = instantiation.typedef_name
        new_class.base = instantiate_type(new_class.base, instantiation)
        for constructor in new_class.constructors:
            instantiate_constructor(constructor, instantiation)
        for method in new_class.methods:
            instantiate_method(method, instantiation)
        for cur_property in new_class.properties:
            instantiate_property(cur_property, instantiation)
        for lifecycle_extension in new_class.lifecycle_extensions:
            lifecycle_extension.name = instantiate_type(lifecycle_extension.name, instantiation)
            lifecycle_extension.wrap_name = instantiate_type(lifecycle_extension.wrap_name, instantiation)
            for cast_to in lifecycle_extension.cast_tos:
                cast_to.target_type = instantiate_type(cast_to.target_type, instantiation)
            for cast_from in lifecycle_extension.cast_froms:
                cast_from.source_type = instantiate_type(cast_from.source_type, instantiation)
        for typedef in new_class.typedefs:
            typedef.type = instantiate_type(typedef.type, instantiation)
        for constant in new_class.constants:
            constant.type = instantiate_type(constant.type, instantiation)
            constant.value = instantiate_type(constant.value, instantiation)

        name2value = {}
        for instantiation_argument in instantiation.arguments:
            name2value.update({instantiation_argument.name: instantiation_argument.value})
        new_class.template_arguments = []
        for template_argument in template.arguments:
            if template_argument.name not in name2value:
                raise BeautifulCapiException('The required template argument ({0}) is not specified'.format(
                    template_argument.name))
            template_argument_value = name2value[template_argument.name]
            template_argument_type = name2type[template_argument.name]
            new_template_argument = TemplateArgument(
                template_argument.name, template_argument_value, template_argument_type)
            new_class.template_arguments.append(new_template_argument)

        new_class.template_line = 'template<>'
        class_suffix = ', '.join([argument.value for argument in new_class.template_arguments])
        new_class.name += '<{0}>'.format(class_suffix)
        new_class.instantiation = instantiation
        namespace.classes.append(new_class)

        if not template.wrap_csharp_templates:
            # Create special class for C# wrappers
            # This is the case when C# generics for C++ templates are not generated
            # instead of that normal C# classes are generated, without any generics
            new_csharp_wrap_class = copy.deepcopy(new_class)
            new_csharp_wrap_class.template_arguments = []
            new_csharp_wrap_class.template_line = ''
            new_csharp_wrap_class.name = new_class.typedef_name
            if not new_class.typedef_name:
                raise BeautifulCapiException(
                    'Template ({0}) instantiation does not specify typedef name'.format(template_class.name))
            new_csharp_wrap_class.typedef_name = ''
            new_csharp_wrap_class.instantiation = None
            new_class.wrap_csharp_class = new_csharp_wrap_class


def process_namespace(namespace: TNamespace):
    for nested_namespace in namespace.namespaces:
        process_namespace(nested_namespace)
    for cur_template in namespace.templates:
        generate_template_classes(namespace, cur_template)


def process(root_node: TBeautifulCapiRoot):
    for cur_namespace in root_node.namespaces:
        process_namespace(cur_namespace)
