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
from Helpers import NamespaceScope
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
            return '::'.join(self.full_name_array) + self.capi_generator.lifecycle_traits.get_suffix()

    def get_fwd_class_name(self):
        return '::'.join(self.full_name_array) + self.capi_generator.params_description.forward_typedef_suffix

    def get_c_name(self):
        return '_'.join(self.full_name_array).lower()


def process_beautiful_capi_class(cur_class, cur_name_path, capi_generator):
    with NamespaceScope(cur_name_path, cur_class):
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


def process_beautiful_capi_namespace(cur_namespace, cur_name_path, capi_generator):
    with NamespaceScope(cur_name_path, cur_namespace):
        extra_info_entry = ExtraInfo(capi_generator)
        extra_info_entry.full_name_array = copy.deepcopy(cur_name_path)
        extra_info_entry.class_object = cur_namespace
        capi_generator.extra_info.update({cur_namespace: extra_info_entry})
        for cur_sub_namespace in cur_namespace.namespaces:
            process_beautiful_capi_namespace(cur_sub_namespace, cur_name_path, capi_generator)
        for cur_class in cur_namespace.classes:
            process_beautiful_capi_class(cur_class, cur_name_path, capi_generator)


def pre_process_beautiful_capi_root(root_node, capi_generator):
    cur_name_path = []
    for cur_namespace in root_node.namespaces:
        process_beautiful_capi_namespace(cur_namespace, cur_name_path, capi_generator)
