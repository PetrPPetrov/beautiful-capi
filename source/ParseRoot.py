#!/usr/bin/env python
#
# Beautiful Capi generates beautiful C API wrappers for your C++ classes
# Copyright (C) 2016 Petr Petrovich Petrov
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

import os
from xml.dom.minidom import parse as dom_parse

from Parser import load
from FileCache import full_relative_path_from_candidates


def get_all_namespaces(root_namespaces: list):
    result = root_namespaces.copy()
    for namespace in root_namespaces:
        result += get_all_namespaces(namespace.namespaces)
    return result


def parse_root(root_api_xml_path: str, params):
    root_api = load(dom_parse(root_api_xml_path))
    namespaces = get_all_namespaces(root_api.namespaces)
    if not hasattr(params, "xml_paths"):
        params.xml_paths = []

    if root_api.include_once:
        params.xml_paths.append(root_api_xml_path)

    cur_dir = os.path.dirname(root_api_xml_path)
    for namespace in namespaces:
        for include in namespace.includes:
            path = full_relative_path_from_candidates(include.path, cur_dir, params.additional_include_directories)
            if os.path.exists(path) and path not in params.xml_paths:
                if params.verbosity:
                    print('loading XML API description: {0}'.format(path))
                sub_api = parse_root(path, params)

                def update_named_attr(source, destination, attr_name: str):
                    if hasattr(source, attr_name) and hasattr(destination, attr_name):
                        dst_attr = getattr(destination, attr_name)
                        used_names = [element.name for element in dst_attr]
                        src_attr = getattr(source, attr_name)
                        for sub_element in src_attr:
                            sub_name = sub_element.name
                            if sub_name in used_names:
                                print(
                                    "WARNING: {path} namespace {root} already contains {sub}; "
                                    "skipping import from {include}".format(
                                        root=destination.name, sub=sub_name, path=root_api_xml_path, include=path
                                    )
                                )
                            else:
                                dst_attr.append(sub_element)
                                used_names.append(sub_name)

                def update_array(source, destination, array_name: str):
                    if hasattr(source, array_name) and hasattr(destination, array_name):
                        dst_attr = getattr(destination, array_name)
                        src_attr = getattr(source, array_name)
                        for sub_element in src_attr:
                            dst_attr.append(sub_element)

                if include.use_content_without_root_namespaces:
                    for sub_api_nested_ns in sub_api.namespaces:
                        update_array(sub_api_nested_ns, namespace, 'external_libraries')
                        update_named_attr(sub_api_nested_ns, namespace, 'namespaces')
                        update_array(sub_api_nested_ns, namespace, 'include_headers')
                        update_named_attr(sub_api_nested_ns, namespace, 'enumerations')
                        update_named_attr(sub_api_nested_ns, namespace, 'classes')
                        update_named_attr(sub_api_nested_ns, namespace, 'functions')
                        update_array(sub_api_nested_ns, namespace, 'templates')
                        update_named_attr(sub_api_nested_ns, namespace, 'mapped_types')
                else:
                    update_named_attr(sub_api, namespace, 'namespaces')
                if params.verbosity:
                    print('loaded XML API description: {0}'.format(path))

    return root_api
