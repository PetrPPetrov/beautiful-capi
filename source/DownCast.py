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

import FileGenerator
import Helpers
from LifecycleTraits import CreateLifecycleTraits


def generate_down_cast(output_file, cur_class, base_class, capi_generator):
    cur_class_extra_info = capi_generator.extra_info[cur_class]
    base_class_extra_info = capi_generator.extra_info[base_class]
    output_file.put_line('template<>')
    output_file.put_line(
        'inline {return_type} down_cast(const {input_type}& input_object)'.format(
            return_type=cur_class_extra_info.get_class_name(),
            input_type=base_class_extra_info.get_class_name()
        )
    )
    with FileGenerator.IndentScope(output_file):
        Helpers.put_raw_pointer_structure(output_file)
        c_function_name = '{0}_cast_to_{1}'.format(
            base_class_extra_info.get_c_name(),
            cur_class_extra_info.get_c_name()
        )
        output_file.put_line(
            'return {0}({1}(reinterpret_cast<const raw_pointer_holder*>(&input_object)->raw_pointer), true);'.format(
                cur_class_extra_info.get_class_name(),
                c_function_name,
            )
        )
        c_function_declaration = 'void* {{convention}} {0}(void* object_pointer)'.format(c_function_name)
        capi_generator.loader_traits.add_c_function_declaration(c_function_declaration)
        with FileGenerator.IndentScope(capi_generator.output_source):
            capi_generator.output_source.put_line(
                'return dynamic_cast<{0}*>(static_cast<{1}*>(object_pointer));'.format(
                    cur_class.implementation_class_name,
                    base_class.implementation_class_name
                )
            )
        capi_generator.output_source.put_line('')
    output_file.put_line('')


def generate_down_casts_for_class(output_file, cur_class, capi_generator):
    if cur_class.base:
        cur_base_class = cur_class
        while cur_base_class.base:
            extra_info_entry = capi_generator.extra_info[cur_base_class]
            next_base_class = extra_info_entry.base_class_object
            if next_base_class:
                generate_down_cast(output_file, cur_class, next_base_class, capi_generator)
                cur_base_class = next_base_class
            else:
                break


def generate_down_casts_for_namespace(output_file, namespace, capi_generator):
    output_file.put_line('template<typename TargetType, typename SourceType>')
    output_file.put_line('TargetType down_cast(const SourceType&);')
    output_file.put_line('')
    for cur_class in namespace.classes:
        with CreateLifecycleTraits(cur_class, capi_generator):
            generate_down_casts_for_class(output_file, cur_class, capi_generator)
    for nested_namespace in namespace.namespaces:
        generate_down_casts_for_namespace(output_file, nested_namespace, capi_generator)
