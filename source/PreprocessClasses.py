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
import Helpers
from LifecycleTraits import CreateLifecycleTraits


class ExtraInfo(object):
    def __init__(self, capi_generator):
        self.capi_generator = capi_generator
        self.full_name_array = None
        self.base_class_object = None
        self.derived_objects = []
        self.class_object = None

    def get_class_name(self):
        with CreateLifecycleTraits(self.class_object, self.capi_generator):
            temp_full_array = copy.deepcopy(self.full_name_array)
            temp_full_array[-1] = Helpers.get_template_name(temp_full_array[-1])
            result = '::'.join(temp_full_array) + self.capi_generator.lifecycle_traits.get_suffix()
            return Helpers.format_type(result + Helpers.get_template_tail(self.full_name_array[-1]))

    def get_class_short_name(self):
        with CreateLifecycleTraits(self.class_object, self.capi_generator):
            result = Helpers.get_template_name(self.full_name_array[-1])
            result += self.capi_generator.lifecycle_traits.get_suffix()
            return Helpers.format_type(result + Helpers.get_template_tail(self.full_name_array[-1]))

    def get_fwd_class_name(self):
        if '<' in self.class_object.name:
            return '{0}::forward_pointer_holder<{1} >'.format(
                self.capi_generator.params_description.beautiful_capi_namespace,
                self.get_class_name()
            )
        else:
            return '::'.join(self.full_name_array) + self.capi_generator.params_description.forward_typedef_suffix

    def get_c_name(self):
        return Helpers.replace_template_to_c_id('_'.join(self.full_name_array).lower())


def replace_template_by_implementation_classes(capi_generator, implementation_class_name):
    template_arguments_count = Helpers.get_template_arguments_count(implementation_class_name)
    for index in range(template_arguments_count):
        original_template_argument = Helpers.get_template_argument(implementation_class_name, index)
        template_argument = replace_template_by_implementation_classes(capi_generator, original_template_argument)
        sub_class_type = capi_generator.get_class_type(original_template_argument)
        if sub_class_type:
            implementation_class_name = Helpers.replace_template_argument(
                implementation_class_name, index, sub_class_type.implementation_class_name)
        else:
            implementation_class_name = Helpers.replace_template_argument(
                implementation_class_name, index, template_argument)
    return implementation_class_name


def replace_template_by_wrap_classes(capi_generator, class_name):
    template_arguments_count = Helpers.get_template_arguments_count(class_name)
    for index in range(template_arguments_count):
        original_template_argument = Helpers.get_template_argument(class_name, index)
        template_argument = replace_template_by_wrap_classes(capi_generator, original_template_argument)
        sub_class_type = capi_generator.get_class_type(original_template_argument)
        if sub_class_type:
            extra_info = capi_generator.extra_info[sub_class_type]
            class_name = Helpers.replace_template_argument(
                class_name, index, extra_info.get_class_name())
        else:
            class_name = Helpers.replace_template_argument(
                class_name, index, template_argument)
    return class_name


def process_beautiful_capi_class(cur_class, cur_name_path, capi_generator):
    with Helpers.NamespaceScope(cur_name_path, cur_class):
        extra_info_entry = ExtraInfo(capi_generator)
        extra_info_entry.full_name_array = copy.deepcopy(cur_name_path)
        extra_info_entry.class_object = cur_class
        cur_base_class_str = cur_class.base
        if cur_base_class_str:
            cur_base_class = capi_generator.get_class_type(cur_base_class_str)
            if cur_base_class:
                extra_info_entry.base_class_object = cur_base_class
                # Update derived_objects in base class
                if cur_base_class in capi_generator.extra_info:
                    # Case when base class was processed
                    if cur_class not in capi_generator.extra_info[cur_base_class].derived_objects:
                        capi_generator.extra_info[cur_base_class].derived_objects.append(cur_class)
                else:
                    # Case when base class wasn't processed yet, make dummy entry for it
                    base_class_dummy_extra_info_entry = ExtraInfo(capi_generator)
                    base_class_dummy_extra_info_entry.class_object = cur_base_class
                    base_class_dummy_extra_info_entry.derived_objects.append(cur_class)
                    capi_generator.extra_info.update({cur_base_class: base_class_dummy_extra_info_entry})
            else:
                print('Warning: base class ("{0}") is not found'.format(cur_base_class_str))
        # If dummy entry with derived_objects is exist then merge it
        if cur_class in capi_generator.extra_info:
            extra_info_entry.derived_objects += capi_generator.extra_info[cur_class].derived_objects
        capi_generator.extra_info.update({cur_class: extra_info_entry})
        # print('implementation class {0}'.format(cur_class.implementation_class_name))
        cur_class.implementation_class_name = replace_template_by_implementation_classes(
            capi_generator, cur_class.implementation_class_name)
        # print('was replaced by {0}'.format(cur_class.implementation_class_name))


def process_beautiful_capi_constructor_for_templates(cur_constructor, capi_generator):
    for cur_argument in cur_constructor.arguments:
        cur_argument.type_name = replace_template_by_wrap_classes(capi_generator, cur_argument.type_name)


def process_beautiful_capi_method_for_templates(cur_method, capi_generator):
    process_beautiful_capi_constructor_for_templates(cur_method, capi_generator)
    cur_method.return_type = replace_template_by_wrap_classes(capi_generator, cur_method.return_type)


def process_beautiful_capi_class_for_templates(cur_class, capi_generator):
    for cur_constructor in cur_class.constructors:
        process_beautiful_capi_constructor_for_templates(cur_constructor, capi_generator)
    for cur_method in cur_class.methods:
        process_beautiful_capi_method_for_templates(cur_method, capi_generator)
    #print('class name {0}'.format(cur_class.name))
    cur_class.name = replace_template_by_wrap_classes(capi_generator, cur_class.name)
    capi_generator.extra_info[cur_class].full_name_array[-1] = cur_class.name
    cur_class.base = replace_template_by_wrap_classes(capi_generator, cur_class.base)
    #print('was replaced by {0}'.format(cur_class.name))


def process_beautiful_capi_namespace(cur_namespace, cur_name_path, capi_generator):
    with Helpers.NamespaceScope(cur_name_path, cur_namespace):
        extra_info_entry = ExtraInfo(capi_generator)
        extra_info_entry.full_name_array = copy.deepcopy(cur_name_path)
        extra_info_entry.class_object = cur_namespace
        capi_generator.extra_info.update({cur_namespace: extra_info_entry})
        for cur_sub_namespace in cur_namespace.namespaces:
            process_beautiful_capi_namespace(cur_sub_namespace, cur_name_path, capi_generator)
        for cur_class in cur_namespace.classes:
            process_beautiful_capi_class(cur_class, cur_name_path, capi_generator)


def process_beautiful_capi_namespace_for_templates(cur_namespace, capi_generator):
    for cur_sub_namespace in cur_namespace.namespaces:
        process_beautiful_capi_namespace_for_templates(cur_sub_namespace, capi_generator)
    for cur_class in cur_namespace.classes:
        process_beautiful_capi_class_for_templates(cur_class, capi_generator)
    for cur_function in cur_namespace.functions:
        process_beautiful_capi_method_for_templates(cur_function, capi_generator)


def pre_process_beautiful_capi_root(root_node, capi_generator):
    cur_name_path = []
    for cur_namespace in root_node.namespaces:
        process_beautiful_capi_namespace(cur_namespace, cur_name_path, capi_generator)
    for cur_namespace in root_node.namespaces:
        process_beautiful_capi_namespace_for_templates(cur_namespace, capi_generator)
